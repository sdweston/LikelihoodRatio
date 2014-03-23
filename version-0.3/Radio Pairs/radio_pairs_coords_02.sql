select cid,ra_deg,dec_deg 
from ecdfs.coords
where cid  in (select cid1 
from ecdfs.radio_pairs
where flux1/flux2 > 1.0
and flux1/flux2 < 2.1
and ang_sep_arcsec/sqrt(flux1+flux2) > 2.0
and ang_sep_arcsec/sqrt(flux1+flux2) < 10.0);

select cid1 , 
       (select ra_deg from ecdfs.coords where cid=cid1) ra1,
	   (select dec_deg from ecdfs.coords where cid=cid1) dec1,
       cid2,
       (select ra_deg from ecdfs.coords where cid=cid2) ra2,
	   (select dec_deg from ecdfs.coords where cid=cid2) dec2
from ecdfs.radio_pairs
where flux1/flux2 > 1.0
and flux1/flux2 < 2.1
and ang_sep_arcsec/sqrt(flux1+flux2) > 2.0
and ang_sep_arcsec/sqrt(flux1+flux2) < 10.0

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
(id, ra, decl)
select id,
       ((select ra from atlas_dr3.cdfs_coords where id=cid1)+(select ra from atlas_dr3.cdfs_coords where id=cid2))/2 ,
       ((select decl from atlas_dr3.cdfs_coords where id=cid1)+(select decl from atlas_dr3.cdfs_coords where id=cid2))/2 
from atlas_dr3.cdfs_radio_pairs
where flag='rd';

insert into atlas_dr3.cdfs_radio_properties
(id,sp,sint)
select id,(flux1+flux2)/2,
       ((select sint from atlas_dr3.cdfs_radio_properties where id=cid1)+(select sint from atlas_dr3.cdfs_radio_properties where id=cid2))/2
from atlas_dr3.cdfs_radio_pairs
where flag='rd';

# Need SQL to backout these updates for radio doubles.

# first delete entries from coords

# delete entries from radio_properties

# truncate the radio pairs table ready for another run

select 	