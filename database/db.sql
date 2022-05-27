CREATE TABLE `users` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`username` varchar(255) NOT NULL UNIQUE,
	`email` varchar(255) NOT NULL UNIQUE,
	`password` varchar(255) NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `teams` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`user_id` INT NOT NULL,
	`cartola_id` INT NOT NULL UNIQUE,
	PRIMARY KEY (`id`)
);

CREATE TABLE `leagues` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`name` varchar(255) NOT NULL UNIQUE,
	`image_url` varchar(255) NOT NULL UNIQUE,
	`type` INT NOT NULL,
	`round` INT,
	`subscribers` INT NOT NULL DEFAULT '0',
	`accumulated_value` INT NOT NULL DEFAULT '0',
	`status` BINARY NOT NULL DEFAULT '0',
	PRIMARY KEY (`id`)
);

CREATE TABLE `payments` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`league_id` INT NOT NULL,
	`cartola_id` INT NOT NULL,
	`value` INT NOT NULL,
	`date` varchar(255) NOT NULL,
	`status` varchar(255) NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `points` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`payment_id` INT NOT NULL,
	`points` FLOAT NOT NULL,
	PRIMARY KEY (`id`)
);

ALTER TABLE `teams` ADD CONSTRAINT `teams_fk0` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`);

ALTER TABLE `payments` ADD CONSTRAINT `payments_fk0` FOREIGN KEY (`league_id`) REFERENCES `leagues`(`id`);

ALTER TABLE `payments` ADD CONSTRAINT `payments_fk1` FOREIGN KEY (`cartola_id`) REFERENCES `teams`(`cartola_id`);

ALTER TABLE `points` ADD CONSTRAINT `points_fk0` FOREIGN KEY (`payment_id`) REFERENCES `payments`(`id`);
