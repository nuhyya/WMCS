-- MySQL dump 10.13  Distrib 8.0.39, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: WCMS
-- ------------------------------------------------------
-- Server version	8.0.39

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `habitat`
--

DROP TABLE IF EXISTS `habitat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `habitat` (
  `habitat_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `area_size` decimal(10,2) DEFAULT NULL,
  `environmental_attributes` text,
  PRIMARY KEY (`habitat_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `habitat`
--

LOCK TABLES `habitat` WRITE;
/*!40000 ALTER TABLE `habitat` DISABLE KEYS */;
INSERT INTO `habitat` VALUES (1,'Sundarbans Core Area','West Bengal',4264.00,'Mangrove forests, saline water'),(2,'Buffer Zone','West Bengal',3000.00,'Mixed forest and human settlements'),(3,'Freshwater Zones','West Bengal',1000.00,'Brackish water rivers, freshwater swamps'),(4,'Protected Areas','West Bengal',2000.00,'Strict no-entry zones'),(5,'Coastal Wetlands','West Bengal',1500.00,'Coastal ecosystems with tidal rivers');
/*!40000 ALTER TABLE `habitat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `health_record`
--

DROP TABLE IF EXISTS `health_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `health_record` (
  `health_record_id` int NOT NULL AUTO_INCREMENT,
  `species_id` int DEFAULT NULL,
  `health_status` varchar(50) DEFAULT NULL,
  `vaccination_status` varchar(50) DEFAULT NULL,
  `date_recorded` date DEFAULT NULL,
  `treatment` varchar(255) DEFAULT NULL,
  `disease` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`health_record_id`),
  KEY `species_id` (`species_id`),
  CONSTRAINT `health_record_ibfk_1` FOREIGN KEY (`species_id`) REFERENCES `species` (`species_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `health_record`
--

LOCK TABLES `health_record` WRITE;
/*!40000 ALTER TABLE `health_record` DISABLE KEYS */;
INSERT INTO `health_record` VALUES (1,1,'Injured','Up-to-date','2024-03-10','Wound care','Poaching injury'),(2,2,'Healthy','N/A','2024-02-20','None','None'),(3,3,'Sick','Pending','2024-04-25','Antibiotics','Infection'),(4,4,'Healthy','Up-to-date','2024-01-15','None','None'),(5,5,'Critical','N/A','2024-05-05','Quarantine','Disease outbreak');
/*!40000 ALTER TABLE `health_record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interaction`
--

DROP TABLE IF EXISTS `interaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `interaction` (
  `interaction_id` int NOT NULL AUTO_INCREMENT,
  `species_id` int DEFAULT NULL,
  `mitigation_efforts` text,
  `date_recorded` date DEFAULT NULL,
  `incident_type` varchar(100) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`interaction_id`),
  KEY `species_id` (`species_id`),
  CONSTRAINT `interaction_ibfk_1` FOREIGN KEY (`species_id`) REFERENCES `species` (`species_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interaction`
--

LOCK TABLES `interaction` WRITE;
/*!40000 ALTER TABLE `interaction` DISABLE KEYS */;
INSERT INTO `interaction` VALUES (1,1,'Increased patrolling','2024-03-12','Poaching attempt','Sundarbans Core Area'),(2,2,'Rescue operation','2024-02-25','Fishing cat stuck in net','Buffer Zone'),(3,3,'Fencing installed','2024-04-18','Crocodile entering village','Freshwater Zones'),(4,4,'Public awareness campaign','2024-01-20','Tourist disturbance','Protected Areas'),(5,5,'Rescue operations','2024-05-10','Terrapin poaching','Coastal Wetlands');
/*!40000 ALTER TABLE `interaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `made_on`
--

DROP TABLE IF EXISTS `made_on`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `made_on` (
  `species_id` int NOT NULL,
  `report_id` int NOT NULL,
  `report_type` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`species_id`,`report_id`),
  KEY `report_id` (`report_id`),
  CONSTRAINT `made_on_ibfk_1` FOREIGN KEY (`species_id`) REFERENCES `species` (`species_id`),
  CONSTRAINT `made_on_ibfk_2` FOREIGN KEY (`report_id`) REFERENCES `report` (`report_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `made_on`
--

LOCK TABLES `made_on` WRITE;
/*!40000 ALTER TABLE `made_on` DISABLE KEYS */;
INSERT INTO `made_on` VALUES (1,1,'Bengal Tiger monitoring'),(2,2,'Fishing Cat movement study'),(3,3,'System security audit'),(4,4,'Saltwater Crocodile population study'),(5,5,'Human-wildlife conflict analysis');
/*!40000 ALTER TABLE `made_on` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `movement`
--

DROP TABLE IF EXISTS `movement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `movement` (
  `movement_id` int NOT NULL AUTO_INCREMENT,
  `species_id` int DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `latitude` decimal(9,6) DEFAULT NULL,
  `longitude` decimal(9,6) DEFAULT NULL,
  PRIMARY KEY (`movement_id`),
  KEY `species_id` (`species_id`),
  CONSTRAINT `movement_ibfk_1` FOREIGN KEY (`species_id`) REFERENCES `species` (`species_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movement`
--

LOCK TABLES `movement` WRITE;
/*!40000 ALTER TABLE `movement` DISABLE KEYS */;
INSERT INTO `movement` VALUES (1,1,'2024-03-05 03:30:00',21.949700,88.431400),(2,2,'2024-02-22 05:00:00',22.009900,88.737800),(3,3,'2024-04-20 06:15:00',21.937500,88.523400),(4,4,'2024-01-25 08:30:00',21.981200,88.486200),(5,5,'2024-05-07 10:45:00',21.923800,88.693000);
/*!40000 ALTER TABLE `movement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `report`
--

DROP TABLE IF EXISTS `report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `report` (
  `report_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `report_type` varchar(50) DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`report_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `report_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `report`
--

LOCK TABLES `report` WRITE;
/*!40000 ALTER TABLE `report` DISABLE KEYS */;
INSERT INTO `report` VALUES (1,1,'Bengal Tiger monitoring','2024-03-15'),(2,2,'Fishing Cat movement study','2024-02-28'),(3,3,'System security audit','2024-04-05'),(4,4,'Saltwater Crocodile population study','2024-05-01'),(5,5,'Human-wildlife conflict analysis','2024-01-22');
/*!40000 ALTER TABLE `report` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `resides_in`
--

DROP TABLE IF EXISTS `resides_in`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `resides_in` (
  `species_id` int NOT NULL,
  `habitat_id` int NOT NULL,
  `area_size` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`species_id`,`habitat_id`),
  KEY `habitat_id` (`habitat_id`),
  CONSTRAINT `resides_in_ibfk_1` FOREIGN KEY (`species_id`) REFERENCES `species` (`species_id`),
  CONSTRAINT `resides_in_ibfk_2` FOREIGN KEY (`habitat_id`) REFERENCES `habitat` (`habitat_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resides_in`
--

LOCK TABLES `resides_in` WRITE;
/*!40000 ALTER TABLE `resides_in` DISABLE KEYS */;
INSERT INTO `resides_in` VALUES (1,1,2000.00),(2,2,500.00),(3,3,1200.00),(4,4,300.00),(5,5,500.00);
/*!40000 ALTER TABLE `resides_in` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `species`
--

DROP TABLE IF EXISTS `species`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `species` (
  `species_id` int NOT NULL AUTO_INCREMENT,
  `population_status` varchar(50) DEFAULT NULL,
  `common_name` varchar(100) DEFAULT NULL,
  `scientific_name` varchar(100) DEFAULT NULL,
  `classification` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`species_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `species`
--

LOCK TABLES `species` WRITE;
/*!40000 ALTER TABLE `species` DISABLE KEYS */;
INSERT INTO `species` VALUES (1,'Endangered','Bengal Tiger','Panthera tigris tigris','Mammal'),(2,'Endangered','Fishing Cat','Prionailurus viverrinus','Mammal'),(3,'Vulnerable','Saltwater Crocodile','Crocodylus porosus','Reptile'),(4,'Least Concern','Indian Peafowl','Pavo cristatus','Bird'),(5,'Endangered','Northern River Terrapin','Batagur baska','Reptile');
/*!40000 ALTER TABLE `species` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `role` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Rajesh Kumar','rajesh.kumar@example.com','password123','Conservationist'),(2,'Anjali Gupta','anjali.gupta@example.com','password456','Researcher'),(3,'Suresh Menon','suresh.menon@example.com','password789','Administrator'),(4,'Priya Singh','priya.singh@example.com','passwordabc','Field Technician'),(5,'Amit Sharma','amit.sharma@example.com','passwordxyz','Conservationist');
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

-- Dump completed on 2024-10-31 18:23:26
