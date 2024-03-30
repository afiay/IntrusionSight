# schema.sql
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS network_traffic (
    id INTEGER PRIMARY KEY,
    src_ip TEXT NOT NULL,
    dst_ip TEXT NOT NULL,
    protocol TEXT NOT NULL,
    src_port INTEGER,
    dst_port INTEGER,
    packet_length INTEGER,
    flags TEXT,
    checksum TEXT,
    ttl INTEGER,
    ihl INTEGER,
    tos INTEGER,
    payload TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    label TEXT -- 'normal' or 'anomaly', this may be NULL if unlabeled
);
