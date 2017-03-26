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
import sys

schema="atlas_dr3"
field="elais"
swire_schema='swire_es1'
sr="100.0"

# Connect to the local database with the atlas uid

db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

sql1=("SELECT id,ra,decl FROM "+schema+"."+field+"_coords;")
db.query(sql1)

r=db.use_result()

# fetch results, returning char we need float !
rows=r.fetch_row(maxrows=0)
db.close()

nir=0

for row in rows:
    ra=row[1]
    decl=row[2]
#    print ra,decl

# now find all the ir sources within search radius

# Connect to the local database with the atlas uid

    db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")
    
    sql2=("select count(*) "
         "from "+swire_schema+".es1_swire as t2 "
         "where pow(("+str(ra)+"-t2.RA_SPITZER)*cos(radians("+str(decl)+")),2)+" 
         "pow("+str(decl)+"-t2.DEC_SPITZER,2) <= pow("+str(sr)+"/3600,2); ")

    db.query(sql2)

    c=db.use_result()
    count=c.fetch_row(maxrows=0)

    for row in count:
        nir=nir+int(row[0])
        sys.stdout.write('.')
#        print row[0],nir

    db.close()

print nir
    


