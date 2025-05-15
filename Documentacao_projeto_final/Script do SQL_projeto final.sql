-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema dw_projeto
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema dw_projeto
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `dw_projeto` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `dw_projeto` ;

-- -----------------------------------------------------
-- Table `dw_projeto`.`aeronaves`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dw_projeto`.`aeronaves` (
  `id_aeronave` INT NOT NULL AUTO_INCREMENT,
  `modelo` VARCHAR(100) NULL DEFAULT NULL,
  `nome_do_fabricante` VARCHAR(100) NULL DEFAULT NULL,
  PRIMARY KEY (`id_aeronave`))
ENGINE = InnoDB
AUTO_INCREMENT = 748
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `dw_projeto`.`descricao_tipo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dw_projeto`.`descricao_tipo` (
  `id_descricao_tipo` INT NOT NULL AUTO_INCREMENT,
  `descricao_do_tipo` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`id_descricao_tipo`),
  UNIQUE INDEX `descricao_do_tipo` (`descricao_do_tipo` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 25
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `dw_projeto`.`locais`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dw_projeto`.`locais` (
  `id_local` INT NOT NULL AUTO_INCREMENT,
  `municipio` VARCHAR(100) NULL DEFAULT NULL,
  `uf` VARCHAR(20) NULL DEFAULT NULL,
  PRIMARY KEY (`id_local`))
ENGINE = InnoDB
AUTO_INCREMENT = 1068
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `dw_projeto`.`ocorrencias`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dw_projeto`.`ocorrencias` (
  `id_ocorrencia` INT NOT NULL AUTO_INCREMENT,
  `numero_da_ocorrencia` INT NULL DEFAULT NULL,
  `data_da_ocorrencia` DATE NULL DEFAULT NULL,
  `id_aeronave` INT NULL DEFAULT NULL,
  `id_descricao_tipo` INT NULL DEFAULT NULL,
  `id_local` INT NULL DEFAULT NULL,
  `locais_id_local` INT NOT NULL,
  `descricao_tipo_id_descricao_tipo` INT NOT NULL,
  `aeronaves_id_aeronave` INT NOT NULL,
  PRIMARY KEY (`id_ocorrencia`),
  UNIQUE INDEX `numero_da_ocorrencia` (`numero_da_ocorrencia` ASC) VISIBLE,
  INDEX `fk_ocorrencias_locais_idx` (`locais_id_local` ASC) VISIBLE,
  INDEX `fk_ocorrencias_descricao_tipo1_idx` (`descricao_tipo_id_descricao_tipo` ASC) VISIBLE,
  INDEX `fk_ocorrencias_aeronaves1_idx` (`aeronaves_id_aeronave` ASC) VISIBLE,
  CONSTRAINT `fk_ocorrencias_locais`
    FOREIGN KEY (`locais_id_local`)
    REFERENCES `dw_projeto`.`locais` (`id_local`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ocorrencias_descricao_tipo1`
    FOREIGN KEY (`descricao_tipo_id_descricao_tipo`)
    REFERENCES `dw_projeto`.`descricao_tipo` (`id_descricao_tipo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ocorrencias_aeronaves1`
    FOREIGN KEY (`aeronaves_id_aeronave`)
    REFERENCES `dw_projeto`.`aeronaves` (`id_aeronave`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 3091
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
