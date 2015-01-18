# we want to find all candidates with the highest reliability (if more than 1 NN) no matter what
# there reliability value.

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
