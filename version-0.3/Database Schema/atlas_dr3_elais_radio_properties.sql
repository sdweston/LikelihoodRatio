CREATE DATABASE  IF NOT EXISTS `atlas_dr3` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `atlas_dr3`;
-- MySQL dump 10.13  Distrib 5.6.12, for Win64 (x86_64)
--
-- Host: localhost    Database: atlas_dr3
-- ------------------------------------------------------
-- Server version	5.6.12-log

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
-- Table structure for table `elais_radio_properties`
--

DROP TABLE IF EXISTS `elais_radio_properties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `elais_radio_properties` (
  `id` varchar(8) NOT NULL COMMENT 'Component identification number',
  `snr` float DEFAULT NULL COMMENT 'signal-to-noise ratio of raw dectection',
  `rms` float DEFAULT NULL COMMENT 'local rms noise level (mJy/beam)',
  `bws` float DEFAULT NULL COMMENT 'local bandwidth smearing value',
  `sp` float DEFAULT NULL COMMENT 'Fitted source peak (mJy/beam)',
  `sp_err` float DEFAULT NULL COMMENT 'Error in fitted source peak (mJy/beam)',
  `sint` float DEFAULT NULL COMMENT 'Integrated flux density (mJy)',
  `sint_err` float DEFAULT NULL COMMENT 'Error in integrated flux density (mJy)',
  `obs_freq` float DEFAULT NULL COMMENT 'Frequency at which the peak and integrated flux was measured (MHz)',
  PRIMARY KEY (`id`)
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

-- Dump completed on 2014-01-27 15:21:38
