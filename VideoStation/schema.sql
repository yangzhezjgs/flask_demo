drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title string not null,
  text string not null,
  now string not null,
  name string not null
);
drop table if exists users;
create table users(
  username string not null,
  password string not null
);
