global nrs

# Connect to the local database with the atlas uid

#db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")
	
# Put nir into the working table, so don't have to re-run this each time

#sql_get_nrs=("select nrs from atlas_dr3.atlas_dr3_working "
#                   " where field like '"+field+"';")
#print sql_get_nrs,"\n"
#db.query(sql_get_nrs)
	
#r=db.use_result()

# fetch results, returning char we need float !

#rows=r.fetch_row(maxrows=1)
#for row in rows:
#    n_rs=int(row[0])

#====
# if above is null, then do below and update working table
#
# Connect to the local database with the atlas uid

#    db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")
db=_mysql.connect(host=db_host,user=db_user,passwd=db_passwd)

# Lets run a querry to find the number of radio sources.

sql1=("SELECT count(distinct(cid)) FROM "+schema+"."+field+"_matches;")
db.query(sql1)
r=db.store_result()
rows=r.fetch_row(maxrows=1)
for row in rows:
    nrs=float(row[0])
#    print "    Number of Radio Sources : ",nrs

# Have to allow for over-blended objects from atlas for number of radio sources NRM
#
# First how many overblended objects - NOB
# SELECT count(*) FROM atlas_dr3.elais_coords
# where length(id) > 6;

sql1a=("SELECT count(*) FROM "+schema+"."+field+"_matches where length(cid) > 6;")
db.query(sql1a)
r=db.store_result()
rows=r.fetch_row(maxrows=1)
for row in rows:
    nob=float(row[0])
#    print "    Number of over blended components : ",nob
#
# Second group these to once source - NS
# select count(*)
# from
# (SELECT count(*) FROM atlas_dr3.elais_coords
# where length(id) > 6
# group by substr(id,1,6)) as a1;
#

sql1b=("SELECT count(*) FROM ( select count(*) from "+schema+"."+field+"_matches where length(cid) > 6 group by substr(cid,1,6)) as a1;")
db.query(sql1b)
r=db.store_result()
rows=r.fetch_row(maxrows=1)
for row in rows:
    ns=float(row[0])
#    print "    Number of blended sources : ",ns

# True_NRS=NRS - NOB + NS
# We know have catalogue with over blended sources merged, so don't need this any more		
#nrs=nrs-nob+ns
# But do we still need blended ?

print "    Number of Radio Sources : ",nrs
	
db.close()