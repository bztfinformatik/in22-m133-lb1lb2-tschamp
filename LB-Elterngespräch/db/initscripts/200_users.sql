USE `classicmodels`;

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `id` int NOT NULL UNIQUE AUTO_INCREMENT,
  `username` varchar(15) UNIQUE,
  `password` varchar(80) UNIQUE,
  `access` smallint(6) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
