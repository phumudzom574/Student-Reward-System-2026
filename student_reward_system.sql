-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Aug 31, 2026 at 04:28 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `student_reward_system`
--

-- --------------------------------------------------------

--
-- Table structure for table `goalprogress`
--

CREATE TABLE `goalprogress` (
  `ProgressID` int(11) NOT NULL,
  `ParticipantID` int(11) DEFAULT NULL,
  `GoalID` int(11) DEFAULT NULL,
  `CurrentPoints` int(11) DEFAULT 0,
  `Completed` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `goalprogress`
--

INSERT INTO `goalprogress` (`ProgressID`, `ParticipantID`, `GoalID`, `CurrentPoints`, `Completed`) VALUES
(1, 1, 1, 10, 0);

-- --------------------------------------------------------

--
-- Table structure for table `goals`
--

CREATE TABLE `goals` (
  `GoalID` int(11) NOT NULL,
  `ParticipantID` int(11) DEFAULT NULL,
  `StartDate` date DEFAULT NULL,
  `EndDate` date DEFAULT NULL,
  `TargetPoints` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `goals`
--

INSERT INTO `goals` (`GoalID`, `ParticipantID`, `StartDate`, `EndDate`, `TargetPoints`) VALUES
(1, 1, '2026-08-13', '2026-11-02', 100),
(2, 1, '2026-08-13', '2026-11-02', 100);

-- --------------------------------------------------------

--
-- Table structure for table `participants`
--

CREATE TABLE `participants` (
  `ParticipantID` int(11) NOT NULL,
  `Name` varchar(100) NOT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `StartDate` date DEFAULT NULL,
  `Active` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `participants`
--

INSERT INTO `participants` (`ParticipantID`, `Name`, `Email`, `StartDate`, `Active`) VALUES
(1, 'Phumudzo Mulaudzi', 'phumudzo@gmail.com', '2026-08-10', 1),
(2, 'Thilivhali Mulaudzi', 'thilivhali@gmail.com', '2026-08-12', 1),
(3, 'Test Student', 'test@example.com', '2026-08-17', 1),
(4, 'Nyiko', 'nyiko@gmail.com', '2026-08-17', 1);

-- --------------------------------------------------------

--
-- Table structure for table `pointrules`
--

CREATE TABLE `pointrules` (
  `RuleID` int(11) NOT NULL,
  `ActivityName` varchar(100) DEFAULT NULL,
  `Description` text DEFAULT NULL,
  `Points` int(11) DEFAULT NULL,
  `MaxPerDay` int(11) DEFAULT NULL,
  `Active` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pointrules`
--

INSERT INTO `pointrules` (`RuleID`, `ActivityName`, `Description`, `Points`, `MaxPerDay`, `Active`) VALUES
(1, 'Attend Workshop', 'IT Project Management Workshop', 50, 1, 1),
(2, 'Workshop', 'IT Project Management', 50, 1, 1),
(3, 'Attendance', 'Session Attendance', 10, 1, 1),
(4, 'workshop', 'programming attendance', 50, 1, 1),
(5, 'workshop', 'programming attendace', 50, 1, 1),
(6, 'workshop', 'programming attendace', 10, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `pointtransactions`
--

CREATE TABLE `pointtransactions` (
  `TransactionID` int(11) NOT NULL,
  `ParticipantID` int(11) DEFAULT NULL,
  `RuleID` int(11) DEFAULT NULL,
  `ActivityDate` date DEFAULT NULL,
  `Points` int(11) DEFAULT NULL,
  `Notes` text DEFAULT NULL,
  `CreatedAt` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pointtransactions`
--

INSERT INTO `pointtransactions` (`TransactionID`, `ParticipantID`, `RuleID`, `ActivityDate`, `Points`, `Notes`, `CreatedAt`) VALUES
(1, 1, 1, '2026-08-17', 10, 'attended class', '2026-08-17 20:18:57'),
(2, 1, 1, '2026-08-17', 10, 'attended class', '2026-08-17 20:19:30');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `UserID` int(11) NOT NULL,
  `Username` varchar(50) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `Role` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`UserID`, `Username`, `Password`, `Role`) VALUES
(1, 'admin', 'admin123', 'admin');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `goalprogress`
--
ALTER TABLE `goalprogress`
  ADD PRIMARY KEY (`ProgressID`),
  ADD KEY `ParticipantID` (`ParticipantID`),
  ADD KEY `GoalID` (`GoalID`);

--
-- Indexes for table `goals`
--
ALTER TABLE `goals`
  ADD PRIMARY KEY (`GoalID`),
  ADD KEY `ParticipantID` (`ParticipantID`);

--
-- Indexes for table `participants`
--
ALTER TABLE `participants`
  ADD PRIMARY KEY (`ParticipantID`);

--
-- Indexes for table `pointrules`
--
ALTER TABLE `pointrules`
  ADD PRIMARY KEY (`RuleID`);

--
-- Indexes for table `pointtransactions`
--
ALTER TABLE `pointtransactions`
  ADD PRIMARY KEY (`TransactionID`),
  ADD KEY `ParticipantID` (`ParticipantID`),
  ADD KEY `RuleID` (`RuleID`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`UserID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `goalprogress`
--
ALTER TABLE `goalprogress`
  MODIFY `ProgressID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `goals`
--
ALTER TABLE `goals`
  MODIFY `GoalID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `participants`
--
ALTER TABLE `participants`
  MODIFY `ParticipantID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `pointrules`
--
ALTER TABLE `pointrules`
  MODIFY `RuleID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `pointtransactions`
--
ALTER TABLE `pointtransactions`
  MODIFY `TransactionID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `UserID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `goalprogress`
--
ALTER TABLE `goalprogress`
  ADD CONSTRAINT `goalprogress_ibfk_1` FOREIGN KEY (`ParticipantID`) REFERENCES `participants` (`ParticipantID`),
  ADD CONSTRAINT `goalprogress_ibfk_2` FOREIGN KEY (`GoalID`) REFERENCES `goals` (`GoalID`);

--
-- Constraints for table `goals`
--
ALTER TABLE `goals`
  ADD CONSTRAINT `goals_ibfk_1` FOREIGN KEY (`ParticipantID`) REFERENCES `participants` (`ParticipantID`);

--
-- Constraints for table `pointtransactions`
--
ALTER TABLE `pointtransactions`
  ADD CONSTRAINT `pointtransactions_ibfk_1` FOREIGN KEY (`ParticipantID`) REFERENCES `participants` (`ParticipantID`),
  ADD CONSTRAINT `pointtransactions_ibfk_2` FOREIGN KEY (`RuleID`) REFERENCES `pointrules` (`RuleID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
