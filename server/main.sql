PRAGMA foreign_keys = OFF;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS "main"."users";
CREATE TABLE "users" (
"user_id"  INTEGER NOT NULL,
"username"  TEXT,
"password"  TEXT,
"nickname"  TEXT,
PRIMARY KEY ("user_id" ASC)
);
-- ----------------------------
-- Table structure for chat_room
-- ----------------------------
DROP TABLE IF EXISTS "main"."chat_room";
CREATE TABLE "chat_room" (
"room_id"  INTEGER NOT NULL,
"room_name"  TEXT,
PRIMARY KEY ("room_id" ASC)
);

-- ----------------------------
-- Table structure for room_user
-- ----------------------------
DROP TABLE IF EXISTS "main"."room_list";
CREATE TABLE "room_list" (
"id"  INTEGER NOT NULL,
"room_id"  INTEGER,
"user_id"  INTEGER,
PRIMARY KEY ("id")
);

-- ----------------------------
-- Table structure for chat_history
-- ----------------------------
DROP TABLE IF EXISTS "main"."chat_history";
CREATE TABLE "chat_history" (
"id"  INTEGER NOT NULL,
"user_id"  INTEGER,
"target_id"  INTEGER,
"target_type"  TEXT,
"data"  BLOB,
"sent"  INTEGER,
-- "time"
PRIMARY KEY ("id" ASC)
);

-- ----------------------------
-- Table structure for friends
-- ----------------------------
DROP TABLE IF EXISTS "main"."friends";
CREATE TABLE "friends" (
"from_user_id"  INTEGER NOT NULL,
"to_user_id"  INTEGER NOT NULL,
"accepted"  TEXT,
PRIMARY KEY ("from_user_id" ASC, "to_user_id")
);




