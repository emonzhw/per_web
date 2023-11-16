SET @@global.sql_mode= '';
SET @OLD_UNIQUE_CHECKS = @@UNIQUE_CHECKS,
    UNIQUE_CHECKS = 0;
SET @OLD_FOREIGN_KEY_CHECKS = @@FOREIGN_KEY_CHECKS,
    FOREIGN_KEY_CHECKS = 0;
SET @OLD_SQL_MODE = @@SQL_MODE,
    SQL_MODE = 'TRADITIONAL,ALLOW_INVALID_DATES';
-- -----------------------------------------------------
-- Schema demo
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `demo`;
-- -----------------------------------------------------
-- Schema demo
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `demo` DEFAULT CHARACTER SET utf8;
USE `demo`;
-- -----------------------------------------------------
-- Table `demo`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `demo`.`users`;
CREATE TABLE IF NOT EXISTS `demo`.`users` (
    `username` VARCHAR(16) NOT NULL,
    `password` VARCHAR(16) NOT NULL,
    PRIMARY KEY (`username`)
) ENGINE = InnoDB;
INSERT INTO `demo`.`users` (`username`, `password`)
VALUES ('test', 'password');
INSERT INTO `demo`.`users` (`username`, `password`)
VALUES ('test2', 'password');
INSERT INTO `demo`.`users` (`username`, `password`)
VALUES ('test2', 'new_password') ON DUPLICATE KEY
UPDATE `password` = 'duplicate_password';
DELETE FROM `demo`.`users`
WHERE `username` = 'test2';
-- -----------------------------------------------------
-- Database user setting
-- -----------------------------------------------------
SET SQL_MODE = @OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS = @OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS = @OLD_UNIQUE_CHECKS;
DROP USER IF EXISTS 'ez' @'localhost';
CREATE USER 'ez' @'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON demo.* TO 'ez' @'localhost';
