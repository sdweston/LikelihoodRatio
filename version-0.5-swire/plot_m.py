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

    db.query("SELECT i,log10_f,total_m,real_m,n_m FROM %s.%s_n_m_lookup;" % (schema,field))
          
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


    plt.plot(log10_f, total_m,'k.',log10_f,real_m,'g+',log10_f,bckgrd,'ro')
    plot_title=field+'  Log10(f) vs #(m)' 
    plt.title(plot_title)
    plt.ylabel('#(m)')
    plt.yscale('log')
    plt.ylabel('N')
    plt.xlabel('log10(f)')
    plt.legend(["Total(m)","Real(m)","n(m) - Background"])
    plot_fname='atlas_'+field+'_magnitude_dependance_point.eps' 
    fname=output_dir + plot_fname
    plt.savefig(fname,format="eps")
    plt.show()
	
# create a stepped histogram

    width=(log10_f[2]-log10_f[1])/2
    print "Width : ",width
#offset the x for horizontal, repeat the y for vertical:
    x=[]
    y1=[]
    y2=[]
    y3=[]
	
    i=0
    for item in log10_f:
        print item
        x.append(item-width)
        y1.append(total_m[i])
        y2.append(real_m[i])
        y3.append(bckgrd[i])
        x.append(item+width)
        y1.append(total_m[i])
        y2.append(real_m[i])
        y3.append(bckgrd[i])
        i=i+1
	
    print x
    print y1	
#    plt.plot(x,y1,linestyle='_',color='k')
    plt.plot(x, y1,'k:',x,y2,'g-',x,y3,'r--')
    plt.yscale('log')
    plt.ylabel('total(m)')
    plt.xlabel('log10(f)')
    plot_fname='atlas_'+field+'_magnitude_dependance_bar.eps' 
    fname=output_dir + plot_fname
    plt.savefig(fname,format="eps")
    plt.show()
    
    print "End Plotting\n"


