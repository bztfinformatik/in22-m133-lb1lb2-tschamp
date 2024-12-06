USE `classicmodels`;

DROP TABLE IF EXISTS `elterngespraech_termine`;
CREATE TABLE `elterngespraech_termine` (
  `termin_id` int(11) NOT NULL AUTO_INCREMENT,
  `lehrer_id` int(11) NOT NULL,
  `schueler_name` varchar(30) NOT NULL,
  `datum` date NOT NULL,
  `uhrzeit` time NOT NULL,
  `dauer_minuten` int(20) NOT NULL,
  `status` varchar(20) NOT NULL,
  `raum` varchar(20) NOT NULL,
  `notizen` text NOT NULL,
  PRIMARY KEY (`termin_id`),
  CONSTRAINT `elterngespraech_termine_ibfk_1` FOREIGN KEY (`termin_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;