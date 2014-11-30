truncate table atlas_dr3.elais_coords;

insert into atlas_dr3.elais_coords (id,ra,ra_err,decl,decl_err)
select id,ra,ra_err,decl,decl_err
from atlas_dr3.elais_cmpcat_24nov2014;

truncate table atlas_dr3.elais_name;

insert into atlas_dr3.elais_name (id,name)
select id,name
from atlas_dr3.elais_cmpcat_24nov2014;

truncate table atlas_dr3.elais_deconv;

insert into atlas_dr3.elais_deconv (id,deconv,deconv_err)
select id,deconv,deconv_err
from atlas_dr3.elais_cmpcat_24nov2014;

truncate table atlas_dr3.elais_sindex;

insert into atlas_dr3.elais_sindex (id,sindex,sindex_err)
select id,sindex,sindex_err
from atlas_dr3.elais_cmpcat_24nov2014;

truncate table atlas_dr3.elais_radio_properties;

insert into atlas_dr3.elais_radio_properties (id,rms,bws,sp,sp_err,sint,sint_err,obs_freq)
select id,rms,bws,sp,sp_err,sint,sint_err,obs_freq
from atlas_dr3.elais_cmpcat_24nov2014;