insert into atlas_dr3.elais_coords
select id,ra,ra_err,decl,decl_err from atlas_dr3.elais_cmpcat;

truncate atlas_dr3.elais_deconv;
insert into atlas_dr3.elais_deconv
select id,deconv,deconv_err from atlas_dr3.elais_cmpcat;

truncate atlas_dr3.elais_name;
insert into atlas_dr3.elais_name
select id,survey,name from atlas_dr3.elais_cmpcat;

truncate atlas_dr3.elais_sindex;
insert into atlas_dr3.elais_sindex
select id,sindex,sindex_err from atlas_dr3.elais_cmpcat;

truncate atlas_dr3.elais_radio_properties;
insert into atlas_dr3.elais_radio_properties
select id,snr,rms,bws,sp,sp_err,sint,sint_err,obs_freq from atlas_dr3.elais_cmpcat;
