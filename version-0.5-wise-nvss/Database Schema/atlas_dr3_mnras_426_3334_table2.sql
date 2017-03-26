CREATE DATABASE  IF NOT EXISTS `atlas_dr3` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `atlas_dr3`;
-- MySQL dump 10.13  Distrib 5.5.16, for Win32 (x86)
--
-- Host: localhost    Database: atlas_dr3
-- ------------------------------------------------------
-- Server version	5.5.28-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `mnras_426_3334_table2`
--

DROP TABLE IF EXISTS `mnras_426_3334_table2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mnras_426_3334_table2` (
  `RAJ2000` double DEFAULT NULL,
  `DEJ2000` double DEFAULT NULL,
  `recno` int(11) NOT NULL DEFAULT '0',
  `SID` varchar(7) DEFAULT NULL,
  `M` smallint(6) DEFAULT NULL,
  `char_RAJ2000` varchar(11) DEFAULT NULL,
  `char_DEJ2000` varchar(11) DEFAULT NULL,
  `S20` float DEFAULT NULL,
  `R_mag` float DEFAULT NULL,
  `Bmag` float DEFAULT NULL,
  `z` float DEFAULT NULL,
  `Class` varchar(5) DEFAULT NULL,
  `RMAG` float DEFAULT NULL,
  `logL` float DEFAULT NULL,
  `SimbadName` varchar(14) DEFAULT NULL,
  `mnras_426_3334_table2col` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`recno`),
  KEY `idx_ra` (`RAJ2000`),
  KEY `idx_dec` (`DEJ2000`),
  KEY `idx_sid` (`SID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-12-01 18:55:37
