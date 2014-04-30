CREATE DATABASE  IF NOT EXISTS `swire_cdfs` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `swire_cdfs`;
-- MySQL dump 10.13  Distrib 5.5.16, for Win32 (x86)
--
-- Host: localhost    Database: swire_cdfs
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
-- Table structure for table `swire`
--

DROP TABLE IF EXISTS `swire`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `swire` (
  `Index_Spitzer` int(11) DEFAULT NULL,
  `RA_Spitzer` double DEFAULT NULL,
  `Dec_Spitzer` double DEFAULT NULL,
  `Index_MIPS_24_micron` int(11) DEFAULT NULL,
  `RA_MIPS_24_micron` double DEFAULT NULL,
  `Dec_MIPS_24_micron` double DEFAULT NULL,
  `Index_MIPS_70_micron` smallint(6) DEFAULT NULL,
  `RA_MIPS_70_micron` double DEFAULT NULL,
  `Dec_MIPS_70_micron` double DEFAULT NULL,
  `Index_MIPS_160_micron` smallint(6) DEFAULT NULL,
  `RA_MIPS_160_micron` double DEFAULT NULL,
  `Dec_MIPS_160_micron` double DEFAULT NULL,
  `Index_UV_GALEX` bigint(20) DEFAULT NULL,
  `RA_UV_GALEX` double DEFAULT NULL,
  `Dec_UV_GALEX` double DEFAULT NULL,
  `Index_Optical_SDSS` smallint(6) DEFAULT NULL,
  `RA_Optical_SDSS` double DEFAULT NULL,
  `Dec_Optical_SDSS` double DEFAULT NULL,
  `Index_Optical_Extra` int(11) DEFAULT NULL,
  `RA_Optical_Extra` double DEFAULT NULL,
  `Dec_Optical_Extra` double DEFAULT NULL,
  `Index_NIR_2MASS` int(11) DEFAULT NULL,
  `RA_NIR_2MASS` double DEFAULT NULL,
  `Dec_NIR_2MASS` double DEFAULT NULL,
  `Index_NIR_Extra` smallint(6) DEFAULT NULL,
  `RA_NIR_Extra` double DEFAULT NULL,
  `Dec_NIR_Extra` double DEFAULT NULL,
  `FUV_AB_mag_GALEX` float DEFAULT NULL,
  `NUV_AB_mag_GALEX` float DEFAULT NULL,
  `FUV_AB_mag_Error_GALEX` float DEFAULT NULL,
  `NUV_AB_mag_Error_GALEX` float DEFAULT NULL,
  `u_AB_mag_SDSS` float DEFAULT NULL,
  `g_AB_mag_SDSS` float DEFAULT NULL,
  `r_AB_mag_SDSS` float DEFAULT NULL,
  `i_AB_mag_SDSS` float DEFAULT NULL,
  `z_AB_mag_SDSS` float DEFAULT NULL,
  `u_AB_mag_Error_SDSS` float DEFAULT NULL,
  `g_AB_mag_Error_SDSS` float DEFAULT NULL,
  `r_AB_mag_Error_SDSS` float DEFAULT NULL,
  `i_AB_mag_Error_SDSS` float DEFAULT NULL,
  `z_AB_mag_Error_SDSS` float DEFAULT NULL,
  `u_AB_mag_Extra` float DEFAULT NULL,
  `g_AB_mag_Extra` float DEFAULT NULL,
  `r_AB_mag_Extra` float DEFAULT NULL,
  `i_AB_mag_Extra` float DEFAULT NULL,
  `z_AB_mag_Extra` float DEFAULT NULL,
  `u_AB_mag_Error_Extra` float DEFAULT NULL,
  `g_AB_mag_Error_Extra` float DEFAULT NULL,
  `r_AB_mag_Error_Extra` double DEFAULT NULL,
  `i_AB_mag_Error_Extra` double DEFAULT NULL,
  `z_AB_mag_Error_Extra` float DEFAULT NULL,
  `J_Vega_mag_2MASS` float DEFAULT NULL,
  `H_Vega_mag_2MASS` float DEFAULT NULL,
  `K_Vega_mag_2MASS` float DEFAULT NULL,
  `J_Vega_mag_Error_2MASS` float DEFAULT NULL,
  `H_Vega_mag_Error_2MASS` float DEFAULT NULL,
  `K_Vega_mag_Error_2MASS` float DEFAULT NULL,
  `J_Vega_mag_Extra` float DEFAULT NULL,
  `H_Vega_mag_Extra` float DEFAULT NULL,
  `K_Vega_mag_Extra` float DEFAULT NULL,
  `J_Vega_mag_Error_Extra` float DEFAULT NULL,
  `H_Vega_mag_Error_Extra` float DEFAULT NULL,
  `K_Vega_mag_Error_Extra` float DEFAULT NULL,
  `IRAC_3_6_micron_Flux_muJy` double DEFAULT NULL,
  `IRAC_4_5_micron_Flux_muJy` double DEFAULT NULL,
  `IRAC_5_8_micron_Flux_muJy` double DEFAULT NULL,
  `IRAC_8_0_micron_Flux_muJy` double DEFAULT NULL,
  `IRAC_3_6_micron_Flux_Error_muJy` double DEFAULT NULL,
  `IRAC_4_5_micron_Flux_Error_muJy` double DEFAULT NULL,
  `IRAC_5_8_micron_Flux_Error_muJy` double DEFAULT NULL,
  `IRAC_8_0_micron_Flux_Error_muJy` double DEFAULT NULL,
  `IRAC_3_6_micron_SNR` double DEFAULT NULL,
  `IRAC_4_5_micron_SNR` double DEFAULT NULL,
  `IRAC_5_8_micron_SNR` double DEFAULT NULL,
  `IRAC_8_0_micron_SNR` double DEFAULT NULL,
  `MIPS_24_micron_Flux_muJy` double DEFAULT NULL,
  `MIPS_24_micron_Flux_Error_muJy` float DEFAULT NULL,
  `MIPS_24_micron_SNR` double DEFAULT NULL,
  `MIPS_24_micron_vs_IRAC_dist_arcsec` double DEFAULT NULL,
  `MIPS_24_micron_Reliability` double DEFAULT NULL,
  `MIPS_70_micron_Flux_mJy` double DEFAULT NULL,
  `MIPS_70_micron_Flux_Error_mJy` float DEFAULT NULL,
  `MIPS_70_micron_SNR` double DEFAULT NULL,
  `MIPS_70_micron_vs_MIPS_24_micron_dist_arcsec` double DEFAULT NULL,
  `MIPS_70_micron_Reliability` double DEFAULT NULL,
  `MIPS_160_micron_Flux_mJy` double DEFAULT NULL,
  `MIPS_160_micron_Flux_Error_mJy` float DEFAULT NULL,
  `MIPS_160_micron_SNR` float DEFAULT NULL,
  `MIPS_160_micron_vs_MIPS_24_micron_dist_arcsec` double DEFAULT NULL,
  `MIPS_160_micron_Reliability` double DEFAULT NULL,
  `Redshift` float DEFAULT NULL,
  `Redshift_Error` float DEFAULT NULL,
  `Redshift_Flag` smallint(6) DEFAULT NULL,
  `SDSS_Photometric_Redshift_z1` float DEFAULT NULL,
  `SDSS_Photometric_Redshift_z2d1` float DEFAULT NULL,
  `SDSS_Photometric_Redshift_z2cc2` float DEFAULT NULL,
  `SDSS_Spectroscopic_Redshift` float DEFAULT NULL,
  `NED_Spectroscopic_Redshift` float DEFAULT NULL,
  `SDSS_Photometric_Redshift_Error_z1` float DEFAULT NULL,
  `SDSS_Photometric_Redshift_Error_z2d1` float DEFAULT NULL,
  `SDSS_Photometric_Redshift_Error_z2cc2` float DEFAULT NULL,
  `SDSS_Spectroscopic_Redshift_Error` float DEFAULT NULL,
  `NED_Spectroscopic_Redshift_Error` float DEFAULT NULL,
  `SDSS_stype_Flag` smallint(6) DEFAULT NULL,
  `SDSS_zconf_Flag` smallint(6) DEFAULT NULL,
  `SDSS_zstatus_Flag` smallint(6) DEFAULT NULL,
  `SDSS_specclass_Flag` smallint(6) DEFAULT NULL,
  `Spitzer_Catalog_Reliability_Flag` smallint(6) DEFAULT NULL
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

-- Dump completed on 2014-04-07 13:27:58
