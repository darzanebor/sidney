CREATE TABLE `thumbnail` (
	`id`   INTEGER PRIMARY KEY,
	`url`  VARCHAR NOT NULL,
	`path` VARCHAR NOT NULL,
	`link` VARCHAR NOT NULL,
	`size` VARCHAR NOT NULL,
	`mime` VARCHAR NOT NULL,
    `hash` VARCHAR
);