/*
SQLyog Professional v12.09 (64 bit)
MySQL - 10.1.30-MariaDB : Database - csneasc3
*********************************************************************
*/


/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`csneasc5` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `csneasc5`;

/*Parent Loopup Tables*/

/*Will drop table if it already exists, this measn new changes will be applied without having to create new database*/
DROP TABLE IF EXISTS `Gender`;
/*Table is named 'Gender' and the field 'Gender' and 'GenderID'
so that the same value can be uinserted later into the MySQL query within the main program without the need to have multiple values for the table name and the two different fields,
To achive 'GenderID' within python a concatination of 'table' eg 'Gender' and 'ID' is made*/
CREATE TABLE `Gender` (
  /*'AUTO_INCREMENT' is used to generate a serial number for the ID field*/
  `GenderID` int(11) NOT NULL AUTO_INCREMENT,
  `Gender` varchar(80) NOT NULL,
  /*Keys must be declared*/
  PRIMARY KEY (`GenderID`)
  /*More detailed settings*/
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `Country`;
CREATE TABLE `Country` (
  `CountryID` int(11) NOT NULL AUTO_INCREMENT,
  `Country` varchar(80) NOT NULL,
  PRIMARY KEY (`CountryID`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `Eth`;
CREATE TABLE `Eth` (
  `EthID` int(11) NOT NULL AUTO_INCREMENT,
  `Eth` varchar(80) NOT NULL,
  PRIMARY KEY (`EthID`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `Lan`;
CREATE TABLE `Lan` (
  `LanID` int(11) NOT NULL AUTO_INCREMENT,
  `Lan` varchar(80) NOT NULL,
  PRIMARY KEY (`LanID`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

/*Child for Parent Loopup Tables*/
DROP TABLE IF EXISTS `User`;
CREATE TABLE `User` (
  `UserID` INT(11) NOT NULL AUTO_INCREMENT,
  `Username` VARCHAR(40) NOT NULL,
  `Password` VARCHAR(50) NOT NULL,
  `FirstName` VARCHAR(80) DEFAULT NULL,
  `LastName` VARCHAR(80) DEFAULT NULL,
  `GenderID` INT(11) DEFAULT 1,
  `CountryID` INT(11) DEFAULT 1,
  `EthID` INT(11) DEFAULT 1,
  `LanID` INT(11) DEFAULT 1,
  `Age` INT(11) DEFAULT NULL,
  `Bio` VARCHAR(500) DEFAULT NULL,
  PRIMARY KEY (`UserID`),
  /*Keys are their relashionships are declared*/
  FOREIGN KEY (`GenderID`) REFERENCES `Gender`(`GenderID`),
  FOREIGN KEY (`CountryID`) REFERENCES `Country`(`CountryID`),
  FOREIGN KEY (`EthID`) REFERENCES `Eth`(`EthID`),
  FOREIGN KEY (`LanID`) REFERENCES `Lan`(`LanID`),
  /*Constraints insure thge integrity of the database
  For exmapel there shouldn't be two users with the same 'Username'*/
  CONSTRAINT UC_User UNIQUE (`Username`)
) ENGINE=INNODB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

/*More Tables*/

DROP TABLE IF EXISTS `Match`;
CREATE TABLE `Match` (
  `MatchID` int(11) NOT NULL UNIQUE AUTO_INCREMENT,
  `FromID` int(11) NOT NULL,
  `ToID` int(11) NOT NULL,
  `State` int(11) NOT NULL,
  PRIMARY KEY (`MatchID`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `Message`;
CREATE TABLE `Message` (
  `MessageID` int(11) NOT NULL AUTO_INCREMENT,
  `FromID` int(11) NOT NULL,
  `ToID` int(11) NOT NULL,
  `Message` char(200) NOT NULL,
  PRIMARY KEY (`MessageID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
