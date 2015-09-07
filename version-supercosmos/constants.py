# Database 
global db_host
db_host='localhost'
global db_user
db_user='atlas'
global db_passwd
db_passwd='atlas'

# None radio source catalog area
# arc_sec ^ 2
# Calulated in area_none_radio_survey
global area_nr

# Assume a % of area lost due to contamination from forground stars in the
# none radio catalogue.
global area_pct
area_pct=0.03

# Search Radius, arc sec
global sr

# Location to put plot files etc
global output_dir
output_dir='d:/temp/'

# Sum of Real(m)_i
global sum_real_m
sum_real_m=0.0

# Schema Information
global schema
schema='gama12' 
global foreground_field
foreground_field='nvss_gama12'
global background_field
background_field='supercosmos_gama12'

# NVSS Beam, arcsec
global beam_maj
beam_maj=45.0
global beam_min
beam_min=45.0

# Supercosmos
global sc_ra_min
sc_ra_min=174.138458333
global sc_ra_max
sc_ra_max=186.185083333
global sc_dec_min
sc_dec_min=-2.08702777778
global sc_dec_max
sc_dec_max=1.94011111111

# n(m)
global sr_out
sr_out=200
