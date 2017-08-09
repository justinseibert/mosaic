drop table if exists r;
create table r (
  id INTEGER PRIMARY KEY autoincrement,
  value TEXT UNIQUE NOT NULL,
  tree TEXT,
  aqua TEXT,
  sand TEXT
);
drop table if exists g;
create table g (
  id INTEGER PRIMARY KEY autoincrement,
  value TEXT UNIQUE NOT NULL,
  tree TEXT,
  aqua TEXT,
  sand TEXT
);
drop table if exists b;
create table b (
  id INTEGER PRIMARY KEY autoincrement,
  value TEXT UNIQUE NOT NULL,
  tree TEXT,
  aqua TEXT,
  sand TEXT
);
drop table if exists a;
create table a (
  id INTEGER PRIMARY KEY autoincrement,
  value TEXT UNIQUE NOT NULL,
  tree TEXT,
  aqua TEXT,
  sand TEXT
);
