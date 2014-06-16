global Q0

# Connect to the local database with the atlas uid

db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")
	
# Put sigma_radio into the working table, so don't have to re-run this each time

sql_get_q0=("select q0 from atlas_dr3.atlas_dr3_working "
                   " where field like '"+field+"';")
print sql_get_q0,"\n"
db.query(sql_get_q0)
	
r=db.use_result()

# fetch results, returning char we need float !

rows=r.fetch_row(maxrows=1)
for row in rows:
    Q0=float(row[0])
	
db.close()