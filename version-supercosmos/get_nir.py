global nir

#    db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")
db=_mysql.connect(host=db_host,user=db_user,passwd=db_passwd)

# Lets run a querry to find the number of radio sources.

sql1=("SELECT count(*) FROM "+background_field+"."+background_field+";")
print sql1
db.query(sql1)
r=db.store_result()
rows=r.fetch_row(maxrows=1)
for row in rows:
    nir=float(row[0])
    print "    Number of Background Sources : ",nir


db.close()