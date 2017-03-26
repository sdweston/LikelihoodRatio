global nir

# Connect to the local database with the atlas uid

db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")
	
# Put nir into the working table, so don't have to re-run this each time

sql_get_nir=("select nir from atlas_dr3.atlas_dr3_working "
                   " where field like '"+field+"';")
print sql_get_nir,"\n"
db.query(sql_get_nir)
	
r=db.use_result()

# fetch results, returning char we need float !

rows=r.fetch_row(maxrows=1)
for row in rows:
    nir=int(row[0])
	
db.close()