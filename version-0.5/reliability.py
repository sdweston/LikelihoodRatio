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

    db.query("select cid,sum(lr) \
              from "+schema+"."+field+"_matches \
		      where lr is not null \
		      group by cid;" )
          
# store_result() returns the entire result set to the client immediately.
# The other is to use use_result(), which keeps the result set in the server 
#and sends it row-by-row when you fetch.

#r=db.store_result()
# ...or...
    r=db.use_result()

# fetch results, returning char we need float !

    rows=r.fetch_row(maxrows=100000)

# rows is a tuple, convert it to a list

    print "    Calculate Reliability values and Update database "
    LR=[]
    REL=[]

    for row in rows:
#    print row
        cid=row[0]
        sum_lr=float(row[1])
		
#        sys.stdout.write('.')
    
# now select each row from matches for each radio source where the flux is not null

        db.query("select swire_index_spitzer,lr \
                  from "+schema+"."+field+"_matches \
	              where lr is not null \
	              and cid like '%s';" % (cid))

        r2=db.store_result()
        strings=r2.fetch_row(maxrows=100000)

        for string in strings:
#        print string
            index_spitzer=(string[0])
            lr=float(string[1])   
		
#       and calculate the reliability

            rel= lr / (sum_lr + (1-Q0))
            LR.append(lr)
            REL.append(rel)
            sys.stdout.write('.')
#        print 'Reliability : %f ' % rel
	
#       Now update the matches table with the reliability

            db.query("update "+schema+"."+field+"_matches set reliability=%s where cid='%s' \
                      and swire_index_spitzer='%s';" % (rel, cid, index_spitzer))
	
# End of do block

# Close connection to the database
    db.close()

    print "Plot LR vs Reliability"

    plt.xscale('log')
    plt.plot(LR, REL,'k.')
	
    plot_title='ATLAS ' +field+ ' Reliability vs Likelihood Ratio'
    plt.title(plot_title)
    plt.ylabel('Reliability')
    plt.xlabel('Likelihood Ratio')
    plot_fname='atlas_' +field+ '_rel_vs_lr.ps'
    fname=output_dir + plot_fname
    plt.savefig(fname,orientation='landscape')
    plt.show()

    print "End"


