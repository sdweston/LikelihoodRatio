#===========================================================================
#
# likelihoodratio.py
#
# Python script to query mysql database to determine the
# LR the likelihood ratio.
#
#===========================================================================
#
# S. Weston
# AUT University
# March 2013
#===========================================================================

def lr():

    print "\nStarting LR calculations and db updates"

# Connect to the local database with the atlas uid

    db=_mysql.connect(host=db_host,user=db_user,passwd=db_passwd)

# Lets run a querry

    db.query("select nvss_id,supercosmos_id,f_r,flux from "+schema+"."+schema+"_matches \
              where f_r is not null and flux > 0;")
          
# store_result() returns the entire result set to the client immediately.
# The other is to use use_result(), which keeps the result set in the server 
#and sends it row-by-row when you fetch.

#r=db.store_result()
# ...or...
    r=db.use_result()

# fetch results, returning char we need float !

    rows=r.fetch_row(maxrows=10000)

# rows is a tuple, convert it to a list

    print "    Calculate LR Update database with LR values"

#print rows

    for row in rows:
        index_foreground=row[0]
        index_background=row[1]
        f_r=float(row[2])
        flux=float(row[3])
#        print "Flux %f" %flux
        sys.stdout.write('.')

#   check lookup table for values of q(m) and n(m)
	
#        log10_f=math.log10(flux)
# we are working  B_J Photographic Magnitude, no need to log it !
	
        sql1=("select log10_f,n_m,q_m from "+schema+"."+schema+"_n_m_lookup "
              "    where log10_f between "+str(flux)+" - 0.2125 and  "+str(flux)+" + 0.2125;")
 			  
# where log10_f between 17.541-0.2125 and 17.541+0.2125;
	
#        print sql1,"\n" 
        db.query(sql1)
        r2=db.store_result()
        strings=r2.fetch_row(maxrows=1)

#    print log10_f,strings

        for string in strings:
            n_m=float(string[1])
            q_m=float(string[2])         

#            print "n(m) %20.9f q(m) %20.9f f(r) %20.9f \n" % (n_m, q_m, f_r)
              
#        lr = (q_m * f_r) / (n_m / atlas_sqasec)
            if n_m != 0.0:
			
               lr = (q_m * f_r) / (n_m)
        
#   print "Likelihood Ratio : %f " % lr
    
#   update table with likelihood ratio.

               db.query("update "+schema+"."+schema+"_matches set lr=%s where nvss_id='%s' \
                  and supercosmos_id='%s';" % (lr, index_foreground, index_background))

# End of do block

# Close connection to the database
    db.close()

    print "End"


