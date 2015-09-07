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

sql1=("SELECT count(distinct(nvss_id)) FROM "+schema+"."+schema+"_matches;")
print sql1
db.query(sql1)
r=db.store_result()
rows=r.fetch_row(maxrows=1)
for row in rows:
    nrs=float(row[0])
    print "    Number of Radio Sources : ",nrs


db.close()