-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 23, 2020 at 02:32 PM
-- Server version: 10.4.11-MariaDB
-- PHP Version: 7.2.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `rfidattendance`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `admin_name` varchar(30) NOT NULL,
  `admin_email` varchar(80) NOT NULL,
  `admin_pwd` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `admin_name`, `admin_email`, `admin_pwd`) VALUES
(1, 'Admin', 'admin@gmail.com', '$2y$10$89uX3LBy4mlU/DcBveQ1l.32nSianDP/E1MfUh.Z.6B4Z0ql3y7PK');

-- --------------------------------------------------------

--
-- Table structure for table `devices`
--

CREATE TABLE `devices` (
  `id` int(11) NOT NULL,
  `device_name` varchar(50) NOT NULL,
  `device_dep` varchar(20) NOT NULL,
  `device_uid` text NOT NULL,
  `device_date` date NOT NULL,
  `device_mode` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `devices`
--

INSERT INTO `devices` (`id`, `device_name`, `device_dep`, `device_uid`, `device_date`, `device_mode`) VALUES
(1, 'Test', 'Test', 'f554b65977e460e1', '2020-06-14', 1);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(30) NOT NULL DEFAULT 'None',
  `serialnumber` double NOT NULL DEFAULT 0,
  `gender` varchar(10) NOT NULL DEFAULT 'None',
  `email` varchar(50) NOT NULL DEFAULT 'None',
  `card_uid` varchar(30) NOT NULL,
  `card_select` tinyint(1) NOT NULL DEFAULT 0,
  `user_date` date NOT NULL,
  `device_uid` varchar(20) NOT NULL DEFAULT '0',
  `device_dep` varchar(20) NOT NULL DEFAULT '0',
  `add_card` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `serialnumber`, `gender`, `email`, `card_uid`, `card_select`, `user_date`, `device_uid`, `device_dep`, `add_card`) VALUES
(1, 'Josh', 111, 'Male', 'adsa', '1231231', 0, '2020-06-14', 'f554b65977e460e1', 'Test', 1),
(2, 'NoneTestsss', 2, 'Male', 'None', '885974631345', 0, '2020-06-14', 'f554b65977e460e1', 'Test', 1),
(3, 'None', 0, 'None', 'None', '1050838182562', 0, '2020-06-14', 'f554b65977e460e1', 'Test', 0),
(4, 'ld', 6455415, 'Male', 'None', '562229427492', 0, '2020-06-14', 'f554b65977e460e1', 'Test', 1),
(5, 'mm', 99, 'Male', 'None', '867188882784', 0, '2020-06-14', 'f554b65977e460e1', 'Test', 1),
(6, 'None', 0, 'None', 'None', '1234567', 1, '2020-06-15', 'f554b65977e460e1', 'Test', 0);

-- --------------------------------------------------------

--
-- Table structure for table `users_logs`
--

CREATE TABLE `users_logs` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `serialnumber` double NOT NULL,
  `card_uid` varchar(30) NOT NULL,
  `device_uid` varchar(20) NOT NULL,
  `device_dep` varchar(20) NOT NULL,
  `checkindate` date NOT NULL,
  `timein` time NOT NULL,
  `timeout` time NOT NULL,
  `card_out` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `users_logs`
--

INSERT INTO `users_logs` (`id`, `username`, `serialnumber`, `card_uid`, `device_uid`, `device_dep`, `checkindate`, `timein`, `timeout`, `card_out`) VALUES
(1, 'NoneTestsss', 2, '885974631345', 'f554b65977e460e1', 'Test', '2020-06-14', '18:42:04', '18:42:20', 1),
(2, 'NoneTestsss', 2, '885974631345', 'f554b65977e460e1', 'Test', '2020-06-14', '18:51:06', '00:00:00', 0),
(3, 'mm', 99, '867188882784', 'f554b65977e460e1', 'Test', '2020-06-14', '18:58:34', '00:00:00', 0),
(4, 'ld', 6455415, '562229427492', 'f554b65977e460e1', 'Test', '2020-06-14', '18:58:56', '18:59:02', 1),
(5, 'mm', 99, '867188882784', 'f554b65977e460e1', 'Test', '2020-06-15', '15:24:43', '15:27:47', 1),
(6, 'NoneTestsss', 2, '885974631345', 'f554b65977e460e1', 'Test', '2020-06-15', '15:27:27', '15:27:32', 1),
(7, 'mm', 99, '867188882784', 'f554b65977e460e1', 'Test', '2020-06-15', '15:28:16', '00:00:00', 0),
(8, 'NoneTestsss', 2, '885974631345', 'f554b65977e460e1', 'Test', '2020-06-15', '15:29:28', '15:29:36', 1),
(9, 'NoneTestsss', 2, '885974631345', 'f554b65977e460e1', 'Test', '2020-06-15', '15:29:45', '18:33:32', 1),
(10, 'NoneTestsss', 2, '885974631345', 'f554b65977e460e1', 'Test', '2020-06-15', '18:33:34', '18:33:44', 1),
(11, 'NoneTestsss', 2, '885974631345', 'f554b65977e460e1', 'Test', '2020-06-15', '18:33:46', '00:00:00', 0),
(12, 'mm', 99, '867188882784', 'f554b65977e460e1', 'Test', '2020-06-16', '21:32:11', '21:32:18', 1),
(13, 'mm', 99, '867188882784', 'f554b65977e460e1', 'Test', '2020-06-16', '21:32:21', '00:00:00', 0),
(14, 'ld', 6455415, '562229427492', 'f554b65977e460e1', 'Test', '2020-06-16', '21:32:24', '21:32:27', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `devices`
--
ALTER TABLE `devices`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users_logs`
--
ALTER TABLE `users_logs`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `devices`
--
ALTER TABLE `devices`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `users_logs`
--
ALTER TABLE `users_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
