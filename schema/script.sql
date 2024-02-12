-- Mon Feb 12 11:41:03 2024
-- Model: New Model    Version: 1.0

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema ecommerce_db
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema ecommerce_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `ecommerce_db` DEFAULT CHARACTER SET utf8 ;
USE `ecommerce_db` ;

-- -----------------------------------------------------
-- Table `ecommerce_db`.`admin_users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ecommerce_db`.`admin_users` (
  `id` BINARY(16) NOT NULL,
  `email` VARCHAR(150) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT now(),
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE);


-- -----------------------------------------------------
-- Table `ecommerce_db`.`customers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ecommerce_db`.`customers` (
  `id` BINARY(16) NOT NULL,
  `full_name` VARCHAR(150) NOT NULL,
  `email` VARCHAR(150) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT now(),
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `full_name_UNIQUE` (`full_name` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE);


-- -----------------------------------------------------
-- Table `ecommerce_db`.`categories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ecommerce_db`.`categories` (
  `id` BINARY(16) NOT NULL,
  `name` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX (`name` ASC) VISIBLE,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE);


-- -----------------------------------------------------
-- Table `ecommerce_db`.`products`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ecommerce_db`.`products` (
  `id` BINARY(16) NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `description` TEXT NULL DEFAULT NULL,
  `price` DECIMAL NOT NULL,
  `quantity` INT NULL,
  `category_id` BINARY(16) NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT now(),
  `updated_at` TIMESTAMP NOT NULL,
  PRIMARY KEY (`id`),
  INDEX (`category_id` ASC) VISIBLE,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  CONSTRAINT `fk_products_category_id`
    FOREIGN KEY (`category_id`)
    REFERENCES `ecommerce_db`.`categories` (`id`));


-- -----------------------------------------------------
-- Table `ecommerce_db`.`orders`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ecommerce_db`.`orders` (
  `id` BINARY(16) NOT NULL,
  `customer_id` BINARY(16) NOT NULL,
  `order_date` DATETIME NOT NULL,
  `status` ENUM('processing', 'shipped', 'canceled') NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT now(),
  `updated_at` TIMESTAMP NOT NULL,
  PRIMARY KEY (`id`),
  INDEX (`customer_id` ASC) VISIBLE,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `customer_id_UNIQUE` (`customer_id` ASC) VISIBLE,
  CONSTRAINT `fk_orders_customer_id`
    FOREIGN KEY (`customer_id`)
    REFERENCES `ecommerce_db`.`customers` (`id`));


-- -----------------------------------------------------
-- Table `ecommerce_db`.`order_details`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ecommerce_db`.`order_details` (
  `id` BINARY(16) NOT NULL,
  `order_id` BINARY(16) NOT NULL,
  `product_id` BINARY(16) NOT NULL,
  `quantity` INT NOT NULL,
  `unit_price` DOUBLE NOT NULL,
  `total_price` DOUBLE NOT NULL,
  PRIMARY KEY (`id`),
  INDEX (`order_id` ASC) VISIBLE,
  INDEX (`product_id` ASC) VISIBLE,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  CONSTRAINT `fk_order_details_order_id`
    FOREIGN KEY (`order_id`)
    REFERENCES `ecommerce_db`.`orders` (`id`),
  CONSTRAINT `fk_order_details_product_id`
    FOREIGN KEY (`product_id`)
    REFERENCES `ecommerce_db`.`products` (`id`));


-- -----------------------------------------------------
-- Table `ecommerce_db`.`shopping_cart`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ecommerce_db`.`shopping_cart` (
  `id` BINARY(16) NOT NULL,
  `customer_id` BINARY(16) NOT NULL,
  `product_id` BINARY(16) NULL DEFAULT NULL,
  `quantity` INT NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX (`customer_id` ASC) VISIBLE,
  INDEX (`product_id` ASC) VISIBLE,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `customer_id_UNIQUE` (`customer_id` ASC) VISIBLE,
  CONSTRAINT `fk_shopping_cart_customer_id`
    FOREIGN KEY (`customer_id`)
    REFERENCES `ecommerce_db`.`customers` (`id`),
  CONSTRAINT `fk_shopping_cart_product_id`
    FOREIGN KEY (`product_id`)
    REFERENCES `ecommerce_db`.`products` (`id`));


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
