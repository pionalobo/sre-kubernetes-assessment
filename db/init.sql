CREATE TABLE IF NOT EXISTS system_metrics (
    id SERIAL PRIMARY KEY,
    collected_at TIMESTAMPTZ NOT NULL,
    hostname TEXT NOT NULL,
    cpu_count INTEGER NOT NULL,
    cpu_percent DOUBLE PRECISION NOT NULL,
    memory_total BIGINT NOT NULL,
    memory_available BIGINT NOT NULL,
    memory_percent DOUBLE PRECISION NOT NULL,
    disk_total BIGINT NOT NULL,
    disk_used BIGINT NOT NULL,
    disk_percent DOUBLE PRECISION NOT NULL,
    os_info TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_system_metrics_collected_at
    ON system_metrics (collected_at);