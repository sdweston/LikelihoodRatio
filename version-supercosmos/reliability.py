#===========================================================================
#
# reliability.py
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

def rel():

    execfile('get_q0.py')

    print "\nStarting Reliability calculations and db updates"

# Connect to the local database with the atlas uid

    db=_mysql.connect(host=db_host,user=db_user,passwd=db_passwd)

# select from matches the sum of L_i grouped by radio source

    db.query("select nvss_id,sum(lr) \
              from "+schema+"."+schema+"_matches \
		      where lr is not null \
		      group by nvss_id;" )
          
# store_result() returns the entire result set to the client immediately.
# The other is to use use_result(), which keeps the result set in the server 
#and sends it row-by-row when you fetch.

#r=db.store_result()
# ...or...
    r=db.use_result()

# fetch results, returning char we need float !

    rows=r.fetch_row(maxrows=500000)

# rows is a tuple, convert it to a list

    print "    Calculate Reliability values and Update database "
    LR=[]
    REL=[]

    for row in rows:
#    print row
        foreground_id=row[0]
        sum_lr=float(row[1])
		
#        sys.stdout.write('.')
    
# now select each row from matches for each radio source where the flux is not null

        db.query("select supercosmos_id,lr \
                  from "+schema+"."+schema+"_matches \
	              where lr is not null \
	              and nvss_id like '%s';" % (foreground_id))

        r2=db.store_result()
        strings=r2.fetch_row(maxrows=50000)

        for string in strings:
#        print string
            background_id=(string[0])
            lr=float(string[1])   
		
#       and calculate the reliability

            rel= lr / (sum_lr + (1-Q0))
            LR.append(lr)
            REL.append(rel)
            sys.stdout.write('.')
#        print 'Reliability : %f ' % rel
	
#       Now update the matches table with the reliability

            db.query("update "+schema+"."+schema+"_matches set reliability=%s where nvss_id='%s' \
                      and supercosmos_id='%s';" % (rel, foreground_id, background_id))
	
# End of do block

# Close connection to the database
    db.close()

    print "Plot LR vs Reliability"

    plt.xscale('log')
    plt.plot(LR, REL,'k.')
	
    plot_title=' ' +schema+ ' Reliability vs Likelihood Ratio'
    plt.title(plot_title)
    plt.ylabel('Reliability')
    plt.xlabel('Likelihood Ratio')
#    plot_fname=field+ '_rel_vs_lr.ps'
#    fname=output_dir + plot_fname
#    plt.savefig(fname,orientation='landscape')
    plt.show()

    print "End"


