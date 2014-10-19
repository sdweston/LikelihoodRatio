SELECT * FROM atlas_dr3.cdfs_matches
where reliability > 0.8

truncate table atlas_dr3.cdfs_q0;

select * from atlas_dr3.cdfs_q0;

truncate table atlas_dr3.ozdes_c1;
create table atlas_dr3.ozdes_c3 as (select * from atlas_dr3.ozdes_c1);


LOAD DATA LOCAL INFILE 'd:/cdfs/c3.txt' INTO TABLE atlas_dr3.ozdes_c3 FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
(id, ra, decl)