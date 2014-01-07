#===========================================================================
#
# lr_swire_es1.py
#
# Python script to query SWIRE_ES1 mysql database to determine the
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

    db.query("select cid,swire_index_spitzer,f_r,flux from %s.matches \
              where f_r is not null and flux > -9.0;" % (field))
          
# store_result() returns the entire result set to the client immediately.
# The other is to use use_result(), which keeps the result set in the server 
#and sends it row-by-row when you fetch.

#r=db.store_result()
# ...or...
    r=db.use_result()

# fetch results, returning char we need float !

    rows=r.fetch_row(maxrows=5000)

# rows is a tuple, convert it to a list

    print "    Calculate LR Update database with LR values"

#print rows

    for row in rows:
        cid=row[0]
        index_spitzer=row[1]
        f_r=float(row[2])
        flux=float(row[3])
#    print "Flux %f" %flux
        sys.stdout.write('.')

#   check lookup table for values of q(m) and n(m)
	
        log10_f=math.log10(flux)
	
        db.query("select log10_f,n_m,q_m from %s.n_m_lookup \
                  where %s > log10_f - 0.05 \
                  and %s < log10_f + 0.05;" % (swire_schema,log10_f, log10_f))
	
        r2=db.store_result()
        strings=r2.fetch_row(maxrows=1)

#    print log10_f,strings

        for string in strings:
            n_m=float(string[1])
            q_m=float(string[2])         

#    print "n(m) %20.9f q(m) %20.9f " % (n_m, q_m)
              
        lr = (q_m * f_r) / (n_m / atlas_sqasec)
        
#   print "Likelihood Ratio : %f " % lr
    
#   update table with likelihood ratio.

        db.query("update %s.matches set lr=%s where cid='%s' \
                  and swire_index_spitzer='%s';" % (field,lr, cid, index_spitzer))

# End of do block

# Close connection to the database
    db.close()

    print "End"


