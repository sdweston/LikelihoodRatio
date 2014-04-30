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
-- Table structure for table `elais_cmpcat`
--

DROP TABLE IF EXISTS `elais_cmpcat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `elais_cmpcat` (
  `ID` varchar(8) NOT NULL COMMENT 'Component identification number',
  `Survey` varchar(6) DEFAULT NULL,
  `Name` varchar(20) DEFAULT NULL COMMENT 'Full catalogue name',
  `RA` double NOT NULL COMMENT 'Right Ascension (degrees, J2000)',
  `DECL` double DEFAULT NULL COMMENT 'Declination (degrees, J2000)',
  `RA_ERR` double DEFAULT NULL COMMENT 'Error in right ascension (arcsec)',
  `DECL_ERR` double DEFAULT NULL COMMENT 'Error in declination (arcsec)',
  `SNR` float DEFAULT NULL COMMENT 'signal-to-noise ratio of raw dectection',
  `RMS` float DEFAULT NULL COMMENT 'local rms noise level (mJy/beam)',
  `BWS` float DEFAULT NULL COMMENT 'local bandwidth smearing value',
  `Sp` float DEFAULT NULL COMMENT 'Fitted source peak (mJy/beam)',
  `Sp_ERR` float DEFAULT NULL COMMENT 'Error in fitted source peak (mJy/beam)',
  `SInt` float DEFAULT NULL COMMENT 'Integrated flux density (mJy)',
  `SInt_ERR` float DEFAULT NULL COMMENT 'Error in integrated flux density (mJy)',
  `DECONV` float DEFAULT NULL COMMENT 'Deconvolved angular size (arcsec)',
  `DECONV_ERR` float DEFAULT NULL COMMENT 'Error in deconvolved angular size (arcsec)',
  `V` float DEFAULT NULL COMMENT 'Visibility area',
  `OBS_FREQ` float DEFAULT NULL COMMENT 'Frequency at which the peak and integrated flux was measured (MHz)',
  `SINDEX` float DEFAULT NULL COMMENT 'Spectral index of source between 1400 and 1710 MHz',
  `SINDEX_ERR` float DEFAULT NULL COMMENT 'Error on spectral index',
  PRIMARY KEY (`ID`),
  KEY `idx_id` (`ID`),
  KEY `idx_ra` (`RA`),
  KEY `idx_dec` (`DECL`)
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

-- Dump completed on 2014-03-31  9:15:01
