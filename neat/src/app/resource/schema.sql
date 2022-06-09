DROP TABLE IF EXISTS groups;
drop table if exists servers;
drop table if exists tasks;

create table if not exists servers(
    id integer primary key autoincrement,
    ip text not null ,
    port integer not null ,
    user text not null ,
    password text not null ,
    position text not null
);

create table if not exists groups(
    name text not null ,
    server_id integer not null,
    primary key (name,server_id)
);

create table if not exists tasks(
    id integer primary key autoincrement,
    name text not null ,
    command text not null ,
    env text not null ,
    script text not null ,
    notes text
);

insert into servers(ip,port,user,password,position) values ('192.168.28.131',22,'breath','naxiehuaer','test');
insert into servers(ip,port,user,password,position) values ('172.16.135.184',22,'breath','naxiehuaer','test');

insert into groups(name, server_id) values ('group1', 1);
insert into groups(name, server_id) values ('group1', 2);
insert into groups(name, server_id) values ('group2', 1);


insert into tasks(name, command, env, script, notes) values ('echo','sh test1.sh',
'D:\\workspace\\neat\\neat\\src\\app\\tasks\\echo\\env\\echo.yaml',
'D:\\workspace\\neat\\neat\\src\\app\\tasks\\echo\\bin\\test1.sh', 'for test');








