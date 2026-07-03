create table support_documents (
    id text primary key,
    title text not null,
    category text not null,
    summary text not null,
    body text not null,
    keywords text[] not null default '{}',
    is_active boolean not null default true,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create index support_documents_category_idx
    on support_documents (category)
    where is_active;

create index support_documents_keywords_idx
    on support_documents
    using gin (keywords)
    where is_active;

-- Run `python3 -m support_agent.ingest_policies` to load markdown files from docs/policies.
