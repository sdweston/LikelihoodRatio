SELECT cid,swire_index_spitzer,max(reliability) FROM atlas_dr3.elais_matches;


group by cid;

create table if not exists atlas_dr3.elais_t2 as (
select t1.cid, t1.swire_index_spitzer, t1.reliability
from atlas_dr3.elais_matches as t1
inner join(
    select cid, max(reliability) reliability
    from atlas_dr3.elais_matches
    group by cid
) ss on t1.cid = ss.cid and t1.reliability = ss.reliability);

select t1.cid, t1.swire_index_spitzer, t2.ra, t2.decl, t3.ra_spitzer, t3.dec_spitzer, t1.reliability
from atlas_dr3.elais_t2 as t1, atlas_dr3.elais_coords as t2, fusion.swire_elais as t3
where t1.cid=t2.id
and t1.swire_index_spitzer=t3.index_spitzer;

drop table atlas_dr3.cdfs_t2;
create table if not exists atlas_dr3.cdfs_t2 as (
select t1.cid, t1.swire_index_spitzer, t1.reliability, t1.p_not
from atlas_dr3.cdfs_matches as t1
inner join(
    select cid, max(reliability) reliability
    from atlas_dr3.cdfs_matches
    group by cid
) ss on t1.cid = ss.cid and t1.reliability = ss.reliability);

select t1.cid "ATLAS ID", t2.ra, t2.decl, t4.sp "Peak Radio Flux", t4.sint "Integrated Radio Flux", 
	   t1.swire_index_spitzer, t3.ra_spitzer, t3.dec_spitzer,
       t3.irac_3_6_micron_flux_mujy, t3.irac_3_6_micron_flux_error_mujy, t1.reliability, t1.p_not
from atlas_dr3.cdfs_t2 as t1, atlas_dr3.cdfs_coords as t2, fusion.swire_cdfs as t3,
	 atlas_dr3.cdfs_radio_properties as t4
where t1.cid=t2.id
and t1.swire_index_spitzer=t3.index_spitzer
and t1.cid=t4.id;


drop table atlas_dr3.elais_t2;
create table if not exists atlas_dr3.elais_t2 as (
select t1.cid, t1.swire_index_spitzer, t1.reliability, t1.p_not
from atlas_dr3.elais_matches as t1
inner join(
    select cid, max(reliability) reliability
    from atlas_dr3.elais_matches
    group by cid
) ss on t1.cid = ss.cid and t1.reliability = ss.reliability);

%====

Need to merge the output of these two into one !

select t1.cid , format(t2.ra,4) "RA", format(t2.decl,4) "Dec", t4.sp "Peak Radio Flux", t4.sint "Integrated Radio Flux", 
	   t1.swire_index_spitzer, format(t3.ra_spitzer,4) "IR RA", format(t3.dec_spitzer,4) "IR Dec",
       t3.irac_3_6_micron_flux_mujy, t3.irac_3_6_micron_flux_error_mujy, format(t1.reliability,4) "Reliability", format(t1.p_not,4) "P_Not"
from atlas_dr3.elais_t2 as t1, atlas_dr3.elais_coords as t2, fusion.swire_elais as t3,
	 atlas_dr3.elais_radio_properties as t4
where t1.cid=t2.id
and t1.swire_index_spitzer=t3.index_spitzer
and t1.cid=t4.id;

SELECT t1.cid, t3.ra, t3.decl, t2.sp , t2.sint, t1.swire_index_spitzer,
	t4.ra_spitzer, t4.dec_spitzer,
       t4.irac_3_6_micron_flux_mujy, t4.irac_3_6_micron_flux_error_mujy,
	t1.reliability
FROM atlas_dr3.elais_matches t1, atlas_dr3.elais_radio_properties as t2, atlas_dr3.elais_coords as t3, fusion.swire_elais as t4
where t1.reliability is null
and t1.swire_index_spitzer=t4.index_spitzer
and t1.cid=t2.id
and t1.cid=t3.id;

% also add ir doubles

%====

select t1.cid , format(t2.ra,4) "RA", format(t2.decl,4) "Dec", t4.sp "Peak Radio Flux", t4.sint "Integrated Radio Flux", 
	   t1.swire_index_spitzer, format(t3.ra_spitzer,4) "IR RA", format(t3.dec_spitzer,4) "IR Dec",
       t3.irac_3_6_micron_flux_mujy, t3.irac_3_6_micron_flux_error_mujy, format(t1.reliability,4) "Reliability", format(t1.p_not,4) "P_Not"
from atlas_dr3.cdfs_t2 as t1, atlas_dr3.cdfs_coords as t2, fusion.swire_cdfs as t3,
	 atlas_dr3.cdfs_radio_properties as t4
where t1.cid=t2.id
and t1.swire_index_spitzer=t3.index_spitzer
and t1.cid=t4.id;

