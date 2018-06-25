begin;
---- USERS ----
drop table if exists Users cascade;
create table Users(
       user_id          serial primary key,
       username         text unique not null,
       name             text not null,
       created_at       date not null default now(),
       is_deleted       boolean not null default False, -- Field for marking a user as deleted
       last_login_at    timestamptz,
       k19_membership   integer unique,
       email            text,
       phone            text,
       address          text,
       birthday_at      date
);
create unique index on Users (lower(username)); -- Ensure usernames are case insensitive

drop table if exists Passwords cascade;
create table Passwords(
       user_id          integer references Users(user_id) primary key,
       password         text not null -- Store salt, not actual password. If password is to be deleted the entry is removed instead
);

drop table if exists Groups cascade;
create table Groups(
       group_id         serial primary key,
       groupname        text unique not null
);

insert into Groups(groupname) values('admin');
insert into Groups(groupname) values('admin_mail_log');
insert into Groups(groupname) values('responsible');
insert into Groups(groupname) values('member');


drop table if exists Users_groups cascade;
create table Users_groups(
       user_id          integer references Users(user_id),
       group_id         integer references Groups(group_id),
       primary key (user_id, group_id)
);

drop table if exists User_invitation_keys cascade;
create table User_invitation_keys(
       key              text primary key,
       email            text unique,
       created_at       timestamptz not null default now()
);

drop table if exists User_forgotten_password_keys cascade;
create table User_forgotten_password_keys(
       key              text primary key,
       user_id          integer references Users(user_id) unique,
       created_at       timestamptz not null default now()
);


drop table if exists Meetings cascade;
create table Meetings(
       meeting_id       serial primary key,
       date             timestamptz not null,
       title            text,
       description      text,
       created_at       timestamptz not null default now(),
       created_by       integer references Users(user_id),
       is_canceled      boolean not null default false
);
drop table if exists Meetings_users cascade;
create table Meetings_users(
       meeting_id       integer references Meetings(meeting_id),
       user_id          integer references Users(user_id),
       is_attending     boolean not null,
       note             text,
       updated_at       timestamptz not null default now(),
       primary key (meeting_id, user_id)
);

drop table if exists News cascade;
create table News(
       news_id          serial primary key,
       created_at       timestamptz not null default now(),
       created_by       integer references Users(user_id),
       title            text,
       content          text,
);
drop table if exists News_comments cascade;
create table News_comments(
       comment_id       serial primary key,
       news_id          integer references News(news_id),
       reply_to         integer references News_comments(comment_id),
       created_at       timestamptz not null default now(),
       created_by       integer references Users(user_id),
       title            text,
       content          text,
);

commit;
