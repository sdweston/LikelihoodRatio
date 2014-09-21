global sigma_radio

# Connect to the local database with the atlas uid

db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")
	
# Put sigma_radio into the working table, so don't have to re-run this each time

sql_get_sigma=("select sigma from atlas_dr3.atlas_dr3_working "
                   " where field like '"+field+"';")
print sql_get_sigma,"\n"
db.query(sql_get_sigma)
	
r=db.use_result()

# fetch results, returning char we need float !

rows=r.fetch_row(maxrows=1)
for row in rows:
    sigma_radio=float(row[0])
	
db.close()