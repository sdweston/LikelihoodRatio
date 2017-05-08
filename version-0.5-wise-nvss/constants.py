# Database 
global db_host
db_host='localhost'
global db_user
db_user='atlas'
global db_passwd
db_passwd='atlas'
global schema
schema='wise'

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

# Number of bins to use for the n_m_lookup values
# Might have to adjust nbins to get the best for the real_m & total_m calculations for your catalogue,
# also minimize empty bins. We did have nbins=40 but not good.

global nbins
nbins=20
