#===========================================================================
#
# ir_density.py
#
# Python script to query SWIRE_ES1 mysql database to determine the
# density of IR sources around each Radio Source.
#
#===========================================================================
#
# S. Weston
# AUT University
# March 2014
#===========================================================================

import _mysql

schema="atlas_dr3"
field="cdfs"

# Connect to the local database with the atlas uid

db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

sql1=("SELECT id,ra,decl FROM "+schema+"."+field+"_coords;")

r=db.use_result()

# fetch results, returning char we need float !
rows=r.fetch_row(maxrows=1)
print rows

for row in rows:
    ra=row[1]
    decl=row[2]
    print ra,decl
    
# Close connection to the database
db.close()   


