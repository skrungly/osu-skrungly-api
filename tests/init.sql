-- MySQL dump 10.13  Distrib 9.3.0, for Linux (x86_64)
--
-- Host: localhost    Database: bancho
-- ------------------------------------------------------
-- Server version	9.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `achievements`
--

DROP TABLE IF EXISTS `achievements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `achievements` (
  `id` int NOT NULL AUTO_INCREMENT,
  `file` varchar(128) NOT NULL,
  `name` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `desc` varchar(256) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `cond` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `achievements_desc_uindex` (`desc`),
  UNIQUE KEY `achievements_file_uindex` (`file`),
  UNIQUE KEY `achievements_name_uindex` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=84 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `achievements`
--

LOCK TABLES `achievements` WRITE;
/*!40000 ALTER TABLE `achievements` DISABLE KEYS */;
INSERT INTO `achievements` VALUES (1,'osu-skill-pass-1','Rising Star','Can\'t go forward without the first steps.','(score.mods & 1 == 0) and 1 <= score.sr < 2 and mode_vn == 0'),(2,'osu-skill-pass-2','Constellation Prize','Definitely not a consolation prize. Now things start getting hard!','(score.mods & 1 == 0) and 2 <= score.sr < 3 and mode_vn == 0'),(3,'osu-skill-pass-3','Building Confidence','Oh, you\'ve SO got this.','(score.mods & 1 == 0) and 3 <= score.sr < 4 and mode_vn == 0'),(4,'osu-skill-pass-4','Insanity Approaches','You\'re not twitching, you\'re just ready.','(score.mods & 1 == 0) and 4 <= score.sr < 5 and mode_vn == 0'),(5,'osu-skill-pass-5','These Clarion Skies','Everything seems so clear now.','(score.mods & 1 == 0) and 5 <= score.sr < 6 and mode_vn == 0'),(6,'osu-skill-pass-6','Above and Beyond','A cut above the rest.','(score.mods & 1 == 0) and 6 <= score.sr < 7 and mode_vn == 0'),(7,'osu-skill-pass-7','Supremacy','All marvel before your prowess.','(score.mods & 1 == 0) and 7 <= score.sr < 8 and mode_vn == 0'),(8,'osu-skill-pass-8','Absolution','My god, you\'re full of stars!','(score.mods & 1 == 0) and 8 <= score.sr < 9 and mode_vn == 0'),(9,'osu-skill-pass-9','Event Horizon','No force dares to pull you under.','(score.mods & 1 == 0) and 9 <= score.sr < 10 and mode_vn == 0'),(10,'osu-skill-pass-10','Phantasm','Fevered is your passion, extraordinary is your skill.','(score.mods & 1 == 0) and 10 <= score.sr < 11 and mode_vn == 0'),(11,'osu-skill-fc-1','Totality','All the notes. Every single one.','score.perfect and 1 <= score.sr < 2 and mode_vn == 0'),(12,'osu-skill-fc-2','Business As Usual','Two to go, please.','score.perfect and 2 <= score.sr < 3 and mode_vn == 0'),(13,'osu-skill-fc-3','Building Steam','Hey, this isn\'t so bad.','score.perfect and 3 <= score.sr < 4 and mode_vn == 0'),(14,'osu-skill-fc-4','Moving Forward','Bet you feel good about that.','score.perfect and 4 <= score.sr < 5 and mode_vn == 0'),(15,'osu-skill-fc-5','Paradigm Shift','Surprisingly difficult.','score.perfect and 5 <= score.sr < 6 and mode_vn == 0'),(16,'osu-skill-fc-6','Anguish Quelled','Don\'t choke.','score.perfect and 6 <= score.sr < 7 and mode_vn == 0'),(17,'osu-skill-fc-7','Never Give Up','Excellence is its own reward.','score.perfect and 7 <= score.sr < 8 and mode_vn == 0'),(18,'osu-skill-fc-8','Aberration','They said it couldn\'t be done. They were wrong.','score.perfect and 8 <= score.sr < 9 and mode_vn == 0'),(19,'osu-skill-fc-9','Chosen','Reign among the Prometheans, where you belong.','score.perfect and 9 <= score.sr < 10 and mode_vn == 0'),(20,'osu-skill-fc-10','Unfathomable','You have no equal.','score.perfect and 10 <= score.sr < 11 and mode_vn == 0'),(21,'osu-combo-500','500 Combo','500 big ones! You\'re moving up in the world!','500 <= score.max_combo < 750 and mode_vn == 0'),(22,'osu-combo-750','750 Combo','750 notes back to back? Woah.','750 <= score.max_combo < 1000 and mode_vn == 0'),(23,'osu-combo-1000','1000 Combo','A thousand reasons why you rock at this game.','1000 <= score.max_combo < 2000 and mode_vn == 0'),(24,'osu-combo-2000','2000 Combo','Nothing can stop you now.','2000 <= score.max_combo and mode_vn == 0'),(25,'taiko-skill-pass-1','My First Don','Marching to the beat of your own drum. Literally.','(score.mods & 1 == 0) and 1 <= score.sr < 2 and mode_vn == 1'),(26,'taiko-skill-pass-2','Katsu Katsu Katsu','Hora! Izuko!','(score.mods & 1 == 0) and 2 <= score.sr < 3 and mode_vn == 1'),(27,'taiko-skill-pass-3','Not Even Trying','Muzukashii? Not even.','(score.mods & 1 == 0) and 3 <= score.sr < 4 and mode_vn == 1'),(28,'taiko-skill-pass-4','Face Your Demons','The first trials are now behind you, but are you a match for the Oni?','(score.mods & 1 == 0) and 4 <= score.sr < 5 and mode_vn == 1'),(29,'taiko-skill-pass-5','The Demon Within','No rest for the wicked.','(score.mods & 1 == 0) and 5 <= score.sr < 6 and mode_vn == 1'),(30,'taiko-skill-pass-6','Drumbreaker','Too strong.','(score.mods & 1 == 0) and 6 <= score.sr < 7 and mode_vn == 1'),(31,'taiko-skill-pass-7','The Godfather','You are the Don of Dons.','(score.mods & 1 == 0) and 7 <= score.sr < 8 and mode_vn == 1'),(32,'taiko-skill-pass-8','Rhythm Incarnate','Feel the beat. Become the beat.','(score.mods & 1 == 0) and 8 <= score.sr < 9 and mode_vn == 1'),(33,'taiko-skill-fc-1','Keeping Time','Don, then katsu. Don, then katsu..','score.perfect and 1 <= score.sr < 2 and mode_vn == 1'),(34,'taiko-skill-fc-2','To Your Own Beat','Straight and steady.','score.perfect and 2 <= score.sr < 3 and mode_vn == 1'),(35,'taiko-skill-fc-3','Big Drums','Bigger scores to match.','score.perfect and 3 <= score.sr < 4 and mode_vn == 1'),(36,'taiko-skill-fc-4','Adversity Overcome','Difficult? Not for you.','score.perfect and 4 <= score.sr < 5 and mode_vn == 1'),(37,'taiko-skill-fc-5','Demonslayer','An Oni felled forevermore.','score.perfect and 5 <= score.sr < 6 and mode_vn == 1'),(38,'taiko-skill-fc-6','Rhythm\'s Call','Heralding true skill.','score.perfect and 6 <= score.sr < 7 and mode_vn == 1'),(39,'taiko-skill-fc-7','Time Everlasting','Not a single beat escapes you.','score.perfect and 7 <= score.sr < 8 and mode_vn == 1'),(40,'taiko-skill-fc-8','The Drummer\'s Throne','Percussive brilliance befitting royalty alone.','score.perfect and 8 <= score.sr < 9 and mode_vn == 1'),(41,'fruits-skill-pass-1','A Slice Of Life','Hey, this fruit catching business isn\'t bad.','(score.mods & 1 == 0) and 1 <= score.sr < 2 and mode_vn == 2'),(42,'fruits-skill-pass-2','Dashing Ever Forward','Fast is how you do it.','(score.mods & 1 == 0) and 2 <= score.sr < 3 and mode_vn == 2'),(43,'fruits-skill-pass-3','Zesty Disposition','No scurvy for you, not with that much fruit.','(score.mods & 1 == 0) and 3 <= score.sr < 4 and mode_vn == 2'),(44,'fruits-skill-pass-4','Hyperdash ON!','Time and distance is no obstacle to you.','(score.mods & 1 == 0) and 4 <= score.sr < 5 and mode_vn == 2'),(45,'fruits-skill-pass-5','It\'s Raining Fruit','And you can catch them all.','(score.mods & 1 == 0) and 5 <= score.sr < 6 and mode_vn == 2'),(46,'fruits-skill-pass-6','Fruit Ninja','Legendary techniques.','(score.mods & 1 == 0) and 6 <= score.sr < 7 and mode_vn == 2'),(47,'fruits-skill-pass-7','Dreamcatcher','No fruit, only dreams now.','(score.mods & 1 == 0) and 7 <= score.sr < 8 and mode_vn == 2'),(48,'fruits-skill-pass-8','Lord of the Catch','Your kingdom kneels before you.','(score.mods & 1 == 0) and 8 <= score.sr < 9 and mode_vn == 2'),(49,'fruits-skill-fc-1','Sweet And Sour','Apples and oranges, literally.','score.perfect and 1 <= score.sr < 2 and mode_vn == 2'),(50,'fruits-skill-fc-2','Reaching The Core','The seeds of future success.','score.perfect and 2 <= score.sr < 3 and mode_vn == 2'),(51,'fruits-skill-fc-3','Clean Platter','Clean only of failure. It is completely full, otherwise.','score.perfect and 3 <= score.sr < 4 and mode_vn == 2'),(52,'fruits-skill-fc-4','Between The Rain','No umbrella needed.','score.perfect and 4 <= score.sr < 5 and mode_vn == 2'),(53,'fruits-skill-fc-5','Addicted','That was an overdose?','score.perfect and 5 <= score.sr < 6 and mode_vn == 2'),(54,'fruits-skill-fc-6','Quickening','A dash above normal limits.','score.perfect and 6 <= score.sr < 7 and mode_vn == 2'),(55,'fruits-skill-fc-7','Supersonic','Faster than is reasonably necessary.','score.perfect and 7 <= score.sr < 8 and mode_vn == 2'),(56,'fruits-skill-fc-8','Dashing Scarlet','Speed beyond mortal reckoning.','score.perfect and 8 <= score.sr < 9 and mode_vn == 2'),(57,'mania-skill-pass-1','First Steps','It isn\'t 9-to-5, but 1-to-9. Keys, that is.','(score.mods & 1 == 0) and 1 <= score.sr < 2 and mode_vn == 3'),(58,'mania-skill-pass-2','No Normal Player','Not anymore, at least.','(score.mods & 1 == 0) and 2 <= score.sr < 3 and mode_vn == 3'),(59,'mania-skill-pass-3','Impulse Drive','Not quite hyperspeed, but getting close.','(score.mods & 1 == 0) and 3 <= score.sr < 4 and mode_vn == 3'),(60,'mania-skill-pass-4','Hyperspeed','Woah.','(score.mods & 1 == 0) and 4 <= score.sr < 5 and mode_vn == 3'),(61,'mania-skill-pass-5','Ever Onwards','Another challenge is just around the corner.','(score.mods & 1 == 0) and 5 <= score.sr < 6 and mode_vn == 3'),(62,'mania-skill-pass-6','Another Surpassed','Is there no limit to your skills?','(score.mods & 1 == 0) and 6 <= score.sr < 7 and mode_vn == 3'),(63,'mania-skill-pass-7','Extra Credit','See me after class.','(score.mods & 1 == 0) and 7 <= score.sr < 8 and mode_vn == 3'),(64,'mania-skill-pass-8','Maniac','There\'s just no stopping you.','(score.mods & 1 == 0) and 8 <= score.sr < 9 and mode_vn == 3'),(65,'mania-skill-fc-1','Keystruck','The beginning of a new story','score.perfect and 1 <= score.sr < 2 and mode_vn == 3'),(66,'mania-skill-fc-2','Keying In','Finding your groove.','score.perfect and 2 <= score.sr < 3 and mode_vn == 3'),(67,'mania-skill-fc-3','Hyperflow','You can *feel* the rhythm.','score.perfect and 3 <= score.sr < 4 and mode_vn == 3'),(68,'mania-skill-fc-4','Breakthrough','Many skills mastered, rolled into one.','score.perfect and 4 <= score.sr < 5 and mode_vn == 3'),(69,'mania-skill-fc-5','Everything Extra','Giving your all is giving everything you have.','score.perfect and 5 <= score.sr < 6 and mode_vn == 3'),(70,'mania-skill-fc-6','Level Breaker','Finesse beyond reason','score.perfect and 6 <= score.sr < 7 and mode_vn == 3'),(71,'mania-skill-fc-7','Step Up','A precipice rarely seen.','score.perfect and 7 <= score.sr < 8 and mode_vn == 3'),(72,'mania-skill-fc-8','Behind The Veil','Supernatural!','score.perfect and 8 <= score.sr < 9 and mode_vn == 3'),(73,'all-intro-suddendeath','Finality','High stakes, no regrets.','score.mods == 32'),(74,'all-intro-hidden','Blindsight','I can see just perfectly','score.mods & 8'),(75,'all-intro-perfect','Perfectionist','Accept nothing but the best.','score.mods & 16384'),(76,'all-intro-hardrock','Rock Around The Clock','You can\'t stop the rock.','score.mods & 16'),(77,'all-intro-doubletime','Time And A Half','Having a right ol\' time. One and a half of them, almost.','score.mods & 64'),(78,'all-intro-flashlight','Are You Afraid Of The Dark?','Harder than it looks, probably because it\'s hard to look.','score.mods & 1024'),(79,'all-intro-easy','Dial It Right Back','Sometimes you just want to take it easy.','score.mods & 2'),(80,'all-intro-nofail','Risk Averse','Safety nets are fun!','score.mods & 1'),(81,'all-intro-nightcore','Sweet Rave Party','Founded in the fine tradition of changing things that were just fine as they were.','score.mods & 512'),(82,'all-intro-halftime','Slowboat','You got there. Eventually.','score.mods & 256'),(83,'all-intro-spunout','Burned Out','One cannot always spin to win.','score.mods & 4096');
/*!40000 ALTER TABLE `achievements` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `channels`
--

DROP TABLE IF EXISTS `channels`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `channels` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `topic` varchar(256) NOT NULL,
  `read_priv` int NOT NULL DEFAULT '1',
  `write_priv` int NOT NULL DEFAULT '2',
  `auto_join` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `channels_name_uindex` (`name`),
  KEY `channels_auto_join_index` (`auto_join`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `channels`
--

LOCK TABLES `channels` WRITE;
/*!40000 ALTER TABLE `channels` DISABLE KEYS */;
INSERT INTO `channels` VALUES (1,'#osu','General discussion.',1,2,1),(2,'#announce','Exemplary performance and public announcements.',1,24576,1),(3,'#lobby','Multiplayer lobby discussion room.',1,2,0),(4,'#supporter','General discussion for supporters.',48,48,0),(5,'#staff','General discussion for staff members.',28672,28672,1),(6,'#admin','General discussion for administrators.',24576,24576,1),(7,'#dev','General discussion for developers.',16384,16384,1);
/*!40000 ALTER TABLE `channels` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clans`
--

