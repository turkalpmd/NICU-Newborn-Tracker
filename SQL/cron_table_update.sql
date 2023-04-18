alter table cron
    alter column status type boolean using status::boolean;

alter table cron
    add baby_id smallint;

alter table cron
    add constraint cron_baby_id_fk
        foreign key (baby_id) references baby_table;