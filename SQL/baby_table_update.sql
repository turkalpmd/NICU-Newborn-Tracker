alter table baby_table
    alter column baby_id type SERIAL using baby_id::SERIAL;

alter table baby_table
    alter column baby_id add generated always as identity;

alter table baby_table
    add baby_id_md5 varchar(32);

alter table baby_table
    add couveuse_number integer;    