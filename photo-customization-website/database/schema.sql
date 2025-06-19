CREATE TABLE `orders` (
  `id` INT UNSIGNED AUTO_INCREMENT,
  `order_no` VARCHAR(32) NOT NULL COMMENT '唯一订单号',
  `user_id` VARCHAR(64) NOT NULL COMMENT '用户标识',
  `image_path` VARCHAR(255) COMMENT '最终排版图片路径',
  `receiver_info` JSON COMMENT '收件信息（姓名/电话/地址）',
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_no_unique` (`order_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `templates` (
  `id` INT UNSIGNED AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL COMMENT '模板名称',
  `preview_url` VARCHAR(255) NOT NULL COMMENT '预览图地址',
  `background_path` VARCHAR(255) NOT NULL COMMENT '模板背景图路径',
  `is_active` TINYINT(1) DEFAULT 1 COMMENT '是否启用',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    