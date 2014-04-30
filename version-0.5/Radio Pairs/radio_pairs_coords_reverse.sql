# Need SQL to backout these updates for radio doubles.

# first delete entries from coords

delete from atlas_dr3.cdfs_coords 
where id not like "C%";

# delete entries from radio_properties

delete from atlas_dr3.cdfs_radio_properties
where id not like 'C%';

# truncate the radio pairs table ready for another run

truncate table atlas_dr3.cdfs_radio_pairs;