DROP TABLE IF EXISTS `clans`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clans` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(16) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `tag` varchar(6) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `owner` int NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `clans_name_uindex` (`name`),
  UNIQUE KEY `clans_owner_uindex` (`owner`),
  UNIQUE KEY `clans_tag_uindex` (`tag`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clans`
--

LOCK TABLES `clans` WRITE;
/*!40000 ALTER TABLE `clans` DISABLE KEYS */;
/*!40000 ALTER TABLE `clans` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `client_hashes`
--

DROP TABLE IF EXISTS `client_hashes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `client_hashes` (
  `userid` int NOT NULL,
  `osupath` char(32) NOT NULL,
  `adapters` char(32) NOT NULL,
  `uninstall_id` char(32) NOT NULL,
  `disk_serial` char(32) NOT NULL,
  `latest_time` datetime NOT NULL,
  `occurrences` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`userid`,`osupath`,`adapters`,`uninstall_id`,`disk_serial`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `client_hashes`
--

LOCK TABLES `client_hashes` WRITE;
/*!40000 ALTER TABLE `client_hashes` DISABLE KEYS */;
INSERT INTO `client_hashes` VALUES (3,'260c4ab94f72cb9dabc8970af4a13842','b4ec3c4334a0249dae95c284ec5983df','f6fa33fc9504b83ce642a26d3ff85abf','ac6884115296283f1bb3d9ae53830207','2025-06-01 20:58:20',5),(4,'260c4ab94f72cb9dabc8970af4a13842','b4ec3c4334a0249dae95c284ec5983df','4bc5a97fd1c8dbe58d2ad56ed5449e7e','8ea2bca1e2d33bca38483563d11a7cfe','2025-05-31 14:16:10',2),(4,'260c4ab94f72cb9dabc8970af4a13842','b4ec3c4334a0249dae95c284ec5983df','f6fa33fc9504b83ce642a26d3ff85abf','ac6884115296283f1bb3d9ae53830207','2025-05-31 13:31:57',2);
/*!40000 ALTER TABLE `client_hashes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comments`
--

DROP TABLE IF EXISTS `comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `target_id` int NOT NULL COMMENT 'replay, map, or set id',
  `target_type` enum('replay','map','song') NOT NULL,
  `userid` int NOT NULL,
  `time` int NOT NULL,
  `comment` varchar(80) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `colour` char(6) DEFAULT NULL COMMENT 'rgb hex string',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comments`
--

LOCK TABLES `comments` WRITE;
/*!40000 ALTER TABLE `comments` DISABLE KEYS */;
/*!40000 ALTER TABLE `comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `favourites`
--

DROP TABLE IF EXISTS `favourites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `favourites` (
  `userid` int NOT NULL,
  `setid` int NOT NULL,
  `created_at` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`userid`,`setid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `favourites`
--

LOCK TABLES `favourites` WRITE;
/*!40000 ALTER TABLE `favourites` DISABLE KEYS */;
/*!40000 ALTER TABLE `favourites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ingame_logins`
--

DROP TABLE IF EXISTS `ingame_logins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ingame_logins` (
  `id` int NOT NULL AUTO_INCREMENT,
  `userid` int NOT NULL,
  `ip` varchar(45) NOT NULL COMMENT 'maxlen for ipv6',
  `osu_ver` date NOT NULL,
  `osu_stream` varchar(11) NOT NULL,
  `datetime` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ingame_logins`
--

LOCK TABLES `ingame_logins` WRITE;
/*!40000 ALTER TABLE `ingame_logins` DISABLE KEYS */;
INSERT INTO `ingame_logins` VALUES (1,3,'92.23.164.98','2025-04-01','stable','2025-05-31 13:13:16'),(2,4,'92.23.164.98','2025-04-01','stable','2025-05-31 13:30:41'),(3,4,'92.23.164.98','2025-04-01','stable','2025-05-31 13:31:57'),(4,3,'92.23.164.98','2025-04-01','stable','2025-05-31 13:44:15'),(5,4,'92.23.164.98','2025-04-01','stable','2025-05-31 14:08:37'),(6,3,'92.23.164.98','2025-04-01','stable','2025-05-31 14:12:25'),(7,4,'92.23.164.98','2025-04-01','stable','2025-05-31 14:16:10'),(8,3,'92.23.164.98','2025-04-01','stable','2025-06-01 20:28:30'),(9,3,'92.23.164.98','2025-04-01','stable','2025-06-01 20:58:20');
/*!40000 ALTER TABLE `ingame_logins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `logs`
--

DROP TABLE IF EXISTS `logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `from` int NOT NULL COMMENT 'both from and to are playerids',
  `to` int NOT NULL,
  `action` varchar(32) NOT NULL,
  `msg` varchar(2048) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `time` datetime NOT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logs`
--

LOCK TABLES `logs` WRITE;
/*!40000 ALTER TABLE `logs` DISABLE KEYS */;
/*!40000 ALTER TABLE `logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mail`
--

DROP TABLE IF EXISTS `mail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mail` (
  `id` int NOT NULL AUTO_INCREMENT,
  `from_id` int NOT NULL,
  `to_id` int NOT NULL,
  `msg` varchar(2048) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `time` int DEFAULT NULL,
  `read` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mail`
--

LOCK TABLES `mail` WRITE;
/*!40000 ALTER TABLE `mail` DISABLE KEYS */;
INSERT INTO `mail` VALUES (1,4,3,'hiiiiiiiiii',1748700595,1),(2,3,4,'hi!',1748701005,0);
/*!40000 ALTER TABLE `mail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `map_requests`
--

DROP TABLE IF EXISTS `map_requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `map_requests` (
  `id` int NOT NULL AUTO_INCREMENT,
  `map_id` int NOT NULL,
  `player_id` int NOT NULL,
  `datetime` datetime NOT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `map_requests`
--

LOCK TABLES `map_requests` WRITE;
/*!40000 ALTER TABLE `map_requests` DISABLE KEYS */;
/*!40000 ALTER TABLE `map_requests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `maps`
--

DROP TABLE IF EXISTS `maps`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `maps` (
  `server` enum('osu!','private') NOT NULL DEFAULT 'osu!',
  `id` int NOT NULL,
  `set_id` int NOT NULL,
  `status` int NOT NULL,
  `md5` char(32) NOT NULL,
  `artist` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `title` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `version` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `creator` varchar(19) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `filename` varchar(256) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `last_update` datetime NOT NULL,
  `total_length` int NOT NULL,
  `max_combo` int NOT NULL,
  `frozen` tinyint(1) NOT NULL DEFAULT '0',
  `plays` int NOT NULL DEFAULT '0',
  `passes` int NOT NULL DEFAULT '0',
  `mode` tinyint(1) NOT NULL DEFAULT '0',
  `bpm` float(12,2) NOT NULL DEFAULT '0.00',
  `cs` float(4,2) NOT NULL DEFAULT '0.00',
  `ar` float(4,2) NOT NULL DEFAULT '0.00',
  `od` float(4,2) NOT NULL DEFAULT '0.00',
  `hp` float(4,2) NOT NULL DEFAULT '0.00',
  `diff` float(6,3) NOT NULL DEFAULT '0.000',
  PRIMARY KEY (`server`,`id`),
  UNIQUE KEY `maps_id_uindex` (`id`),
  UNIQUE KEY `maps_md5_uindex` (`md5`),
  KEY `maps_set_id_index` (`set_id`),
  KEY `maps_status_index` (`status`),
  KEY `maps_filename_index` (`filename`),
  KEY `maps_plays_index` (`plays`),
  KEY `maps_mode_index` (`mode`),
  KEY `maps_frozen_index` (`frozen`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maps`
--

LOCK TABLES `maps` WRITE;
/*!40000 ALTER TABLE `maps` DISABLE KEYS */;
INSERT INTO `maps` VALUES ('osu!',148756,48045,2,'e0f619f9610eab1fb16e9832e24eb2e7','Subplaid','Only time makes your happiness','Insane','grumd','Subplaid - Only time makes your happiness (grumd) [Insane].osu','2012-05-01 09:34:06',125,664,0,2,1,0,170.00,4.00,9.00,8.00,8.00,4.524),('osu!',148878,48045,2,'cf3881e6a74509fa5b3c88e667016c97','Subplaid','Only time makes your happiness','Hard','grumd','Subplaid - Only time makes your happiness (grumd) [Hard].osu','2012-05-01 09:34:06',124,559,0,0,0,0,170.00,4.00,8.00,7.00,6.00,2.787),('osu!',149639,48045,2,'445d69d26ccd4eb1192ee0b6a51a875e','Subplaid','Only time makes your happiness','Normal','grumd','Subplaid - Only time makes your happiness (grumd) [Normal].osu','2012-05-01 09:34:06',125,306,0,0,0,0,170.00,3.00,6.00,5.00,5.00,1.751),('osu!',149859,48045,2,'3c8703d6cfb4f6007acf3d4a5ea73af6','Subplaid','Only time makes your happiness','Odaril\'s Taiko Oni','grumd','Subplaid - Only time makes your happiness (grumd) [Odaril\'s Taiko Oni].osu','2012-05-01 09:34:06',125,717,0,0,0,1,170.00,4.00,5.00,5.00,7.00,4.351),('osu!',150309,48045,2,'457de6b5fbbdd13254f25491c03c46fe','Subplaid','Only time makes your happiness','Ryuu\'s Easy','grumd','Subplaid - Only time makes your happiness (grumd) [Ryuu\'s Easy].osu','2012-05-01 09:34:06',125,227,0,0,0,0,170.00,3.00,2.00,1.00,1.00,1.179),('osu!',152078,49052,3,'12e14d24b09da2dc7b067dfd11497b69','goreshit','the nature of dying','The Nature of Dying','grumd','goreshit - the nature of dying (grumd) [The Nature of Dying].osu','2012-06-26 15:35:21',322,1932,0,2,1,0,171.00,4.00,9.00,8.00,7.00,4.604),('osu!',159866,49052,3,'34edeba37fa8dd3de3debcf967453c75','goreshit','the nature of dying','Loctav\'s Taiko','grumd','goreshit - the nature of dying (grumd) [Loctav\'s Taiko].osu','2012-06-26 15:35:21',321,1898,0,0,0,1,171.00,5.00,5.00,5.00,4.00,5.295),('osu!',356979,143513,2,'569b38948f80975b101347af5e2d715d','DJ Sharpnel','We Luv Lama','LV18','sergioperez','DJ Sharpnel - We Luv Lama (sergioperez) [LV18].osu','2014-01-18 22:27:44',322,3282,1,0,0,3,210.00,4.00,5.00,5.00,6.00,3.386),('osu!',811675,370340,2,'f8483b44ffbbc86603f486aad3ceaa0d','CENOB1TE','Onslaught','apoplexy_','Irreversible','CENOB1TE - Onslaught (Irreversible) [apoplexy_].osu','2015-10-26 19:35:41',199,1002,0,5,2,0,140.00,4.00,9.30,8.50,7.00,5.989),('osu!',811676,370340,2,'04b61d6e2c97caa6ee7505e97ebeb39b','CENOB1TE','Onslaught','easy_','Irreversible','CENOB1TE - Onslaught (Irreversible) [easy_].osu','2015-10-26 19:35:41',199,311,0,0,0,0,140.00,2.50,3.50,3.00,3.00,1.574),('osu!',811677,370340,2,'1f02818fe1aa90aff70ea9994fe7bc81','CENOB1TE','Onslaught','inverness-hard_','Irreversible','CENOB1TE - Onslaught (Irreversible) [inverness-hard_].osu','2015-10-26 19:35:41',199,705,0,0,0,0,140.00,4.00,8.00,7.00,5.00,3.778),('osu!',811678,370340,2,'126043fb4c5ff72452ed8213f1e98e66','CENOB1TE','Onslaught','kyversible-insane_','Irreversible','CENOB1TE - Onslaught (Irreversible) [kyversible-insane_].osu','2015-10-26 19:35:41',199,914,0,0,0,0,140.00,4.00,9.00,8.00,6.00,4.931),('osu!',811679,370340,2,'65dbdbfee87516af302fc5763c155b12','CENOB1TE','Onslaught','wendao-normal_','Irreversible','CENOB1TE - Onslaught (Irreversible) [wendao-normal_].osu','2015-10-26 19:35:41',199,464,0,0,0,0,140.00,3.20,6.00,5.50,4.20,2.055),('osu!',921164,426638,2,'160f21a1d338ac8096730614dada122f','LeaF','I','Limbo','Tidek','LeaF - I (Tidek) [Limbo].osu','2017-07-02 16:34:07',154,2879,0,0,0,3,280.00,4.00,5.00,9.00,9.40,5.921),('osu!',922576,426638,2,'39304d56cbae4887c01f70fa8c9b444b','LeaF','I','Black Another','Tidek','LeaF - I (Tidek) [Black Another].osu','2017-07-02 16:34:07',154,2608,0,0,0,3,280.00,4.00,5.00,8.50,9.00,4.929),('osu!',923925,426638,2,'7ebf4550820c6ecbbfcb3f87d6ed47d4','LeaF','I','_UJ\'s Easy','Tidek','LeaF - I (Tidek) [_UJ\'s Easy].osu','2017-07-02 16:34:07',154,880,0,0,0,3,280.00,4.00,5.00,7.00,7.50,1.444),('osu!',928340,426638,2,'261d2c5f8df5412928b355ba0fc2e7e1','LeaF','I','Normal','Tidek','LeaF - I (Tidek) [Normal].osu','2017-07-02 16:34:07',154,1373,0,0,0,3,280.00,4.00,5.00,7.50,8.00,2.236),('osu!',928341,426638,2,'349bf615e127756ffba33911c3e13079','LeaF','I','_UJ\'s Another','Tidek','LeaF - I (Tidek) [_UJ\'s Another].osu','2017-07-02 16:34:07',154,2180,0,0,0,3,280.00,4.00,5.00,8.50,8.50,4.148),('osu!',934351,433476,0,'8e5b112c905e4e1995b1a54f621c0e68','SAVE THE QUEEN','EX-Termination','EX-Plosion','ShiraKai','SAVE THE QUEEN - EX-Termination (ShiraKai) [EX-Plosion].osu','2016-05-15 11:04:58',179,1214,0,0,0,0,256.00,3.60,9.60,7.60,6.60,5.722),('osu!',964146,426638,2,'bd1cf09e3be2c4a413b21b0e22c10917','LeaF','I','Hyper','Tidek','LeaF - I (Tidek) [Hyper].osu','2017-07-02 16:34:07',154,1684,0,1,1,3,280.00,4.00,5.00,8.00,8.00,3.247),('osu!',1236466,584467,0,'781e1bfe2835de1dec0530b10d36774a','DJ Sharpnel','Exciting Hyper Highspeed Star','Hyperspeed','kingdom5500','DJ Sharpnel - Exciting Hyper Highspeed Star (kingdom5500) [Hyperspeed].osu','2017-03-11 22:25:01',105,674,0,0,0,0,180.15,4.20,9.20,7.60,7.20,4.723),('osu!',1617033,768965,0,'b341ea3cc0c37171230e9226287627fc','Shiraishi','Koukakukidou','4K Another','Snow Note','Shiraishi - Koukakukidou (Snow Note) [4K Another].osu','2018-06-21 15:38:01',122,1849,0,0,0,3,176.00,4.00,5.00,8.00,9.40,4.673),('osu!',1683185,768965,0,'0e33817e21eb3caff2328a98450f62ba','Shiraishi','Koukakukidou','Lv.20 Assault X Auto-SC','Snow Note','Shiraishi - Koukakukidou (Snow Note) [Lv.20 Assault X Auto-SC].osu','2018-06-21 15:38:01',122,2933,0,0,0,3,176.00,7.00,5.00,7.00,9.40,6.877),('osu!',1683186,768965,0,'244dd91d7934838461686ae53963276f','Shiraishi','Koukakukidou','Lv.20 Assault X','Snow Note','Shiraishi - Koukakukidou (Snow Note) [Lv.20 Assault X].osu','2018-06-21 15:38:01',122,3000,0,0,0,3,176.00,8.00,5.00,7.00,9.40,7.018),('osu!',2321255,1110961,2,'a71bd0c33adafafd04a9833437d3e089','ginkiha','Paved Garden','Collab Insane','Leader','ginkiha - Paved Garden (Leader) [Collab Insane].osu','2020-03-01 11:16:27',93,557,0,2,2,0,187.00,4.00,9.00,8.00,7.00,5.038),('osu!',2321256,1110961,2,'a03233d2ba67194c968e3fee908af445','ginkiha','Paved Garden','Easy','Leader','ginkiha - Paved Garden (Leader) [Easy].osu','2020-03-01 11:16:27',90,203,0,0,0,0,187.00,3.00,3.00,3.00,3.00,1.686),('osu!',2321257,1110961,2,'632e3d28451ba562cb53d0d0d0fc26a3','ginkiha','Paved Garden','Extra','Leader','ginkiha - Paved Garden (Leader) [Extra].osu','2020-03-01 11:16:27',93,593,0,0,0,0,187.00,4.20,9.40,8.60,7.00,6.112),('osu!',2321258,1110961,2,'7f29cdce5ccbaf10b0bfc4be898f3979','ginkiha','Paved Garden','Hard','Leader','ginkiha - Paved Garden (Leader) [Hard].osu','2020-03-01 11:16:27',92,502,0,0,0,0,187.00,3.80,8.00,6.00,6.00,3.807),('osu!',2321259,1110961,2,'2b43b2a9c46d4246ec40b85bfa63f16f','ginkiha','Paved Garden','lfj\'s Extra','Leader','ginkiha - Paved Garden (Leader) [lfj\'s Extra].osu','2020-03-01 11:16:27',93,654,0,0,0,0,187.00,4.00,9.30,8.30,6.50,5.671),('osu!',2321260,1110961,2,'87cd73ba159c27f4fb026a81f9c2440c','ginkiha','Paved Garden','Normal','Leader','ginkiha - Paved Garden (Leader) [Normal].osu','2020-03-01 11:16:27',92,308,0,0,0,0,187.00,3.50,6.00,4.00,5.00,2.725),('osu!',2322544,1111618,5,'bc3a33d32926764639cac6254874f7dc','Polyphia','The Worst','Terrible 1.1x','Cokii-','Polyphia - The Worst (Cokii-) [Terrible 1.1x].osu','2022-11-02 19:02:56',210,2468,0,0,0,3,137.50,4.00,5.00,8.00,8.00,4.233),('osu!',2322545,1111618,5,'8bf5ff961335afdd3de253606409b9b3','Polyphia','The Worst','Terrible 1.2x','Cokii-','Polyphia - The Worst (Cokii-) [Terrible 1.2x].osu','2022-11-02 19:02:56',193,2467,0,0,0,3,150.00,4.00,5.00,8.00,8.00,4.527),('osu!',2322546,1111618,5,'80041c736549274566d403494ffcc0cf','Polyphia','The Worst','Terrible 1.3x','Cokii-','Polyphia - The Worst (Cokii-) [Terrible 1.3x].osu','2022-11-02 19:02:56',178,2454,0,0,0,3,162.50,4.00,5.00,8.00,8.00,4.849),('osu!',2322547,1111618,5,'7264beb969a22440f0a0112451f2d10d','Polyphia','The Worst','Terrible 1.4x','Cokii-','Polyphia - The Worst (Cokii-) [Terrible 1.4x].osu','2022-11-02 19:02:56',165,2448,0,0,0,3,175.00,4.00,5.00,8.00,8.00,5.161),('osu!',2322548,1111618,5,'d4c215dbb01c1f0009bd286e1f245e5f','Polyphia','The Worst','Terrible','Cokii-','Polyphia - The Worst (Cokii-) [Terrible].osu','2022-11-02 19:02:56',231,2486,0,2,1,3,125.00,4.00,5.00,8.00,8.00,3.911),('osu!',3673018,1792369,2,'9995dcb5758d9596a8a1262c2ccccbc1','KOCHO','Hanyamaru Manten, Zenitendou. (TV Size)','4K Easy','fvrex','KOCHO - Hanyamaru Manten, Zenitendou. (TV Size) (fvrex) [4K Easy].osu','2023-04-11 03:40:49',31,155,0,0,0,3,139.50,4.00,5.00,6.50,6.50,1.195),('osu!',3673019,1792369,2,'95587c900ea841bedba58c62eb25c7cc','KOCHO','Hanyamaru Manten, Zenitendou. (TV Size)','Ucitysm\'s 4K Hard','fvrex','KOCHO - Hanyamaru Manten, Zenitendou. (TV Size) (fvrex) [Ucitysm\'s 4K Hard].osu','2023-04-11 03:40:49',31,401,0,0,0,3,139.50,4.00,5.00,7.50,7.50,2.219),('osu!',3673020,1792369,2,'44e9ef445220a68c8d1a0edefb7608a3','KOCHO','Hanyamaru Manten, Zenitendou. (TV Size)','4K Normal','fvrex','KOCHO - Hanyamaru Manten, Zenitendou. (TV Size) (fvrex) [4K Normal].osu','2023-04-11 03:40:49',31,200,0,0,0,3,139.50,4.00,5.00,7.00,7.00,1.870),('osu!',3673021,1792369,2,'2f15179a06a188011c40f7b94a3041b1','KOCHO','Hanyamaru Manten, Zenitendou. (TV Size)','4K Purr','fvrex','KOCHO - Hanyamaru Manten, Zenitendou. (TV Size) (fvrex) [4K Purr].osu','2023-04-11 03:40:49',31,477,0,1,1,3,139.50,4.00,5.00,8.00,8.00,2.902),('osu!',3673022,1792369,2,'8ef0554d72826489e7c03161e5688bdf','KOCHO','Hanyamaru Manten, Zenitendou. (TV Size)','5K Easy','fvrex','KOCHO - Hanyamaru Manten, Zenitendou. (TV Size) (fvrex) [5K Easy].osu','2023-04-11 03:40:49',31,158,0,0,0,3,139.50,5.00,5.00,6.50,6.50,1.132),('osu!',3673023,1792369,2,'01f0220d45f61274cde5caa2d19731e7','KOCHO','Hanyamaru Manten, Zenitendou. (TV Size)','5K Hard','fvrex','KOCHO - Hanyamaru Manten, Zenitendou. (TV Size) (fvrex) [5K Hard].osu','2023-04-11 03:40:49',31,340,0,0,0,3,139.50,5.00,5.00,7.50,7.50,2.271),('osu!',3673025,1792369,2,'b194f25900f86a55f0809278ba831407','KOCHO','Hanyamaru Manten, Zenitendou. (TV Size)','Ucitysm\'s 5K Normal','fvrex','KOCHO - Hanyamaru Manten, Zenitendou. (TV Size) (fvrex) [Ucitysm\'s 5K Normal].osu','2023-04-11 03:40:49',31,219,0,0,0,3,139.50,5.00,5.00,7.00,7.00,1.559),('osu!',3673026,1792369,2,'609b645046755638b75067229b377fbe','KOCHO','Hanyamaru Manten, Zenitendou. (TV Size)','6K Easy','fvrex','KOCHO - Hanyamaru Manten, Zenitendou. (TV Size) (fvrex) [6K Easy].osu','2023-04-11 03:40:49',31,152,0,0,0,3,139.50,6.00,5.00,6.50,6.50,1.122),('osu!',3673027,1792369,2,'12f4f291f3e76a63dee2cf75f9971b12','KOCHO','Hanyamaru Manten, Zenitendou. (TV Size)','6K Hard','fvrex','KOCHO - Hanyamaru Manten, Zenitendou. (TV Size) (fvrex) [6K Hard].osu','2023-04-11 03:40:49',31,337,0,0,0,3,139.50,6.00,5.00,7.50,7.50,2.280),('osu!',3673028,1792369,2,'ff883b1363b233ffe9926bc4c111cce1','KOCHO','Hanyamaru Manten, Zenitendou. (TV Size)','6K Baby Tiger','fvrex','KOCHO - Hanyamaru Manten, Zenitendou. (TV Size) (fvrex) [6K Baby Tiger].osu','2023-04-11 03:40:49',31,369,0,0,0,3,139.50,6.00,5.00,8.00,8.00,2.940),('osu!',3673029,1792369,2,'c80172c6fdd2c32ab0b7ccf887094a58','KOCHO','Hanyamaru Manten, Zenitendou. (TV Size)','6K Normal','fvrex','KOCHO - Hanyamaru Manten, Zenitendou. (TV Size) (fvrex) [6K Normal].osu','2023-04-11 03:40:49',31,222,0,0,0,3,139.50,6.00,5.00,7.00,7.00,1.729),('osu!',3673030,1792369,2,'ef6e77a3c6f40c514e52dd6ecfce2835','KOCHO','Hanyamaru Manten, Zenitendou. (TV Size)','7K Silent\'s Easy','fvrex','KOCHO - Hanyamaru Manten, Zenitendou. (TV Size) (fvrex) [7K Silent\'s Easy].osu','2023-04-11 03:40:49',31,159,0,0,0,3,139.50,7.00,5.00,6.50,6.50,1.115),('osu!',3673031,1792369,2,'907e141afe6aacb3a4686480db0f1f70','KOCHO','Hanyamaru Manten, Zenitendou. (TV Size)','Ham\'s 7K Hard','fvrex','KOCHO - Hanyamaru Manten, Zenitendou. (TV Size) (fvrex) [Ham\'s 7K Hard].osu','2023-04-11 03:40:49',31,416,0,0,0,3,139.50,7.00,5.00,7.50,7.50,2.642),('osu!',3673032,1792369,2,'0391405398bf1eca1447b0f4831360f5','KOCHO','Hanyamaru Manten, Zenitendou. (TV Size)','Ham\'s 7K Normal','fvrex','KOCHO - Hanyamaru Manten, Zenitendou. (TV Size) (fvrex) [Ham\'s 7K Normal].osu','2023-04-11 03:40:49',31,291,0,0,0,3,139.50,7.00,5.00,7.00,7.00,1.921),('osu!',3673033,1792369,2,'71951092e218cc85cf99101bff110ed5','KOCHO','Hanyamaru Manten, Zenitendou. (TV Size)','7K Pspspsp','fvrex','KOCHO - Hanyamaru Manten, Zenitendou. (TV Size) (fvrex) [7K Pspspsp].osu','2023-04-11 03:40:49',31,481,0,0,0,3,139.50,7.00,5.00,8.00,8.00,3.326),('osu!',3972153,1924071,2,'a39791b023b5c4205f9dd65ee9bcc911','Ardolf','Lycanthrope','Hard','Ucitysm','Ardolf - Lycanthrope (Ucitysm) [Hard].osu','2023-08-20 03:09:53',157,1557,0,0,0,3,185.00,4.00,5.00,7.50,7.50,2.792),('osu!',3972154,1924071,2,'e02cfc38e2423dae7af8a253d6cf981f','Ardolf','Lycanthrope','Himitsu\'s Easy','Ucitysm','Ardolf - Lycanthrope (Ucitysm) [Himitsu\'s Easy].osu','2023-08-20 03:09:53',157,835,0,0,0,3,185.00,4.00,5.00,6.50,6.50,1.569),('osu!',3972155,1924071,2,'1c925074dc47441e71b5197a25809db3','Ardolf','Lycanthrope','Insane','Ucitysm','Ardolf - Lycanthrope (Ucitysm) [Insane].osu','2023-08-20 03:09:53',157,1680,0,0,0,3,185.00,4.00,5.00,8.00,8.00,3.487),('osu!',3972156,1924071,2,'9e3f65ba19d88a9cab128ca42b2ad3ad','Ardolf','Lycanthrope','Johno\'s Normal','Ucitysm','Ardolf - Lycanthrope (Ucitysm) [Johno\'s Normal].osu','2023-08-20 03:09:53',157,1197,0,0,0,3,185.00,4.00,5.00,7.00,7.00,1.925),('osu!',3972157,1924071,2,'86d7d95971c68f9ab252692c1e2e4dbe','Ardolf','Lycanthrope','Hytex\'s Livid','Ucitysm','Ardolf - Lycanthrope (Ucitysm) [Hytex\'s Livid].osu','2023-08-20 03:09:53',157,1881,0,2,2,3,185.00,4.00,5.00,8.50,8.50,4.186),('osu!',4036879,1924071,2,'f2c32083d4196259e21ee4458b3c6ae7','Ardolf','Lycanthrope','Polarin\'s Hyper','Ucitysm','Ardolf - Lycanthrope (Ucitysm) [Polarin\'s Hyper].osu','2023-08-20 03:09:53',157,1545,0,0,0,3,185.00,4.00,5.00,7.70,7.70,3.133),('osu!',4050726,1792369,2,'95ac8a05c05235b3f3cf6d92ac6db71a','KOCHO','Hanyamaru Manten, Zenitendou. (TV Size)','MJH\'s 5K Meow','fvrex','KOCHO - Hanyamaru Manten, Zenitendou. (TV Size) (fvrex) [MJH\'s 5K Meow].osu','2023-04-11 03:40:49',31,588,0,0,0,3,139.50,5.00,5.00,8.00,8.00,3.196),('osu!',4281105,2050247,2,'68395cfbde3befe2b0b48f8cd87a28e0','Mitchie M','Tokugawa Cup Noodle Kinshirei','Hard','skrungly','Mitchie M - Tokugawa Cup Noodle Kinshirei (skrungly) [Hard].osu','2023-11-24 18:50:47',124,1481,1,1,1,3,178.00,4.00,5.00,7.50,6.50,2.642),('osu!',4281495,2050247,2,'5e30e3b0e3f3e5fc41ed6678a7bdec05','Mitchie M','Tokugawa Cup Noodle Kinshirei','Normal','skrungly','Mitchie M - Tokugawa Cup Noodle Kinshirei (skrungly) [Normal].osu','2023-11-24 18:50:47',124,1081,1,0,0,3,178.00,4.00,5.00,6.50,5.50,1.837);
/*!40000 ALTER TABLE `maps` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mapsets`
--

DROP TABLE IF EXISTS `mapsets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mapsets` (
  `server` enum('osu!','private') NOT NULL DEFAULT 'osu!',
  `id` int NOT NULL,
  `last_osuapi_check` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`server`,`id`),
  UNIQUE KEY `nmapsets_id_uindex` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mapsets`
--

LOCK TABLES `mapsets` WRITE;
/*!40000 ALTER TABLE `mapsets` DISABLE KEYS */;
INSERT INTO `mapsets` VALUES ('osu!',48045,'2025-05-31 13:13:17'),('osu!',49052,'2025-06-01 20:28:31'),('osu!',143513,'2025-06-01 20:48:35'),('osu!',370340,'2025-05-31 13:43:43'),('osu!',426638,'2025-05-31 13:33:14'),('osu!',433476,'2025-06-01 20:47:45'),('osu!',584467,'2025-06-01 20:51:14'),('osu!',768965,'2025-06-01 20:53:19'),('osu!',1110961,'2025-05-31 13:15:55'),('osu!',1111618,'2025-06-01 20:37:09'),('osu!',1792369,'2025-05-31 13:31:59'),('osu!',1924071,'2025-05-31 13:35:51'),('osu!',2050247,'2025-06-01 20:42:52');
/*!40000 ALTER TABLE `mapsets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `performance_reports`
--

DROP TABLE IF EXISTS `performance_reports`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `performance_reports` (
  `scoreid` bigint unsigned NOT NULL,
  `mod_mode` enum('vanilla','relax','autopilot') NOT NULL DEFAULT 'vanilla',
  `os` varchar(64) NOT NULL,
  `fullscreen` tinyint(1) NOT NULL,
  `fps_cap` varchar(16) NOT NULL,
  `compatibility` tinyint(1) NOT NULL,
  `version` varchar(16) NOT NULL,
  `start_time` int NOT NULL,
  `end_time` int NOT NULL,
  `frame_count` int NOT NULL,
  `spike_frames` int NOT NULL,
  `aim_rate` int NOT NULL,
  `completion` tinyint(1) NOT NULL,
  `identifier` varchar(128) DEFAULT NULL COMMENT 'really don''t know much about this yet',
  `average_frametime` int NOT NULL,
  PRIMARY KEY (`scoreid`,`mod_mode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `performance_reports`
--

LOCK TABLES `performance_reports` WRITE;
/*!40000 ALTER TABLE `performance_reports` DISABLE KEYS */;
/*!40000 ALTER TABLE `performance_reports` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ratings`
--

DROP TABLE IF EXISTS `ratings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ratings` (
  `userid` int NOT NULL,
  `map_md5` char(32) NOT NULL,
  `rating` tinyint NOT NULL,
  PRIMARY KEY (`userid`,`map_md5`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ratings`
--

LOCK TABLES `ratings` WRITE;
/*!40000 ALTER TABLE `ratings` DISABLE KEYS */;
/*!40000 ALTER TABLE `ratings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `relationships`
--

DROP TABLE IF EXISTS `relationships`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `relationships` (
  `user1` int NOT NULL,
  `user2` int NOT NULL,
  `type` enum('friend','block') NOT NULL,
  PRIMARY KEY (`user1`,`user2`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `relationships`
--

LOCK TABLES `relationships` WRITE;
/*!40000 ALTER TABLE `relationships` DISABLE KEYS */;
INSERT INTO `relationships` VALUES (4,3,'friend');
/*!40000 ALTER TABLE `relationships` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scores`
--

DROP TABLE IF EXISTS `scores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `scores` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `map_md5` char(32) NOT NULL,
  `score` int NOT NULL,
  `pp` float(7,3) NOT NULL,
  `acc` float(6,3) NOT NULL,
  `max_combo` int NOT NULL,
  `mods` int NOT NULL,
  `n300` int NOT NULL,
  `n100` int NOT NULL,
  `n50` int NOT NULL,
  `nmiss` int NOT NULL,
  `ngeki` int NOT NULL,
  `nkatu` int NOT NULL,
  `grade` varchar(2) NOT NULL DEFAULT 'N',
  `status` tinyint NOT NULL,
  `mode` tinyint NOT NULL,
  `play_time` datetime NOT NULL,
  `time_elapsed` int NOT NULL,
  `client_flags` int NOT NULL,
  `userid` int NOT NULL,
  `perfect` tinyint(1) NOT NULL,
  `online_checksum` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `scores_map_md5_index` (`map_md5`),
  KEY `scores_score_index` (`score`),
  KEY `scores_pp_index` (`pp`),
  KEY `scores_mods_index` (`mods`),
  KEY `scores_status_index` (`status`),
  KEY `scores_mode_index` (`mode`),
  KEY `scores_play_time_index` (`play_time`),
  KEY `scores_userid_index` (`userid`),
  KEY `scores_online_checksum_index` (`online_checksum`),
  KEY `scores_fetch_leaderboard_generic_index` (`map_md5`,`status`,`mode`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scores`
--

LOCK TABLES `scores` WRITE;
/*!40000 ALTER TABLE `scores` DISABLE KEYS */;
INSERT INTO `scores` VALUES (1,'e0f619f9610eab1fb16e9832e24eb2e7',8464300,124.700,99.097,664,0,437,6,0,0,64,5,'S',2,0,'2025-05-31 13:15:31',123330,0,3,1,'8aecd89325f13678f989d38366f8360c'),(2,'a71bd0c33adafafd04a9833437d3e089',5277990,85.348,95.470,500,0,365,22,0,3,78,15,'A',2,0,'2025-05-31 13:17:34',97396,0,3,0,'e320e3942febb5e0d376188d1f734ef5'),(3,'2f15179a06a188011c40f7b94a3041b1',974978,69.535,98.874,420,0,76,0,0,0,210,10,'S',2,3,'2025-05-31 13:32:47',37158,0,4,1,'c5b5bdc3b92e14993cf437f72566dfcf'),(4,'bd1cf09e3be2c4a413b21b0e22c10917',862042,151.653,97.008,320,64,430,6,2,13,680,50,'S',2,3,'2025-05-31 13:35:13',110734,0,4,0,'7a15318957ceaa98d11515895ba8d489'),(5,'86d7d95971c68f9ab252692c1e2e4dbe',981370,172.334,99.561,1596,0,372,1,0,1,1355,18,'S',2,3,'2025-05-31 13:38:45',151918,0,4,0,'473f59ef8421203774b782d361146743'),(6,'e0f619f9610eab1fb16e9832e24eb2e7',3799540,87.686,97.835,424,0,298,10,0,0,38,6,'F',0,0,'2025-05-31 13:40:36',80645,0,4,0,'a9c7c24a66edaf5c72f5638cc1bb6557'),(7,'a71bd0c33adafafd04a9833437d3e089',2515700,67.860,97.479,246,0,377,8,3,2,89,4,'A',2,0,'2025-05-31 13:42:36',97336,0,4,0,'ec8273559fa1f488816cb37c8f53b592'),(8,'f8483b44ffbbc86603f486aad3ceaa0d',4632170,38.972,94.293,331,0,611,34,0,15,182,26,'F',0,0,'2025-05-31 13:48:22',196668,0,3,0,'b9cbc878088c103507c97184f7d51853'),(9,'f8483b44ffbbc86603f486aad3ceaa0d',4128400,91.754,97.235,319,0,643,22,1,3,202,17,'A',1,0,'2025-05-31 13:51:30',186855,0,3,0,'8bbb9f6aefda0dafde5d1f67a912e242'),(10,'f8483b44ffbbc86603f486aad3ceaa0d',2433400,132.472,98.377,331,0,301,6,0,1,90,4,'F',0,0,'2025-05-31 13:53:13',104965,0,3,0,'0f079d5bd82961476aea5312bd0bf565'),(11,'f8483b44ffbbc86603f486aad3ceaa0d',1265510,102.402,95.520,249,0,174,11,0,1,36,5,'F',0,0,'2025-05-31 13:54:11',73859,0,3,0,'ba2e190c1569f56ee86ee923e2e97d54'),(12,'f8483b44ffbbc86603f486aad3ceaa0d',8889330,131.299,96.562,597,0,636,30,0,3,198,22,'A',2,0,'2025-05-31 13:57:21',189165,0,3,0,'e324f0e7b1e1d9bde2bf3442b87ccfd7'),(13,'86d7d95971c68f9ab252692c1e2e4dbe',954061,162.943,98.893,1371,8,444,4,0,2,1253,44,'SH',2,3,'2025-05-31 14:04:35',150425,0,3,0,'debf2075f66eeb6a0ab0929463961bd8'),(14,'12e14d24b09da2dc7b067dfd11497b69',1320030,82.573,95.644,250,0,166,7,0,3,22,5,'F',0,0,'2025-06-01 20:29:20',70227,0,3,0,'eccc102817388c4214da578322b11727'),(15,'12e14d24b09da2dc7b067dfd11497b69',69738770,137.277,98.198,1932,0,1224,34,0,0,165,28,'S',2,0,'2025-06-01 20:34:18',297431,0,3,1,'7288178df28b46fa1d8aaa1674e78b5a'),(16,'d4c215dbb01c1f0009bd286e1f245e5f',73974,160.404,98.953,139,0,50,0,0,1,137,3,'F',0,3,'2025-06-01 20:38:00',29573,0,3,0,'f8c222501797a5ec4f5c66496e37b790'),(17,'d4c215dbb01c1f0009bd286e1f245e5f',932173,134.095,98.400,1293,0,648,4,1,6,1621,85,'S',2,3,'2025-06-01 20:41:51',231183,0,3,0,'b06407d386547976c4c7ee22b560af2e'),(18,'68395cfbde3befe2b0b48f8cd87a28e0',991126,59.617,99.962,1476,0,236,0,0,0,648,1,'S',2,3,'2025-06-01 20:45:20',128057,0,3,1,'863f3a903e4a7ccdb38062038633aaad');
/*!40000 ALTER TABLE `scores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `startups`
--

DROP TABLE IF EXISTS `startups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `startups` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ver_major` tinyint NOT NULL,
  `ver_minor` tinyint NOT NULL,
  `ver_micro` tinyint NOT NULL,
  `ver_extra` tinyint NOT NULL,
  `datetime` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `startups`
--

LOCK TABLES `startups` WRITE;
/*!40000 ALTER TABLE `startups` DISABLE KEYS */;
INSERT INTO `startups` VALUES (1,5,2,2,1,'2025-05-31 13:12:09');
/*!40000 ALTER TABLE `startups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stats`
--

DROP TABLE IF EXISTS `stats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stats` (
  `id` int NOT NULL AUTO_INCREMENT,
  `mode` tinyint(1) NOT NULL,
  `tscore` bigint unsigned NOT NULL DEFAULT '0',
  `rscore` bigint unsigned NOT NULL DEFAULT '0',
  `pp` int unsigned NOT NULL DEFAULT '0',
  `plays` int unsigned NOT NULL DEFAULT '0',
  `playtime` int unsigned NOT NULL DEFAULT '0',
  `acc` float(6,3) NOT NULL DEFAULT '0.000',
  `max_combo` int unsigned NOT NULL DEFAULT '0',
  `total_hits` int unsigned NOT NULL DEFAULT '0',
  `replay_views` int unsigned NOT NULL DEFAULT '0',
  `xh_count` int unsigned NOT NULL DEFAULT '0',
  `x_count` int unsigned NOT NULL DEFAULT '0',
  `sh_count` int unsigned NOT NULL DEFAULT '0',
  `s_count` int unsigned NOT NULL DEFAULT '0',
  `a_count` int unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`,`mode`),
  KEY `stats_mode_index` (`mode`),
  KEY `stats_pp_index` (`pp`),
  KEY `stats_tscore_index` (`tscore`),
  KEY `stats_rscore_index` (`rscore`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stats`
--

LOCK TABLES `stats` WRITE;
/*!40000 ALTER TABLE `stats` DISABLE KEYS */;
INSERT INTO `stats` VALUES (1,0,0,0,0,0,0,0.000,0,0,0,0,0,0,0,0),(1,1,0,0,0,0,0,0.000,0,0,0,0,0,0,0,0),(1,2,0,0,0,0,0,0.000,0,0,0,0,0,0,0,0),(1,3,0,0,0,0,0,0.000,0,0,0,0,0,0,0,0),(1,4,0,0,0,0,0,0.000,0,0,0,0,0,0,0,0),(1,5,0,0,0,0,0,0.000,0,0,0,0,0,0,0,0),(1,6,0,0,0,0,0,0.000,0,0,0,0,0,0,0,0),(1,8,0,0,0,0,0,0.000,0,0,0,0,0,0,0,0),(3,0,106149900,92370390,449,9,1335,97.367,1932,4730,0,0,0,0,2,2),(3,1,0,0,0,0,0,0.000,0,0,0,0,0,0,0,0),(3,2,0,0,0,0,0,0.000,0,0,0,0,0,0,0,0),(3,3,2019161,954061,163,3,307,98.893,1371,2820,0,0,0,1,0,0),(3,4,0,0,0,0,0,0.000,0,0,0,0,0,0,0,0),(3,5,0,0,0,0,0,0.000,0,0,0,0,0,0,0,0),(3,6,0,0,0,0,0,0.000,0,0,0,0,0,0,0,0),(3,8,0,0,0,0,0,0.000,0,0,0,0,0,0,0,0),(4,0,7290218,3490678,68,3,214,97.479,0,992,0,0,0,0,0,1),(4,1,0,0,0,0,0,0.000,0,0,0,0,0,0,0,0),(4,2,0,0,0,0,0,0.000,0,0,0,0,0,0,0,0),(4,3,1843412,1843412,380,2,261,98.493,1596,2914,0,0,0,0,2,0),(4,4,0,0,0,0,0,0.000,0,0,0,0,0,0,0,0),(4,5,0,0,0,0,0,0.000,0,0,0,0,0,0,0,0),(4,6,0,0,0,0,0,0.000,0,0,0,0,0,0,0,0),(4,8,0,0,0,0,0,0.000,0,0,0,0,0,0,0,0);
/*!40000 ALTER TABLE `stats` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tourney_pool_maps`
--

DROP TABLE IF EXISTS `tourney_pool_maps`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tourney_pool_maps` (
  `map_id` int NOT NULL,
  `pool_id` int NOT NULL,
  `mods` int NOT NULL,
  `slot` tinyint NOT NULL,
  PRIMARY KEY (`map_id`,`pool_id`),
  KEY `tourney_pool_maps_mods_slot_index` (`mods`,`slot`),
  KEY `tourney_pool_maps_tourney_pools_id_fk` (`pool_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tourney_pool_maps`
--

LOCK TABLES `tourney_pool_maps` WRITE;
/*!40000 ALTER TABLE `tourney_pool_maps` DISABLE KEYS */;
/*!40000 ALTER TABLE `tourney_pool_maps` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tourney_pools`
--

DROP TABLE IF EXISTS `tourney_pools`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tourney_pools` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(16) NOT NULL,
  `created_at` datetime NOT NULL,
  `created_by` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tourney_pools_users_id_fk` (`created_by`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tourney_pools`
--

LOCK TABLES `tourney_pools` WRITE;
/*!40000 ALTER TABLE `tourney_pools` DISABLE KEYS */;
/*!40000 ALTER TABLE `tourney_pools` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_achievements`
--

DROP TABLE IF EXISTS `user_achievements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_achievements` (
  `userid` int NOT NULL,
  `achid` int NOT NULL,
  PRIMARY KEY (`userid`,`achid`),
  KEY `user_achievements_achid_index` (`achid`),
  KEY `user_achievements_userid_index` (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_achievements`
--

LOCK TABLES `user_achievements` WRITE;
/*!40000 ALTER TABLE `user_achievements` DISABLE KEYS */;
INSERT INTO `user_achievements` VALUES (3,4),(3,5),(4,5),(3,6),(3,14),(3,21),(3,23),(4,58),(3,60),(4,60),(4,66),(3,74),(4,77);
/*!40000 ALTER TABLE `user_achievements` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `safe_name` varchar(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `email` varchar(254) NOT NULL,
  `priv` int NOT NULL DEFAULT '1',
  `pw_bcrypt` char(60) NOT NULL,
  `country` char(2) NOT NULL DEFAULT 'xx',
  `silence_end` int NOT NULL DEFAULT '0',
  `donor_end` int NOT NULL DEFAULT '0',
  `creation_time` int NOT NULL DEFAULT '0',
  `latest_activity` int NOT NULL DEFAULT '0',
  `clan_id` int NOT NULL DEFAULT '0',
  `clan_priv` tinyint(1) NOT NULL DEFAULT '0',
  `preferred_mode` int NOT NULL DEFAULT '0',
  `play_style` int NOT NULL DEFAULT '0',
  `custom_badge_name` varchar(16) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `custom_badge_icon` varchar(64) DEFAULT NULL,
  `userpage_content` varchar(2048) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `api_key` char(36) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_email_uindex` (`email`),
  UNIQUE KEY `users_name_uindex` (`name`),
  UNIQUE KEY `users_safe_name_uindex` (`safe_name`),
  UNIQUE KEY `users_api_key_uindex` (`api_key`),
  KEY `users_priv_index` (`priv`),
  KEY `users_clan_id_index` (`clan_id`),
  KEY `users_clan_priv_index` (`clan_priv`),
  KEY `users_country_index` (`country`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'chatot','chatot','chatot@skrungly.dev',1,'_______________________my_cool_bcrypt_______________________','ca',0,0,1748697120,1748697120,0,0,0,0,NULL,NULL,NULL,NULL),(3,'shinx','shinx','shinx@skrungly.dev',31879,'$2b$12$ZlOkGIkpWaFg/wdcjonHNOg1PJVpCb8ePLH4n1qdlDmP2jywNBk4e','gb',0,0,1748697194,1748811533,0,0,0,0,NULL,NULL,'hello!',NULL),(4,'vulpix','vulpix','vulpix@skrungly.dev',3,'$2b$12$M4qbDZBao7vaGKBqSGGnuukTf2hYNVKYKtPbsYy8ON6xUfBjnhF5O','gb',0,0,1748698240,1748700985,0,0,0,0,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-01 20:58:57
