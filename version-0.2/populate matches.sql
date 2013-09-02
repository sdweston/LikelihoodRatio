truncate table elais_s1.matches;

set session wait_timeout=30000;
set session interactive_timeout=30000;

# we want r in arc-seconds not decimal degrees
insert into elais_s1.matches(elais_s1_cid,swire_index_spitzer,dx,dy,r_arcsec,flux)
select t1.cid,
       t2.Index_Spitzer,
	   (t1.RA_Deg-t2.RA_SPITZER)*cos(t1.Dec_Deg),
	   t1.Dec_Deg-t2.DEC_SPITZER,
	   sqrt(pow((t1.RA_Deg-t2.RA_SPITZER)*cos(t1.Dec_Deg),2)+pow(t1.Dec_Deg-t2.DEC_SPITZER,2))*3600,
	   t2.irac_3_6_micron_flux_mujy
  
from elais_s1.coords as t1, swire_es1.es1_swire as t2

where pow((t1.RA_Deg-t2.RA_SPITZER)*cos(t1.Dec_Deg),2)+
      pow(t1.Dec_Deg-t2.DEC_SPITZER,2) <= pow(10/3600,2)

and   t2.ra_spitzer > 8.0
and   t2.ra_spitzer < 9.5
and   t2.dec_spitzer < -43.0
and   t2.dec_spitzer > -44.5	  
limit 0,3000000;