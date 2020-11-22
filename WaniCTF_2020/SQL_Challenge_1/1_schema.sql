DROP TABLE IF EXISTS anime;

CREATE TABLE anime (
    name VARCHAR(32) NOT NULL,
    years INT(32) NOT NULL,
    PRIMARY KEY (name)
);