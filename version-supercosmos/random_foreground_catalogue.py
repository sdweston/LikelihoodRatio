# random_foreground_catalogue.py
# This program makes a random catalogue based on the foreground sparse catalogue, 
# the one to be XID's with the more abundant background.
#
# As per Bonzini et al, 2012

def random_foreground_catalogue():

   offset=0.0

#===================================================================================================
#

   db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

# Lets run a querry, find the number of records

#db.query("select count(*),max(ra_12),min(ra_12),max(dec_12),min(dec_12) from fusion.cdfs;")
   db.query("select count(*),max(ra_2000),min(ra_2000),max(decl_2000),min(decl_2000) from nvss_gama12.nvss_gama12;")

   r=db.use_result()

# fetch results, returning char we need float !

   rows=r.fetch_row(maxrows=1)

   for row in rows:
    source_count=int(row[0])
    ra_max=float(row[1])+offset
    ra_min=float(row[2])+offset
    dec_min=float(row[3])
    dec_max=float(row[4])

# print the paramaters

   print "Number of sources : %d" % source_count
   print "RA Max, RA Min    : %f %f" % (ra_max,ra_min)
   print "Dec Max, Dec Min  : %f %f" % (dec_max,dec_min)

# Close connection to the database

   db.close()
   db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")
   db.query("set autocommit=0;")

# open a new catalogue file

#f=open('random_cats_cdfs.csv','w')
   f=open('RandomCat_gama12.csv','w')

   commit=0
   print "Commit: "

# Truncate the random catalogue table
   db.query("truncate gama12.gama12_random_catalogue;")

#for x in range(0,source_count):
   for x in range(0,source_count):
         fake_ra=random.uniform(ra_min,ra_max)
         fake_dec=random.uniform(dec_min,dec_max)
         # create a source id
         id_str="R%d" % x
         out_str="%s,%f,%f\n" % (id_str,fake_ra,fake_dec)
         f.write(out_str)
         db.query("insert into gama12.gama12_random_catalogue(id,ra,decl) values ('%s','%f','%f');" % (id_str,fake_ra,fake_dec))
         commit=commit+1
         if commit==1000:
             commit=0
             db.commit()
             sys.stdout.write('.')

            
         
   sys.stdout.write('\n')
   db.commit()
   f.close()

# Close connection to the database

   db.close()
         

