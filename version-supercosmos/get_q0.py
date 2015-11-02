global Q0

# Connect to the local database with the atlas uid

db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")
	
# Put sigma_radio into the working table, so don't have to re-run this each time

sql_get_q0=("select q0 from gama12.gama12_working "
                   " where field like 'gama12';")
print sql_get_q0,"\n"
db.query(sql_get_q0)
	
r=db.use_result()

# fetch results, returning char we need float !

rows=r.fetch_row(maxrows=1)
for row in rows:
    Q0=float(row[0])
    str_q0=row[0]
	
db.close()

# Allow a user input for Q0, if not given then take the calculated value from the database.

answer=raw_input('Value for Q_0 ('+str_q0+') : ')
if answer!='':
   Q0=float(answer)
   
print "Q0 : ",Q0