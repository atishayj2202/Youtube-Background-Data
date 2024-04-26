CREATE TYPE call_status AS ENUM ('NOT_FOUND', 'SUCCESS', 'FAILED');

CREATE TABLE api_call
(
    id               UUID PRIMARY KEY,
    created_at       TIMESTAMPTZ DEFAULT now()::TIMESTAMPTZ,
    last_modified_at TIMESTAMPTZ DEFAULT now()::TIMESTAMPTZ,
    topic            VARCHAR NOT NULL,
    records             INT NOT NULL,
    published_after TIMESTAMPTZ NOT NULL,
    status call_status NOT NULL
);