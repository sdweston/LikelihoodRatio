#===========================================================================
#
# area_quad_slf.py
#
# Python script to query SWIRE_ES1 mysql database to determine the
# area of the survey for a arbitrary quadrilateral using Shoelace formula.
#
#===========================================================================
#
# S. Weston
# AUT University
# March 2013
#===========================================================================

import _mysql

# Connect to the local database with the atlas uid

db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

# Querry the table to get the x1,y1 x2,y2 x3,y3 and x4,y4 coords
# x1,y1
db.query("select ra_spitzer,dec_spitzer \
          from swire_es1.es1_swire \
          where ra_spitzer=(select min(ra_spitzer) from swire_es1.es1_swire) ;")

r=db.use_result()

# fetch results, returning char we need float !
rows=r.fetch_row(maxrows=1)
print rows

for row in rows:
    x1=float(row[0])
    y1=float(row[1])
    print x1,y1
    
# Close connection to the database
db.close()   

# x2,y2
# Connect to the local database with the atlas uid
db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

db.query("select ra_spitzer,dec_spitzer \
          from swire_es1.es1_swire \
          where dec_spitzer=(select min(dec_spitzer) from swire_es1.es1_swire) ;")
		  
r=db.use_result()

# fetch results, returning char we need float !
rows=r.fetch_row(maxrows=1)
print rows

for row in rows:
    x2=float(row[0])
    y2=float(row[1])
    print x2,y2

# Close connection to the database
db.close()   

# x3,y3
# Connect to the local database with the atlas uid
db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

db.query("select ra_spitzer,dec_spitzer \
          from swire_es1.es1_swire \
          where ra_spitzer=(select max(ra_spitzer) from swire_es1.es1_swire) ;")

r=db.use_result()

# fetch results, returning char we need float !
rows=r.fetch_row(maxrows=1)
print rows

for row in rows:
    x3=float(row[0])
    y3=float(row[1])
    print x3,y3
    
# Close connection to the database
db.close()   

# x4,y4
# Connect to the local database with the atlas uid
db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

db.query("select ra_spitzer,dec_spitzer \
          from swire_es1.es1_swire \
          where dec_spitzer=(select max(dec_spitzer) from swire_es1.es1_swire) ;")

r=db.use_result()

# fetch results, returning char we need float !
rows=r.fetch_row(maxrows=1)
print rows

for row in rows:
    x4=float(row[0])
    y4=float(row[1])
    print x4,y4
    
# Close connection to the database
db.close()   

# Area_Quad Shoelace Formula
# Area_Quad = 1/2 | x1.y2 + x2.y3 + x3.y4 + x4.y1 - x2.y1 - x3.y2 - x4.y3 - x1.y4 |

area_quad=(x1*y2 + x2*y3 + x3*y4 + x4*y1 - x2*y1 - x3*y2 - x4*y3 - x1*y4)/2

print "Area square degrees : %f" % area_quad

area_arcsec=area_quad*(3600**2)
print "Area square arcsec  : %f" % area_arcsec

