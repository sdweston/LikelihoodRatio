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

def plot_m():

    print "\nStarting Plot total(m), real(m), background"

#   Connect to the local database with the atlas uid

    db=_mysql.connect(host=db_host,user=db_user,passwd=db_passwd)

# select from matches the sum of L_i grouped by radio source

    db.query("SELECT i,log10_f,total_m,real_m,bckgrd_m FROM swire_es1.n_m_lookup;")
          
# store_result() returns the entire result set to the client immediately.
# The other is to use use_result(), which keeps the result set in the server 
#and sends it row-by-row when you fetch.

#r=db.store_result()
# ...or...
    r=db.use_result()

# fetch results, returning char we need float !

    rows=r.fetch_row(maxrows=5000)

# rows is a tuple, convert it to a list

    log10_f=[]
    total_m=[]
    real_m=[]
    bckgrd=[]

    for row in rows:
        
        log10_f.append(float(row[1]))
        total_m.append(float(row[2]))
        real_m.append(float(row[3]))
        bckgrd.append(float(row[4]))
	
	
#    End of do block

# Close connection to the database
    db.close()

# Now plot the data

    plt.yscale('log')
    plt.plot(log10_f, total_m,'k.',log10_f,real_m,'g+',log10_f,bckgrd,'ro')
    plt.title(' Log10(f) vs Total(m)')
    plt.ylabel('Total(m)')
    plt.xlabel('log10(f)')
    plt.legend(["Total(m)","Real(m)","Background"])
    plot_fname='magnitude_dependance.ps'
    fname=output_dir + plot_fname
    plt.savefig(fname)
    plt.show()
    
    print "End Plotting\n"


