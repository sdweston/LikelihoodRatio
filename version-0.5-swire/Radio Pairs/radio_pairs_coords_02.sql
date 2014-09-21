truncate table atlas_dr3.cdfs_radio_pairs;

# Find pairs based on ang_sep nearest neighbour.
insert into atlas_dr3.cdfs_radio_pairs(cid1,cid2,ang_sep_arcsec)
select t1.id, t2.id,
       format(sqrt(pow((t1.RA-t2.RA)*cos(t1.Decl),2)+pow(t1.Decl-t2.Decl,2))*3600,6)
from atlas_dr3.cdfs_coords as t1, atlas_dr3.cdfs_coords as t2
where pow((t1.RA-t2.RA)*cos(t1.Decl),2)+pow(t1.Decl-t2.Decl,2) <= pow(100/3600,2)
and t1.id!=t2.id
limit 0,20000;

# now get the fluxs
# sp-peak flux
set sql_safe_updates=0;
update atlas_dr3.cdfs_radio_pairs as t1
   inner join atlas_dr3.cdfs_radio_properties as t2
   on t1.cid1=t2.id
set t1.flux1=t2.sp;

update atlas_dr3.cdfs_radio_pairs as t1
   inner join atlas_dr3.cdfs_radio_properties as t2
   on t1.cid2=t2.id
set t1.flux2=t2.sp;

update atlas_dr3.cdfs_radio_pairs as t1
   inner join atlas_dr3.cdfs_deconv as t2
   on t1.cid1=t2.id
set t1.deconv1=t2.deconv;

update atlas_dr3.cdfs_radio_pairs as t1
   inner join atlas_dr3.cdfs_deconv as t2
   on t1.cid2=t2.id
set t1.deconv2=t2.deconv;

select * from atlas_dr3.cdfs_radio_pairs ;

update atlas_dr3.cdfs_radio_pairs
set flag='rd'
where flux1/flux2 > 1.0
and flux1/flux2 < 2.1
and ang_sep_arcsec/sqrt(flux1+flux2) > 2.0
and ang_sep_arcsec/sqrt(flux1+flux2) < 10.0;

===============================================================

# From the entries in field_radio_pairs
# add new entries into tables coords and radio_properties
# sum errors in quadrature

select cid1, 
	        (select ra from atlas_dr3.cdfs_coords where id=cid1) as ra1,  
            (select decl from atlas_dr3.cdfs_coords where id=cid1) as dec1, 
	   cid2, 
            (select ra from atlas_dr3.cdfs_coords where id=cid2) as ra2,
	        (select decl from atlas_dr3.cdfs_coords  where id=cid2) as dec2 ,
       ((select ra from atlas_dr3.cdfs_coords where id=cid1)+(select ra from atlas_dr3.cdfs_coords where id=cid2))/2 as ra,
       ((select decl from atlas_dr3.cdfs_coords where id=cid1)+(select decl from atlas_dr3.cdfs_coords where id=cid2))/2 as decl
from atlas_dr3.cdfs_radio_pairs
where flag='rd';

insert into atlas_dr3.cdfs_coords 
(id, ra, decl, ra_err, decl_err)
select id,
       ((select ra from atlas_dr3.cdfs_coords where id=cid1)+(select ra from atlas_dr3.cdfs_coords where id=cid2))/2 ,
       ((select decl from atlas_dr3.cdfs_coords where id=cid1)+(select decl from atlas_dr3.cdfs_coords where id=cid2))/2,
	   sqrt(power((select ra_err from atlas_dr3.cdfs_coords where id=cid1),2)+power((select ra_err from atlas_dr3.cdfs_coords where id=cid2),2)),
	   sqrt(power((select decl_err from atlas_dr3.cdfs_coords where id=cid1),2)+power((select decl_err from atlas_dr3.cdfs_coords where id=cid2),2))
from atlas_dr3.cdfs_radio_pairs
where flag='rd';

insert into atlas_dr3.cdfs_radio_properties
(id,snr,rms,sp,sint,sp_err,sint_err)
select id,
       sqrt(power((select snr from atlas_dr3.cdfs_radio_properties where id=cid1),2)+power((select snr from atlas_dr3.cdfs_radio_properties where id=cid2),2)),
	   sqrt(power((select rms from atlas_dr3.cdfs_radio_properties where id=cid1),2)+power((select rms from atlas_dr3.cdfs_radio_properties where id=cid2),2)),
	   (flux1+flux2)/2,
       ((select sint from atlas_dr3.cdfs_radio_properties where id=cid1)+(select sint from atlas_dr3.cdfs_radio_properties where id=cid2))/2,
	   sqrt(power((select sp_err from atlas_dr3.cdfs_radio_properties where id=cid1),2)+power((select sp_err from atlas_dr3.cdfs_radio_properties where id=cid2),2)),
	   sqrt(power((select sint_err from atlas_dr3.cdfs_radio_properties where id=cid1),2)+power((select sint_err from atlas_dr3.cdfs_radio_properties where id=cid2),2))
from atlas_dr3.cdfs_radio_pairs
where flag='rd';

# Need SQL to backout these updates for radio doubles.

# first delete entries from coords

# delete entries from radio_properties

# truncate the radio pairs table ready for another run

select 	