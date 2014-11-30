truncate table atlas_dr3.cdfs_coords;

insert into atlas_dr3.cdfs_coords (id,ra,ra_err,decl,decl_err)
select id,ra,ra_err,decl,decl_err
from atlas_dr3.cdfs_cmpcat_24nov2014;

truncate table atlas_dr3.cdfs_name;

insert into atlas_dr3.cdfs_name (id,name)
select id,name
from atlas_dr3.cdfs_cmpcat_24nov2014;

truncate table atlas_dr3.cdfs_deconv;

insert into atlas_dr3.cdfs_deconv (id,deconv,deconv_err)
select id,deconv,deconv_err
from atlas_dr3.cdfs_cmpcat_24nov2014;

truncate table atlas_dr3.cdfs_sindex;

insert into atlas_dr3.cdfs_sindex (id,sindex,sindex_err)
select id,sindex,sindex_err
from atlas_dr3.cdfs_cmpcat_24nov2014;

truncate table atlas_dr3.cdfs_radio_properties;

insert into atlas_dr3.cdfs_radio_properties (id,rms,bws,sp,sp_err,sint,sint_err,obs_freq)
select id,rms,bws,sp,sp_err,sint,sint_err,obs_freq
from atlas_dr3.cdfs_cmpcat_24nov2014;