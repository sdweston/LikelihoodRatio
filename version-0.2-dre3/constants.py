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
sr=15.0

# Number of radio sources in radio catalogue
# What is the definition of NRS ? Number of radio sources with a match, or the total number of radio sources.
#   nrs=SELECT count(distinct elais_s1_cid) FROM elais_s1.matches;

global nrs

#db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

#db.query("SELECT count(distinct elais_s1_cid) FROM elais_s1.matches;")
#r=db.store_result()
#rows=r.fetch_row(maxrows=1)
#for row in rows:
#nrs=int(row[0])
		
#print "Number of Radio Sources : ",nrs

#db.close()


# Q probability that real counterpart is above
# the detection limit

#Q=0.8
# This is now calculated in q_0.py (D.J.B. Smith et al, 2010)

# Location to put plot files etc

global output_dir
output_dir='d:/temp/'

# Sum of Real(m)_i
global sum_real_m
sum_real_m=0.0
