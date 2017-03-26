import math
import array
import _mysql
import numpy
import scipy
import matplotlib.pyplot as plt
import astropysics as astro
import pylab
import sys

answer="no"

db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

while (answer != "exit" ) :
 
     # ask which id to delete 
     answer=raw_input('Which ID to delete ?')
     print "\nentered : ",answer,"\n"
     
     sql1=("delete from atlas_dr3.cdfs_coords where id='"+answer+"'")
     print sql1	 
     db.query(sql1)

     sql2=("delete from atlas_dr3.cdfs_deconv where id='"+answer+"'")
     print sql2	 
     db.query(sql2)

     sql3=("delete from atlas_dr3.cdfs_name where id='"+answer+"'")
     print sql3	 
     db.query(sql3)

     sql4=("delete from atlas_dr3.cdfs_radio_properties where id='"+answer+"'")
     print sql4	 
     db.query(sql4)

     sql5=("delete from atlas_dr3.cdfs_sindex where id='"+answer+"'")
     print sql5	 
     db.query(sql5)
	 
# Close connection to the database
db.close()
