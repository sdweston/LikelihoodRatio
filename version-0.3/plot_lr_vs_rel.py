#===========================================================================
#
# plot_m.py
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

def plot_lr_rel():

    print "\nStarting Plot Likelihood Ratio vs Reliability"

#   Connect to the local database with the atlas uid

    db=_mysql.connect(host=db_host,user=db_user,passwd=db_passwd)

# select from matches the sum of L_i grouped by radio source

    db.query("select lr,reliability from "+schema+"."+field+"_matches where reliability > 0.0 and reliability < 1.0;" )
          
# store_result() returns the entire result set to the client immediately.
# The other is to use use_result(), which keeps the result set in the server 
#and sends it row-by-row when you fetch.

#r=db.store_result()
# ...or...
    r=db.use_result()

# fetch results, returning char we need float !

    rows=r.fetch_row(maxrows=5000)

# rows is a tuple, convert it to a list

    LR=[]
    REL=[]
 

    for row in rows:
        
        LR.append(float(row[0]))
        REL.append(float(row[1]))
        
	
#    End of do block

# Close connection to the database
    db.close()

# Now plot the data

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
	
    
    print "End Plotting\n"


