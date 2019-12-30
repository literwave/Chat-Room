/*
 Navicat Premium Data Transfer

 Source Server         : literwave
 Source Server Type    : MySQL
 Source Server Version : 50726
 Source Host           : localhost:3306
 Source Schema         : test3

 Target Server Type    : MySQL
 Target Server Version : 50726
 File Encoding         : 65001

 Date: 31/12/2019 00:19:43
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for mysock
-- ----------------------------
DROP TABLE IF EXISTS `mysock`;
CREATE TABLE `mysock`  (
  `useid` varchar(11) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `paswd` varchar(20) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  PRIMARY KEY (`useid`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of mysock
-- ----------------------------
INSERT INTO `mysock` VALUES ('', '');
INSERT INTO `mysock` VALUES ('123', '123');
INSERT INTO `mysock` VALUES ('1234', '1234');
INSERT INTO `mysock` VALUES ('123456', '123');
INSERT INTO `mysock` VALUES ('1234567', '1234567');
INSERT INTO `mysock` VALUES ('1979084112', '123456');
INSERT INTO `mysock` VALUES ('572354941', '123456');
INSERT INTO `mysock` VALUES ('5723549411', '123456');
INSERT INTO `mysock` VALUES ('user1', '123456');
INSERT INTO `mysock` VALUES ('user2', '123456');

SET FOREIGN_KEY_CHECKS = 1;
