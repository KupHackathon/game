DROP TABLE IF EXISTS "User";
CREATE TABLE "User" ("u_id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL , "name" VARCHAR, "fb_id" VARCHAR, "access_token" VARCHAR);
DROP TABLE IF EXISTS "games";
CREATE TABLE "games" ("g_id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL , "u_id1" , "u_id2" , "questions" VARCHAR, "score1" , "score2" , "answer1" , "answer2" );
