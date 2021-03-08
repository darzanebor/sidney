CREATE TABLE `thumbnail` (
	`id` INTEGER PRIMARY KEY,
	`location` TEXT NOT NULL,
	`link` VARCHAR NOT NULL,
	`size` VARCHAR NOT NULL,
	`mtype` VARCHAR NOT NULL,
    `hash` VARCHAR
);