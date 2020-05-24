DROP TABLE IF EXISTS test.article_archives;
CREATE TABLE test.article_archives (
  id         int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  url        text             NOT NULL,
  content    mediumblob,
  title      varchar(255),
  created_at datetime         NOT NULL,
  updated_at datetime         NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY url (url(255)) USING BTREE,
  KEY updated_at (updated_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 DEFAULT COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC;

DROP TABLE IF EXISTS test.crawl_requests;
CREATE TABLE test.crawl_requests (
  id             int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  job_id         varchar(255) DEFAULT NULL,
  job_type       varchar(50) NOT NULL,
  start_urls     text NOT NULL,
  rules          json,
  schedule_type  varchar(50) NOT NULL,
  interval_hours int(10) UNSIGNED DEFAULT NULL,
  created_at datetime         NOT NULL,
  updated_at datetime         NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY job_id (job_id(255)) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 DEFAULT COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC;

