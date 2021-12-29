-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Generation Time: Dec 09, 2021 at 03:29 AM
-- Server version: 5.7.34
-- PHP Version: 8.0.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `airlines`
--

-- --------------------------------------------------------

--
-- Table structure for table `airline`
--

CREATE TABLE `airline` (
  `airline_name` varchar(256) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `airline`
--

INSERT INTO `airline` (`airline_name`) VALUES
('China Eastern'),
('Singapore Airlines');

-- --------------------------------------------------------

--
-- Table structure for table `airline_staff`
--

CREATE TABLE `airline_staff` (
  `airline_name` varchar(256) DEFAULT NULL,
  `user_name` varchar(20) NOT NULL,
  `first_name` varchar(20) DEFAULT NULL,
  `last_name` varchar(20) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `airline_staff`
--

INSERT INTO `airline_staff` (`airline_name`, `user_name`, `first_name`, `last_name`, `password`, `date_of_birth`) VALUES
('Singapore Airlines', 'barry', 'Barry', 'Zhang', '5f4dcc3b5aa765d61d8327deb882cf99', '2001-02-28'),
('China Eastern', 'longph', 'Long ', 'Phi', '5d41402abc4b2a76b9719d911017c592', '2021-11-28'),
('China Eastern', 'staff_user', 'Bim', 'Zhang', 'password', '2001-01-28'),
('China Eastern', 'tiff', 'Tiffany', 'Lin', '5f4dcc3b5aa765d61d8327deb882cf99', '2000-02-01');

-- --------------------------------------------------------

--
-- Table structure for table `airplane`
--

CREATE TABLE `airplane` (
  `airline_name` varchar(256) DEFAULT NULL,
  `airplane_ID` varchar(10) NOT NULL,
  `num_of_seats` decimal(3,0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `airplane`
--

INSERT INTO `airplane` (`airline_name`, `airplane_ID`, `num_of_seats`) VALUES
('China Eastern', '435', '435'),
('China Eastern', '532', '200'),
('China Eastern', '542', '250'),
('China Eastern', '552', '100'),
('China Eastern', '590', '500'),
('China Eastern', '6969', '999'),
('Singapore Airlines', 'S123', '5');

-- --------------------------------------------------------

--
-- Table structure for table `airport`
--

CREATE TABLE `airport` (
  `airport_code` varchar(10) NOT NULL,
  `airport_name` varchar(256) DEFAULT NULL,
  `airport_city` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `airport`
--

INSERT INTO `airport` (`airport_code`, `airport_name`, `airport_city`) VALUES
('JFK', 'John F. Kennedy Airport', 'NYC'),
('PVG', 'Shanghai Pudong Airport', 'Shanghai'),
('SGN', 'Tan Son Nhat', 'Sai Gon'),
('SGP', 'Changi Airport', 'Singapore');

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `name` varchar(50) DEFAULT NULL,
  `email` varchar(50) NOT NULL,
  `cust_password` varchar(50) DEFAULT NULL,
  `building_num` varchar(20) DEFAULT NULL,
  `street` varchar(20) DEFAULT NULL,
  `city` varchar(20) DEFAULT NULL,
  `state` varchar(20) DEFAULT NULL,
  `cust_phone_num` decimal(10,0) DEFAULT NULL,
  `passport_num` varchar(20) DEFAULT NULL,
  `passport_expiration` date DEFAULT NULL,
  `passport_country` varchar(20) DEFAULT NULL,
  `cust_dob` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`name`, `email`, `cust_password`, `building_num`, `street`, `city`, `state`, `cust_phone_num`, `passport_num`, `passport_expiration`, `passport_country`, `cust_dob`) VALUES
('Thinzar Lin', 'email@nyu.edu', '5f4dcc3b5aa765d61d8327deb882cf99', '12', '100 Willoughby St', 'Brooklyn', 'NY', '7657728373', '12131414', '2025-12-12', 'Myanmar', '2000-12-12'),
('John', 'john@nyu.edu', 'hiheyho', '133', '44 clark street', 'NYC', 'NY', '27239384', 'ME345443', '2018-11-21', 'Korea', '2002-04-02'),
('Long', 'lhp256@nyu.edu', 'another', '133', '189 Adelphi St', 'NYC', 'NY', '7657239384', 'MD233455443', '2036-11-11', 'US', '2001-09-12'),
('Long Phi', 'long@gmail.com', '5d41402abc4b2a76b9719d911017c592', '4', '12 Metro', 'New York', 'NY', '34235234', '2435345234', '2021-12-31', 'Viet Nam', '2021-12-06'),
('Tiffany', 'tl2853@nyu.edu', 'thisispass', '123', '156 Adelphi St', 'NYC', 'NY', '7657729384', 'MD234443', '2026-11-11', 'Myanmar', '2000-09-28');

-- --------------------------------------------------------

--
-- Table structure for table `flight`
--

CREATE TABLE `flight` (
  `airplane_ID` varchar(10) DEFAULT NULL,
  `airline_name` varchar(256) NOT NULL,
  `flight_num` varchar(10) NOT NULL,
  `base_price` decimal(10,0) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `departure_date_time` datetime NOT NULL,
  `arrival_date_time` datetime DEFAULT NULL,
  `departure_airport_code` varchar(10) DEFAULT NULL,
  `arrival_airport_code` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `flight`
--

INSERT INTO `flight` (`airplane_ID`, `airline_name`, `flight_num`, `base_price`, `status`, `departure_date_time`, `arrival_date_time`, `departure_airport_code`, `arrival_airport_code`) VALUES
('542', 'China Eastern', 'A123', '350', 'delayed', '2021-12-13 00:13:00', '2021-12-13 03:13:00', 'JFK', 'SGP'),
('542', 'China Eastern', 'B123', '400', 'on-time', '2021-12-13 01:00:00', '2021-12-13 03:00:00', 'SGP', 'JFK'),
('552', 'China Eastern', 'D123', '400', 'on-time', '2021-12-12 00:12:00', '2021-12-13 00:12:00', 'PVG', 'JFK'),
('552', 'China Eastern', 'F123', '300', 'delayed', '2021-12-12 00:00:00', '2021-12-12 00:00:00', 'JFK', 'PVG'),
('532', 'China Eastern', 'F134', '500', 'on time', '2021-11-22 12:45:08', '2021-11-23 10:30:00', 'PVG', 'JFK'),
('S123', 'Singapore Airlines', 'SG443', '200', 'delayed', '2021-12-31 00:45:00', '2021-12-31 02:45:00', 'SGP', 'JFK');

-- --------------------------------------------------------

--
-- Table structure for table `purchase`
--

CREATE TABLE `purchase` (
  `ticket_ID` int(11) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `purchase`
--

INSERT INTO `purchase` (`ticket_ID`, `email`) VALUES
(4, 'tl2853@nyu.edu'),
(5, 'lhp256@nyu.edu'),
(6, 'tl2853@nyu.edu'),
(7, 'tl2853@nyu.edu'),
(8, 'lhp256@nyu.edu'),
(9, 'lhp256@nyu.edu'),
(10, 'email@nyu.edu'),
(11, 'email@nyu.edu');

-- --------------------------------------------------------

--
-- Table structure for table `rate`
--

CREATE TABLE `rate` (
  `flight_num` varchar(10) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `rating` decimal(1,0) DEFAULT NULL,
  `comment` varchar(1000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `rate`
--

INSERT INTO `rate` (`flight_num`, `email`, `rating`, `comment`) VALUES
('F123', 'tl2853@nyu.edu', '5', 'twas good'),
('F123', 'email@nyu.edu', '3', 'kinda good but still bad'),
('B123', 'email@nyu.edu', '4', 'Nice');

-- --------------------------------------------------------

--
-- Table structure for table `staff_phone`
--

CREATE TABLE `staff_phone` (
  `user_name` varchar(20) DEFAULT NULL,
  `phone_number` decimal(10,0) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `staff_phone`
--

INSERT INTO `staff_phone` (`user_name`, `phone_number`) VALUES
('barry', '12345'),
('longph', '3543423'),
('staff_user', '1234567890'),
('tiff', '7657728373');

-- --------------------------------------------------------

--
-- Table structure for table `ticket`
--

CREATE TABLE `ticket` (
  `email` varchar(50) DEFAULT NULL,
  `airplane_ID` varchar(10) DEFAULT NULL,
  `airline_name` varchar(256) DEFAULT NULL,
  `flight_num` varchar(10) DEFAULT NULL,
  `departure_date_time` datetime DEFAULT NULL,
  `ticket_ID` int(11) NOT NULL,
  `sold_price` decimal(10,0) DEFAULT NULL,
  `card_type` varchar(10) DEFAULT NULL,
  `card_num` decimal(12,0) DEFAULT NULL,
  `name_on_card` varchar(50) DEFAULT NULL,
  `expiration_date` date DEFAULT NULL,
  `purchase_date_time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `ticket`
--

INSERT INTO `ticket` (`email`, `airplane_ID`, `airline_name`, `flight_num`, `departure_date_time`, `ticket_ID`, `sold_price`, `card_type`, `card_num`, `name_on_card`, `expiration_date`, `purchase_date_time`) VALUES
('tl2853@nyu.edu', '552', 'China Eastern', 'F123', '2021-12-12 00:00:00', 4, '300', 'Credit', '234512345432', 'Tiffany', '2024-12-23', '2021-11-11 00:00:00'),
('lhp256@nyu.edu', '532', 'China Eastern', 'F134', '2021-11-22 12:45:08', 5, '500', 'Debit', '222222222222', 'Long', '2024-12-23', '2021-11-11 00:00:00'),
('tl2853@nyu.edu', '552', 'China Eastern', 'F123', '2021-12-12 00:00:00', 6, '300', 'Credit', '234512345432', 'Tiffany', '2024-12-23', '2021-11-11 00:00:00'),
('tl2853@nyu.edu', '552', 'China Eastern', 'F123', '2021-12-12 00:00:00', 7, '300', 'Credit', '234512345432', 'Tiffany', '2024-12-23', '2021-11-11 00:00:00'),
('lhp256@nyu.edu', '532', 'China Eastern', 'F134', '2021-11-22 12:45:08', 8, '500', 'Debit', '222222222222', 'Long', '2024-12-23', '2021-11-11 00:00:00'),
('lhp256@nyu.edu', '552', 'China Eastern', 'F123', '2021-12-12 00:00:00', 9, '300', 'Credit', '234512345432', 'Long', '2024-12-23', '2021-11-11 00:00:00'),
('email@nyu.edu', '552', 'China Eastern', 'F123', '2021-12-12 00:00:00', 10, '300', 'debit', '12345', 'thinzar', '2025-12-12', '2021-12-07 19:57:19'),
('email@nyu.edu', '542', 'China Eastern', 'B123', '2021-12-13 01:00:00', 11, '400', 'debit', '4234234213', 'Long', '2022-01-08', '2021-12-08 00:37:52');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `airline`
--
ALTER TABLE `airline`
  ADD PRIMARY KEY (`airline_name`);

--
-- Indexes for table `airline_staff`
--
ALTER TABLE `airline_staff`
  ADD PRIMARY KEY (`user_name`),
  ADD KEY `airline_name` (`airline_name`);

--
-- Indexes for table `airplane`
--
ALTER TABLE `airplane`
  ADD PRIMARY KEY (`airplane_ID`),
  ADD KEY `airline_name` (`airline_name`);

--
-- Indexes for table `airport`
--
ALTER TABLE `airport`
  ADD PRIMARY KEY (`airport_code`);

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`email`);

--
-- Indexes for table `flight`
--
ALTER TABLE `flight`
  ADD PRIMARY KEY (`flight_num`,`departure_date_time`,`airline_name`) USING BTREE,
  ADD KEY `airline_name` (`airline_name`),
  ADD KEY `airplane_ID` (`airplane_ID`),
  ADD KEY `departure_airport_code` (`departure_airport_code`),
  ADD KEY `arrival_airport_code` (`arrival_airport_code`);

--
-- Indexes for table `purchase`
--
ALTER TABLE `purchase`
  ADD KEY `ticket_ID` (`ticket_ID`),
  ADD KEY `email` (`email`);

--
-- Indexes for table `rate`
--
ALTER TABLE `rate`
  ADD KEY `flight_num` (`flight_num`),
  ADD KEY `email` (`email`);

--
-- Indexes for table `staff_phone`
--
ALTER TABLE `staff_phone`
  ADD PRIMARY KEY (`phone_number`),
  ADD KEY `user_name` (`user_name`);

--
-- Indexes for table `ticket`
--
ALTER TABLE `ticket`
  ADD PRIMARY KEY (`ticket_ID`),
  ADD KEY `email` (`email`),
  ADD KEY `airline_name` (`airline_name`),
  ADD KEY `airplane_ID` (`airplane_ID`),
  ADD KEY `flight_num` (`flight_num`,`departure_date_time`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `ticket`
--
ALTER TABLE `ticket`
  MODIFY `ticket_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `airline_staff`
--
ALTER TABLE `airline_staff`
  ADD CONSTRAINT `airline_staff_ibfk_1` FOREIGN KEY (`airline_name`) REFERENCES `airline` (`airline_name`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `airplane`
--
ALTER TABLE `airplane`
  ADD CONSTRAINT `airplane_ibfk_1` FOREIGN KEY (`airline_name`) REFERENCES `airline` (`airline_name`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `flight`
--
ALTER TABLE `flight`
  ADD CONSTRAINT `flight_ibfk_1` FOREIGN KEY (`airline_name`) REFERENCES `airline` (`airline_name`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `flight_ibfk_2` FOREIGN KEY (`airplane_ID`) REFERENCES `airplane` (`airplane_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `flight_ibfk_3` FOREIGN KEY (`departure_airport_code`) REFERENCES `airport` (`airport_code`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `flight_ibfk_4` FOREIGN KEY (`arrival_airport_code`) REFERENCES `airport` (`airport_code`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `purchase`
--
ALTER TABLE `purchase`
  ADD CONSTRAINT `purchase_ibfk_1` FOREIGN KEY (`ticket_ID`) REFERENCES `ticket` (`ticket_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `purchase_ibfk_2` FOREIGN KEY (`email`) REFERENCES `customer` (`email`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `rate`
--
ALTER TABLE `rate`
  ADD CONSTRAINT `rate_ibfk_1` FOREIGN KEY (`flight_num`) REFERENCES `flight` (`flight_num`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `rate_ibfk_2` FOREIGN KEY (`email`) REFERENCES `customer` (`email`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `staff_phone`
--
ALTER TABLE `staff_phone`
  ADD CONSTRAINT `staff_phone_ibfk_1` FOREIGN KEY (`user_name`) REFERENCES `airline_staff` (`user_name`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `ticket`
--
ALTER TABLE `ticket`
  ADD CONSTRAINT `ticket_ibfk_1` FOREIGN KEY (`email`) REFERENCES `customer` (`email`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `ticket_ibfk_2` FOREIGN KEY (`airline_name`) REFERENCES `airline` (`airline_name`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `ticket_ibfk_3` FOREIGN KEY (`airplane_ID`) REFERENCES `airplane` (`airplane_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `ticket_ibfk_4` FOREIGN KEY (`flight_num`,`departure_date_time`) REFERENCES `flight` (`flight_num`, `departure_date_time`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
