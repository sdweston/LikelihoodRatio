# mysql to find radio pairs

create table elais_s1.coords2 like elais_s1.coords;
truncate table elais_s1.coords2;
select count(*) from elais_s1.coords2;
insert into elais_s1.coords2 select * from elais_s1.coords;

truncate table elais_s1.radio_pairs;
insert into elais_s1.radio_pairs(cid1,cid2,ang_sep_arcsec)
select t1.cid, t2.cid,
       format(sqrt(pow((t1.RA_Deg-t2.RA_Deg)*cos(t1.Dec_Deg),2)+pow(t1.Dec_Deg-t2.DEC_Deg,2))*3600,6)
from elais_s1.coords as t1, elais_s1.coords2 as t2
where pow((t1.RA_Deg-t2.RA_Deg)*cos(t1.Dec_Deg),2)+
      pow(t1.Dec_Deg-t2.DEC_Deg,2) <= pow(100/3600,2)
and t1.cid!=t2.cid
limit 0,20000;

# now get the flux's

update elais_s1.radio_pairs as t1
   inner join elais_s1.table4 as t2
   on t1.cid1=t2.cid
set t1.flux1=t2.sint;

update elais_s1.radio_pairs as t1
   inner join elais_s1.table4 as t2
   on t1.cid2=t2.cid
set t1.flux2=t2.sint;

select flux1,flux2,flux1/flux2,log10(flux1/flux2),ang_sep_arcsec from elais_s1.radio_pairs limit 0,10000;