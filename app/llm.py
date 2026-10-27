import json
import logging
import time

import httpx
from google import genai
from google.genai import errors, types
from pydantic import ValidationError

from app.errors import ServiceError


class GeminiLLM:
    def __init__(self, settings, store, client=None, sleep=time.sleep):
        self.settings, self.store, self.sleep = settings, store, sleep
        self.client = client

    def complete(self, *, system, payload, schema):
        if not self.settings.gemini_api_key:
            raise ServiceError("not_configured", "The model API key is not configured.")
        if self.client is None:
            self.client = genai.Client(
                api_key=self.settings.gemini_api_key,
                http_options=types.HttpOptions(
                    timeout=self.settings.timeout_seconds * 1000,
                    retry_options=types.HttpRetryOptions(attempts=1),
                ),
            )
        for attempt in range(2):
            # Reserve even failed attempts; shared across workers and restarts.
            self.store.reserve_call(self.settings.daily_calls)
            try:
                response = self.client.models.generate_content(
                    model=self.settings.model,
                    contents=json.dumps(payload, ensure_ascii=False),
                    config=types.GenerateContentConfig(
                        system_instruction=system,
                        response_mime_type="application/json",
                        response_json_schema=schema.model_json_schema(),
                        temperature=0.2,
                        max_output_tokens=4096,
                    ),
                )
                return schema.model_validate_json(response.text or "")
            except (ValidationError, ValueError):
                if attempt:
                    raise ServiceError(
                        "invalid_model_output", "The model returned invalid structured output.", 502
                    ) from None
            except errors.APIError as exc:
                code = int(exc.code or 500)
                # Status only: response bodies can contain sensitive request data.
                logging.getLogger(__name__).warning(
                    "Gemini request failed: provider_status=%s", code
                )
                if code not in (408, 429) and code < 500:
                    raise ServiceError(
                        "model_access_error",
                        "The configured model is not accessible. Check free-tier account access.",
                    ) from None
                if attempt:
                    raise ServiceError(
                        "model_unavailable",
                        "The model is unavailable or its quota was reached. Try again later.",
                    ) from None
            except (httpx.HTTPError, TimeoutError):
                if attempt:
                    raise ServiceError(
                        "model_timeout", "The model could not respond in time. Try again later."
                    ) from None
            self.sleep(0.5)
        raise ServiceError("model_unavailable", "The model could not complete the request.")
