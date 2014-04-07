
# SQL to create the tables and populate the radio pairs table

drop table v_0_3.radio_pairs;

CREATE TABLE v_0_3.radio_pairs (
  cid1 varchar(8) default null,
  cid2 varchar(8) default null,
  flux1 float default null,
  flux2 float default null,
  ang_sep_arcsec float default null,
  KEY idx_cid1 (cid1),
  KEY idx_cid2 (cid2));


# mysql to find radio pairs

truncate table v_0_3.coords1;
create table v_0_3.coords1 as
       select id,ra,declination
	   from v_0_3.dr3_ecdfs_cmpcat;

truncate table v_0_3.coords2;
create table v_0_3.coords2 as
       select id,ra,declination
	   from v_0_3.dr3_ecdfs_cmpcat;
	   
truncate table v_0_3.radio_pairs;
insert into v_0_3.radio_pairs(cid1,cid2,ang_sep_arcsec)
select t1.id, t2.id,
       format(sqrt(pow((t1.RA-t2.RA)*cos(t1.Declination),2)+pow(t1.Declination-t2.Declination,2))*3600,6)
from v_0_3.coords1 as t1, v_0_3.coords2 as t2
where pow((t1.RA-t2.RA)*cos(t1.Declination),2)+
      pow(t1.Declination-t2.Declination,2) <= pow(100/3600,2)
and t1.id!=t2.id
limit 0,20000;

# now get the fluxs

set sql_safe_updates=0;
update v_0_3.radio_pairs as t1
   inner join v_0_3.dr3_ecdfs_cmpcat as t2
   on t1.cid1=t2.id
set t1.flux1=t2.s;

update v_0_3.radio_pairs as t1
   inner join v_0_3.dr3_ecdfs_cmpcat as t2
   on t1.cid2=t2.id
set t1.flux2=t2.s;

select flux1,flux2,flux1/flux2,log10(flux1/flux2),ang_sep_arcsec from v_0_3.radio_pairs limit 0,10000;