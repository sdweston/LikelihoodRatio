
drop table atlas_dr3.elais_radio_pairs;

CREATE TABLE atlas_dr3.elais_radio_pairs (
  `id` int unsigned not null auto_increment,
  `cid1` varchar(8) DEFAULT NULL,
  `cid2` varchar(8) DEFAULT NULL,
  `flux1` decimal(6,2) DEFAULT NULL,
  `flux2` decimal(6,2) DEFAULT NULL,
  `ang_sep_arcsec` decimal(10,6) DEFAULT NULL,
  'flag' varchar(2) default null,
  primary key (id),
  KEY `idx_cid1` (`cid1`),
  KEY `idx_cid2` (`cid2`)
) 

truncate table atlas_dr3.elais_radio_pairs;

# Find pairs based on ang_sep nearest neighbour.
insert into atlas_dr3.elais_radio_pairs(cid1,cid2,ang_sep_arcsec)
select t1.id, t2.id,
       format(sqrt(pow((t1.RA-t2.RA)*cos(t1.Decl),2)+pow(t1.Decl-t2.Decl,2))*3600,6)
from atlas_dr3.elais_coords as t1, atlas_dr3.elais_coords as t2
where pow((t1.RA-t2.RA)*cos(t1.Decl),2)+
      pow(t1.Decl-t2.Decl,2) <= pow(100/3600,2)
and t1.id!=t2.id
limit 0,20000;

# now get the fluxs
# sp-peak flux
set sql_safe_updates=0;
update atlas_dr3.elais_radio_pairs as t1
   inner join atlas_dr3.elais_radio_properties as t2
   on t1.cid1=t2.id
set t1.flux1=t2.sp;

update atlas_dr3.elais_radio_pairs as t1
   inner join atlas_dr3.elais_radio_properties as t2
   on t1.cid2=t2.id
set t1.flux2=t2.sp;

update atlas_dr3.elais_radio_pairs
set flag='rd'
where flux1/flux2 > 1.0
and flux1/flux2 < 2.1
and ang_sep_arcsec/sqrt(flux1+flux2) > 2.0
and ang_sep_arcsec/sqrt(flux1+flux2) < 10.0)

# select id's and coord's for postage stamps.
select cid1, 
	        (select ra from atlas_dr3.elais_coords where id=cid1) ra1,  
                (select decl from atlas_dr3.elais_coords where id=cid1) dec1, 
	   cid2, 
                (select ra from atlas_dr3.elais_coords where id=cid2) ra2,
	        (select decl from atlas_dr3.elais_coords  where id=cid2) dec2 
from atlas_dr3.elais_radio_pairs
where flag='rd';
		  


