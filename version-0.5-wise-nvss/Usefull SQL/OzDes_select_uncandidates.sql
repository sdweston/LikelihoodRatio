SELECT t1.cid, t3.ra, t3.decl, t2.sp , t2.sint, t1.swire_index_spitzer,
	t4.ra_spitzer, t4.dec_spitzer,
       t4.irac_3_6_micron_flux_mujy, t4.irac_3_6_micron_flux_error_mujy,
	t1.reliability
FROM atlas_dr3.elais_matches t1, atlas_dr3.elais_radio_properties as t2, atlas_dr3.elais_coords as t3, fusion.swire_elais as t4
where t1.reliability is null
and t1.swire_index_spitzer=t4.index_spitzer
and t1.cid=t2.id
and t1.cid=t3.id;

group by cid;

SELECT t1.cid, t3.ra, t3.decl, t2.sp , t2.sint, t1.reliability
FROM atlas_dr3.cdfs_matches t1, atlas_dr3.cdfs_radio_properties as t2, atlas_dr3.cdfs_coords as t3
where t1.reliability is null
and t1.cid=t2.id
and t1.cid=t3.id
group by cid;