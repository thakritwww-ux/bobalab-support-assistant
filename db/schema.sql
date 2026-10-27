CREATE TABLE IF NOT EXISTS prompt_versions (
    id uuid PRIMARY KEY,
    created_at timestamptz NOT NULL DEFAULT now(),
    parent_id uuid REFERENCES prompt_versions(id),
    source text NOT NULL CHECK (source IN ('seed','auto','manual','rollback','knowledge')),
    sections jsonb NOT NULL,
    content_hash text NOT NULL
);
CREATE TABLE IF NOT EXISTS prompt_state (
    singleton boolean PRIMARY KEY DEFAULT true CHECK (singleton),
    active_version uuid NOT NULL REFERENCES prompt_versions(id)
);
CREATE TABLE IF NOT EXISTS improvement_events (
    id uuid PRIMARY KEY,
    created_at timestamptz NOT NULL DEFAULT now(),
    base_version uuid NOT NULL REFERENCES prompt_versions(id),
    result_version uuid NOT NULL REFERENCES prompt_versions(id),
    source text NOT NULL,
    outcome text NOT NULL CHECK (outcome IN ('applied','no_change','rejected')),
    operations jsonb NOT NULL,
    rejected jsonb NOT NULL
);
CREATE TABLE IF NOT EXISTS model_usage (
    day date PRIMARY KEY,
    calls integer NOT NULL CHECK (calls >= 0)
);

-- These tables contain server-only application configuration. No anon REST access.
ALTER TABLE prompt_versions ENABLE ROW LEVEL SECURITY;
ALTER TABLE prompt_state ENABLE ROW LEVEL SECURITY;
ALTER TABLE improvement_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE model_usage ENABLE ROW LEVEL SECURITY;

CREATE OR REPLACE FUNCTION protect_prompt_history() RETURNS trigger
LANGUAGE plpgsql AS $$
BEGIN
    RAISE EXCEPTION 'Prompt history is append-only';
END;
$$;
DROP TRIGGER IF EXISTS immutable_prompt_versions ON prompt_versions;
CREATE TRIGGER immutable_prompt_versions BEFORE UPDATE OR DELETE ON prompt_versions
FOR EACH ROW EXECUTE FUNCTION protect_prompt_history();
