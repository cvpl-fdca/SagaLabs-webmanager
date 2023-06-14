drop table if exists users;
create table users (
    'id' INTEGER primary key, -- unique id of user
    'username' TEXT not NULL unique, -- username
    'password' TEXT not NULL -- hashed password of user
);
