drop table if exists users;
create table users (
  id integer primary key autoincrement,
  name text not null,
  password text not null
);

insert into users (name, password) values ('visit', '111');
insert into users (name, password) values ('admin', '123');
