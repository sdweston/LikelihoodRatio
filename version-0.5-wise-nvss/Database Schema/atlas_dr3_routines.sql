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
-- Temporary table structure for view `elais_distribution`
--

DROP TABLE IF EXISTS `elais_distribution`;
/*!50001 DROP VIEW IF EXISTS `elais_distribution`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `elais_distribution` (
  `cid` char(8),
  `n_cid` bigint(21)
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `cdfs_ozdes`
--

DROP TABLE IF EXISTS `cdfs_ozdes`;
/*!50001 DROP VIEW IF EXISTS `cdfs_ozdes`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `cdfs_ozdes` (
  `ID` varchar(30),
  `RA` double,
  `DECL` double,
  `z` float,
  `z_Err` float,
  `flag` varchar(4),
  `source` varchar(20),
  `comments` varchar(30)
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `ozdes_cdfs`
--

DROP TABLE IF EXISTS `ozdes_cdfs`;
/*!50001 DROP VIEW IF EXISTS `ozdes_cdfs`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `ozdes_cdfs` (
  `id` bigint(20),
  `ra` double,
  `decl` double
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `elais_ozdes`
--

DROP TABLE IF EXISTS `elais_ozdes`;
/*!50001 DROP VIEW IF EXISTS `elais_ozdes`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `elais_ozdes` (
  `ID` varchar(30),
  `RA` double,
  `DECL` double,
  `z` float,
  `z_Err` float,
  `flag` varchar(4),
  `source` varchar(20),
  `comments` varchar(30)
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `cdfs_rel`
--

DROP TABLE IF EXISTS `cdfs_rel`;
/*!50001 DROP VIEW IF EXISTS `cdfs_rel`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `cdfs_rel` (
  `ATLAS_ID` char(8),
  `swire_index_spitzer` int(11),
  `Reliability` decimal(28,9)
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `ozdes_elais`
--

DROP TABLE IF EXISTS `ozdes_elais`;
/*!50001 DROP VIEW IF EXISTS `ozdes_elais`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `ozdes_elais` (
  `id` bigint(20),
  `ra` double,
  `decl` double
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `elais_rel`
--

DROP TABLE IF EXISTS `elais_rel`;
/*!50001 DROP VIEW IF EXISTS `elais_rel`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `elais_rel` (
  `ATLAS_ID` char(8),
  `swire_index_spitzer` int(11),
  `Reliability` decimal(28,9)
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `cdfs_distribution`
--

DROP TABLE IF EXISTS `cdfs_distribution`;
/*!50001 DROP VIEW IF EXISTS `cdfs_distribution`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `cdfs_distribution` (
  `cid` char(8),
  `n_cid` bigint(21)
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `elais_distribution`
--

/*!50001 DROP TABLE IF EXISTS `elais_distribution`*/;
/*!50001 DROP VIEW IF EXISTS `elais_distribution`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `elais_distribution` AS select `elais_matches`.`cid` AS `cid`,count(`elais_matches`.`cid`) AS `n_cid` from `elais_matches` group by `elais_matches`.`cid` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `cdfs_ozdes`
--

/*!50001 DROP TABLE IF EXISTS `cdfs_ozdes`*/;
/*!50001 DROP VIEW IF EXISTS `cdfs_ozdes`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`atlas`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `cdfs_ozdes` AS select `ozdes`.`ID` AS `ID`,`ozdes`.`RA` AS `RA`,`ozdes`.`DECL` AS `DECL`,`ozdes`.`z` AS `z`,`ozdes`.`z_Err` AS `z_Err`,`ozdes`.`flag` AS `flag`,`ozdes`.`source` AS `source`,`ozdes`.`comments` AS `comments` from `ozdes` where ((`ozdes`.`RA` > 51.474385) and (`ozdes`.`RA` < 54.023942) and (`ozdes`.`DECL` > -(28.941196)) and (`ozdes`.`DECL` < -(27.213252))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `ozdes_cdfs`
--

/*!50001 DROP TABLE IF EXISTS `ozdes_cdfs`*/;
/*!50001 DROP VIEW IF EXISTS `ozdes_cdfs`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`atlas`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `ozdes_cdfs` AS select `ozdes_c1`.`id` AS `id`,`ozdes_c1`.`ra` AS `ra`,`ozdes_c1`.`decl` AS `decl` from `ozdes_c1` union all select `ozdes_c2`.`id` AS `id`,`ozdes_c2`.`ra` AS `ra`,`ozdes_c2`.`decl` AS `decl` from `ozdes_c2` union all select `ozdes_c3`.`id` AS `id`,`ozdes_c3`.`ra` AS `ra`,`ozdes_c3`.`decl` AS `decl` from `ozdes_c3` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `elais_ozdes`
--

/*!50001 DROP TABLE IF EXISTS `elais_ozdes`*/;
/*!50001 DROP VIEW IF EXISTS `elais_ozdes`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`atlas`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `elais_ozdes` AS select `ozdes`.`ID` AS `ID`,`ozdes`.`RA` AS `RA`,`ozdes`.`DECL` AS `DECL`,`ozdes`.`z` AS `z`,`ozdes`.`z_Err` AS `z_Err`,`ozdes`.`flag` AS `flag`,`ozdes`.`source` AS `source`,`ozdes`.`comments` AS `comments` from `ozdes` where ((`ozdes`.`RA` < 9.77962) and (`ozdes`.`RA` > 7.357132) and (`ozdes`.`DECL` < -(42.899883)) and (`ozdes`.`DECL` > -(44.601035))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `cdfs_rel`
--

/*!50001 DROP TABLE IF EXISTS `cdfs_rel`*/;
/*!50001 DROP VIEW IF EXISTS `cdfs_rel`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`atlas`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `cdfs_rel` AS select `t1`.`cid` AS `ATLAS_ID`,`t1`.`swire_index_spitzer` AS `swire_index_spitzer`,max(`t1`.`reliability`) AS `Reliability` from `cdfs_matches` `t1` group by `t1`.`cid` order by max(`t1`.`reliability`) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `ozdes_elais`
--

/*!50001 DROP TABLE IF EXISTS `ozdes_elais`*/;
/*!50001 DROP VIEW IF EXISTS `ozdes_elais`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`atlas`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `ozdes_elais` AS select `ozdes_e1`.`id` AS `id`,`ozdes_e1`.`ra` AS `ra`,`ozdes_e1`.`decl` AS `decl` from `ozdes_e1` union all select `ozdes_e2`.`id` AS `id`,`ozdes_e2`.`ra` AS `ra`,`ozdes_e2`.`decl` AS `decl` from `ozdes_e2` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `elais_rel`
--

/*!50001 DROP TABLE IF EXISTS `elais_rel`*/;
/*!50001 DROP VIEW IF EXISTS `elais_rel`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`atlas`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `elais_rel` AS select `t1`.`cid` AS `ATLAS_ID`,`t1`.`swire_index_spitzer` AS `swire_index_spitzer`,max(`t1`.`reliability`) AS `Reliability` from `elais_matches` `t1` group by `t1`.`cid` order by max(`t1`.`reliability`) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `cdfs_distribution`
--

/*!50001 DROP TABLE IF EXISTS `cdfs_distribution`*/;
/*!50001 DROP VIEW IF EXISTS `cdfs_distribution`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `cdfs_distribution` AS select `cdfs_matches`.`cid` AS `cid`,count(`cdfs_matches`.`cid`) AS `n_cid` from `cdfs_matches` group by `cdfs_matches`.`cid` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-12-01 18:56:17
