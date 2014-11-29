drop table if exists entries;
drop table if exists answered;

create table entries (
  id integer primary key autoincrement,
  title text not null,
  text text not null
);

create table answered  (
  ident integer secondary key,
  answer text not null
);
