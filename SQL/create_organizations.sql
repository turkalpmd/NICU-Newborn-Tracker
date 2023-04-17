create table organizations
(
    organization_id smallint default nextval('organizations_organization_id_seq'::regclass);
        constraint organizations_pk
            primary key,
    organization_admin varchar(50),
    organization_name  varchar(40),
    doctor_id          integer
        constraint organizations_doctor_id_fk
            references doctors
);