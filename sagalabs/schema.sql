drop table if exists users;
create table users (
    'id' INTEGER primary key, -- unique id of user
    'username' TEXT not NULL unique, -- username
    'password' TEXT not NULL, -- hashed password of user
    'is_admin' BOOLEAN not NULL -- 1 is the user an admin
);
