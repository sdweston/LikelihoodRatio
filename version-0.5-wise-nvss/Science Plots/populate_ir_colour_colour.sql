select * from  atlas_dr3.elais_ir_colour_colour;

create table atlas_dr3.elais_ir_colour_colour
SELECT t1.swire_index_spitzer, t1.cid,  
             t3.sp,
             t3.sint,
             t2.redshift,
			 -2.5*log10(t2.irac_4_5_micron_flux_mujy/t2.irac_8_0_micron_flux_mujy) as s45_s80,
			 -2.5*log10(t2.irac_3_6_micron_flux_mujy/t2.irac_5_8_micron_flux_mujy) as s36_s58,
			 -2.5*log10(t2.irac_3_6_micron_flux_mujy/t2.irac_4_5_micron_flux_mujy) as s36_s45,
			 -2.5*log10(t2.irac_5_8_micron_flux_mujy/t2.irac_8_0_micron_flux_mujy) as s58_s80,
             (t3.sp*1000)/t2.irac_3_6_micron_flux_mujy as s14_s36
from atlas_dr3.elais_matches t1, fusion.swire_elais t2, atlas_dr3.elais_radio_properties t3 
           where t1.swire_index_spitzer=t2.index_spitzer 
           and t1.cid=t3.id  
           and t1.lr > 0.01
           and t1.reliability > 0.1
           and t1.reliability > t1.lr/(0.109+(t1.lr/(0.5+0.4)))
           and t2.irac_3_6_micron_flux_mujy > 0
           and t2.irac_4_5_micron_flux_mujy > 0
           and t2.irac_5_8_micron_flux_mujy > 0
           and t2.irac_8_0_micron_flux_mujy > 0
;