select max(ra_opt),min(ra_opt),max(dec_opt),min(dec_opt)
from  hsn2014.ecdfs_phz_best_ctp;

create table hsn2014.nn as
select t1.id_12,t1.ra_12,t1.dec_12,t1.redshift,t2._hsn2014_,t2.ra_opt,t2.dec_opt,t2.specz,t2.photoz
from fusion.cdfs t1, hsn2014.ecdfs_phz_best_ctp as t2
where pow((t1.ra_12-t2.ra_opt)*cos(radians(t1.dec_12)),2)+pow(t1.dec_12-t2.dec_opt,2) <= pow(1/3600,2) 
      and   t1.ra_12 > 52.8 and t1.ra_12 < 53.4
      and   t1.dec_12 > -28.10 and t1.dec_12 < -27.55
limit 0,3000000; 

select t1.id_12,t1.ra_12,t1.dec_12,t1.redshift,t2._hsn2014_,t2.ra_opt,t2.dec_opt,t2.specz,t2.photoz
from fusion.cdfs t1, hsn2014.ecdfs_phz_best_ctp as t2
where pow((t1.ra_12-t2.ra_opt)*cos(radians(t1.dec_12)),2)+pow(t1.dec_12-t2.dec_opt,2) <= pow(2/3600,2) 
      and   t1.ra_12 > 52.8 and t1.ra_12 < 53.4
      and   t1.dec_12 > -28.10 and t1.dec_12 < -27.55
limit 0,3000000; 

select t2.cid,t1.id_12,t1.specz,t1.photoz,t2.swire_index_spitzer, t2.reliability, t2.flux, t3.id, t3.sp,t3.sint
from hsn2014.nn as t1, atlas_dr3.cdfs_matches as t2, atlas_dr3.cdfs_radio_properties as t3
where t1.id_12=t2.swire_index_spitzer
and t2.reliability > 0.8
and t3.id=t2.cid

select t2.cid,t1.id_12,t1.specz,t1.photoz,t2.swire_index_spitzer, t2.reliability, t2.flux, t3.id, t3.sp,t3.sint
from hsn2014.nn as t1, atlas_dr3.cdfs_matches as t2, atlas_dr3.cdfs_radio_properties as t3
where t1.id_12=t2.swire_index_spitzer
and t3.id=t2.cid

