DROP TABLE IF EXISTS urls;

CREATE TABLE urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_redirect TIMESTAMP NULL DEFAULT NULL, 
    original_url TEXT NOT NULL,
    shortcode TEXT NOT NULL, 
    clicks INTEGER NOT NULL DEFAULT 0
);

INSERT INTO urls (original_url, shortcode, clicks) 
VALUES ('https://example1.com', 'p7k9fd', 10);

INSERT INTO urls (original_url, shortcode, clicks) 
VALUES ('https://example2.com', 'p7k9gp', 10);
