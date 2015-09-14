# randomcats.py
# This program makes a random catalogue based on the FUSION catalogue

def find_blanks_random():

   print "Find Blanks with the Random Catalogue"
   
   sr=100.0

   global dradian
   dradian=math.pi/180

  
#===================================================================================================
#

   print sys.argv[0],"\n"

   db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

   db.query("select count(*),max(ra),min(ra),max(decl),min(decl) from "+schema+"."+schema+"_random_catalogue;")

   r=db.use_result()

# fetch results, returning char we need float !

   rows=r.fetch_row(maxrows=1)

   for row in rows:
       ra_max=float(row[1])
       ra_min=float(row[2])
       dec_min=float(row[3])
       dec_max=float(row[4])

   print "RA Max, RA Min    : %f %f" % (ra_max,ra_min)
   print "Dec Max, Dec Min  : %f %f" % (dec_max,dec_min)

# Close connection to the database
   db.close()

   db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

# Lets run a querry, find the number of records

   db.query("select ra,decl from "+schema+"."+schema+"_random_catalogue;")

   r=db.use_result()

# fetch results, returning char we need float !

   rows=r.fetch_row(maxrows=0)

   n_blanks=0

# Close connection to the database
   db.close()
   db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

   f_radius=[]

   for row in rows:
       ra=float(row[0])
       dec=float(row[1])

       ra_min=float(ra)-float(sr/3600)
       ra_max=float(ra)+float(sr/3600)
       dec_min=float(dec)-float(sr/3600)
       dec_max=float(dec)+float(sr/3600)
    
# print the paramaters

#    print "Ra Dec  : %f %f" % (ra,dec)

       sql=("select "
         "t2.id, "
         "sqrt(pow(("+str(ra)+"-t2.RA)*cos(radians("+str(dec)+")),2)+"
         "     pow("+str(dec)+"-t2.DECL,2))*3600 as radius "
	     "from "+background_field+"."+background_field+" as t2 "
         "where pow(("+str(ra)+"-t2.RA)*cos(radians("+str(dec)+")),2)+" 
         "      pow("+str(dec)+"-t2.DECL,2) <= pow("+str(sr)+"/3600,2) "
         " and   t2.ra > "+str(ra_min)+" and t2.ra < "+str(ra_max)+" "
         " and   t2.decl > "+str(dec_min)+" and t2.decl < "+str(dec_max)+
         " order by radius asc limit 0,3000000; ")

#       print sql
       db.query(sql)
       r=db.use_result()
       count=r.fetch_row(maxrows=0)

       nm=0
	   
       for c in count:
           nm=nm+1
           radius=float(c[1])
           f_radius.append(radius)
           sys.stdout.write('.')
#          print c
           if nm==1: break
        

#    print nm

       if nm==0:
          n_blanks=n_blanks+1

   
   print "number of blanks :",n_blanks
   print f_radius
   
   (hist,bins)=numpy.histogram(f_radius,bins=int(sr),range=[0.0,sr])
   width = 0.7*(bins[1]-bins[0])
   center = (bins[:-1]+bins[1:])/2

   print hist

   # Truncate the q0 table
   db.query("truncate "+schema+"."+schema+"_q0;")

   f=open('Blanks_'+schema+'.csv','w')
   for x in xrange(0,int(sr)):
       sql3=("insert into "+schema+"."+schema+"_q0(radius,nb_random) values ('"+str(x+1)+"','"+str(hist[x])+"');")
       print sql3,"\n"
       db.query(sql3)
       db.commit()
       out_str="hist[%d] : %d \n" % (x,hist[x])
       f.write(out_str)

# Need a cumulative histogram

   for x in xrange(0,int(sr)):
       if x > 0: hist[x]=hist[x]+hist[x-1]
       sql4=("update "+schema+"."+schema+"_q0 set nr_random="+str(hist[x])+" where radius="+str(x+1)+";")
       print sql4,"\n"
       db.query(sql4)
       db.commit()

# Close connection to the database
   db.close()

   plt.bar(center, hist, align = 'center',width = width,linewidth=0)
#plt.hist(hist, bins=15, cumulative=True)
   plot_title=' Random Catalogue - Finding Blanks m(>r)'
   plt.grid('on')
   plt.title(plot_title)
   plt.ylabel('m(>r)')
   plt.xlabel('radius (arcsec)')
   plot_fname=''+schema+'_random_blanks_n_r.ps'
   output_dir='D:/temp/'
   fname=output_dir + plot_fname
   plt.savefig(fname)
   plt.show()

# Print out the histogram values
# 

#f=open('random_cats_cdfs.csv','w')
   f.write('====Cumulative Histogram====\n')
   for x in xrange(0,int(sr)):
       out_str="hist[%d] : %d \n" % (x,hist[x])
       f.write(out_str)
   f.close()



         

