import array
import _mysql
import numpy
import math
import sys
import os

# ask which field to process
answer=raw_input('Which field cdfs/elais ?')
print "\nentered : ",answer,"\n"

# open file for writing

filename="d:/temp/" +answer+ "_ird.txt"
f = open(filename,'w')

# Connect to the local database with the atlas uid

db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

# Preperation, truncate tables etc

sql00=("truncate table atlas_dr3."+answer+"_ird_ozdes;")
db.query(sql00)


# Find the possible IR multiples, from those radio sources with more than one IR candidate
# between the reliability figures.

#sql1="create temporary table if not exists atlas_dr3."+answer+"_ird as ( \
#          select cid,swire_index_spitzer,reliability \
#          from atlas_dr3."+answer+"_matches  \
#          where reliability > 0.3 and reliability < 0.7) ;"

#sql0="drop table atlas_dr3."+answer+"_ird;"
#db.query(sql0)

sql1="select t1.cid,t3.ra,t3.decl,t4.sint,t1.swire_index_spitzer,t2.ra_spitzer,t2.dec_spitzer,t2.irac_3_6_micron_flux_mujy,t1.reliability \
          from atlas_dr3."+answer+"_ird as t1, \
          fusion.swire_"+answer+" as t2, \
          atlas_dr3."+answer+"_coords as t3, \
          atlas_dr3."+answer+"_radio_properties as t4 \
          where t1.swire_index_spitzer=t2.index_spitzer \
          and t1.cid=t3.id \
          and t1.cid=t4.id \
          order by t1.cid;"
 		  
#print sql1,"\n"
db.query(sql1)          

r2=db.use_result()

# fetch results, returning char we need float !

rows=r2.fetch_row(maxrows=0)

for row in rows:
    cid1=row[0]
    ra1=row[1]
    dec1=row[2]
    fusion_id=row[4]
    ra2=row[5]
    dec2=row[6]
#    print row,"\n"

    sql4="select id,ra,decl, \
              pow((ra-"+row[5]+")*cos(radians(decl)),2)+pow(decl-"+row[6]+",2) as rs, \
              z \
              from ozdes.ozdes_grc_2016_02_25 \
              where \
              pow((ra-"+row[5]+")*cos(radians(decl)),2)+pow(decl-"+row[6]+",2) <= pow(2/3600,2) \
              order by rs asc \
              limit 1;"

#    print sql4,"\n"
    db.query(sql4)

    r4=db.use_result()

# fetch results, returning char we need float !

    ozdess=r4.fetch_row(maxrows=0)

    for ozdes in ozdess:
            id=ozdes[0]
            ra=ozdes[1]
            dec=ozdes[2]
            ang_sep=math.sqrt(float(ozdes[3]))*3600
            z=ozdes[4]
            print "ozdes :",cid1," ",fusion_id," ",ra2," ",dec2," ",id," ",ra," ",dec," ",z," ",ang_sep

# Insert this row into table "field"_ird_ozdes, truncate table outside loop first

#            sql3=("insert into "+schema+"."+field+"_ird_ozdes(cid,ozdes_id,ra,decl) \
#            sql3=("insert into atlas_dr3."+answer+"_ird_ozdes(cid,ozdes_id,ra,decl) \
#                   values ('"+cid1+"','"+id+"',"+ra+","+dec+");")
#            print sql3
#            db.query(sql3)

#    print "\n"
			  
# Print out the OzDES id, ra, dec and Z

# Close connection to the database
db.close()

# close open file

f.close()


