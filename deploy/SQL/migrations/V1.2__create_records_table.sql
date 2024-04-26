CREATE TABLE records
(
    id               UUID PRIMARY KEY,
    created_at       TIMESTAMPTZ DEFAULT now()::TIMESTAMPTZ,
    last_modified_at TIMESTAMPTZ DEFAULT now()::TIMESTAMPTZ,
    api_call_id           UUID NOT NULL,
    title         TEXT     NOT NULL,
    description   TEXT     NOT NULL,
    thumbnail_URL     TEXT NOT NULL,
    publish_time   TIMESTAMPTZ NOT NULL,
    FOREIGN KEY (api_call_id) REFERENCES api_call (id)
);

CREATE INDEX records_call_id_idx ON records (api_call_id);
