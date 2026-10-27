import json

from app.config import ROOT


def build_pairs():
    conversations = json.loads((ROOT / "data/conversations.json").read_text())
    split_manifest = json.loads((ROOT / "data/splits.json").read_text())
    split_by_id = {
        cid: split
        for split in ("development", "validation", "final")
        for cid in split_manifest[split]
    }
    result = []
    for conversation in conversations:
        messages = conversation["conversation"]
        if any(
            b["timestamp"] < a["timestamp"] for a, b in zip(messages, messages[1:], strict=False)
        ):
            raise ValueError("Source timestamps are not ordered; do not silently reorder history")
        runs = []
        for message in messages:
            if runs and runs[-1][0]["direction"] == message["direction"]:
                runs[-1].append(message)
            else:
                runs.append([message])
        history = []
        for index, run in enumerate(runs):
            if run[0]["direction"] == "in" and index + 1 < len(runs):
                consultant = runs[index + 1]
                if consultant[0]["direction"] == "out":
                    delayed = [
                        m["message_id"]
                        for a, m in zip(consultant, consultant[1:], strict=False)
                        if m["timestamp"] - a["timestamp"] > 300000
                    ]
                    # A timing heuristic is a warning, not proof of an external event.
                    # This specific source update also claims a completed document review.
                    event_ids = set(delayed)
                    warnings = []
                    if event_ids:
                        warnings.append(
                            "delayed_operational_update_excluded_from_learning_reference"
                        )
                    if any(m["text"] == "[Non-text message]" for m in run):
                        warnings.append("attachment_contents_unavailable")
                    result.append(
                        {
                            "id": f"{conversation['contact_id']}:{run[0]['message_id']}",
                            "contact_id": conversation["contact_id"],
                            "split": split_by_id[conversation["contact_id"]],
                            "client_message_ids": [m["message_id"] for m in run],
                            "consultant_message_ids": [m["message_id"] for m in consultant],
                            "clientSequence": "\n".join(m["text"] for m in run),
                            "chatHistory": list(history),
                            "consultantReply": "\n".join(m["text"] for m in consultant),
                            "learningReference": "\n".join(
                                m["text"] for m in consultant if m["message_id"] not in event_ids
                            ),
                            "external_event_message_ids": delayed,
                            "warnings": warnings,
                        }
                    )
            history.extend(
                {"role": "client" if m["direction"] == "in" else "consultant", "message": m["text"]}
                for m in run
            )
    return result


def development_examples(limit):
    pairs = build_pairs()
    groups = {}
    for pair in pairs:
        if pair["split"] == "development":
            groups.setdefault(pair["contact_id"], []).append(pair)
    selected = []
    # Round-robin prevents one long conversation monopolizing the limited call budget.
    for index in range(max(map(len, groups.values()))):
        for group in groups.values():
            if index < len(group):
                selected.append(group[index])
                if len(selected) >= limit:
                    return selected
    return selected
