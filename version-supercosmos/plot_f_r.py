#===========================================================================
#
# f_r.py
#
# Python script to query SWIRE_ES1 mysql database to plot the
# f(r) vs r for the likelihood ratio.
#
#===========================================================================
#
# S. Weston
# AUT University
# March 2013
#===========================================================================

def plot_f_r():

    print "Plotting f(r) calculations vs radius"

# Load in the definitions and constants
    execfile('constants.py')

# Connect to the local database with the atlas uid

    db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

# Lets run a querry
# table4 for atlas.elais and atlas.cdfs are not consistent. Rename column dbmaj,dbmin to be majaxis,minaxis for both tables !

    sql1="select f_r,r_arcsec from "+schema+"."+schema+"_matches where f_r is not null"
    db.query(sql1)

		  
# store_result() returns the entire result set to the client immediately.
# The other is to use use_result(), which keeps the result set in the server 
#and sends it row-by-row when you fetch.

#r=db.store_result()
# ...or...
    r=db.use_result()

# fetch results, returning char we need float !

    rows=r.fetch_row(maxrows=500000)

# rows is a tuple, convert it to a list

#lst_rows=list(rows)

#print rows

    r_arcsec=[]
    f_r=[]
    irows=0

    for row in rows:

        f_r.append(float(row[0]))
        r_arcsec.append(float(row[1]))
        irows=irows+1

    print "Rows : ",irows
        
    plt.plot(r_arcsec, f_r,'k.')
#plt.plot(x,y)
    plot_title='NVSS GAMA12 f(r) vs r'
    plt.title(plot_title)
    plt.ylabel('f(r)')
    plt.xlabel('r (arcsec)')

    plt.xlim(0.0,40.0)
#plt.yscale('log')
#plt.ylim(0.0,0.5)

#output_dir="D:/temp/"
#plot_fname='nvss_gama12_fr_vs_r.eps'
#fname=output_dir + plot_fname
#plt.savefig(fname,format="eps")
    plt.show()

    print "\nEnd of Plot f(r)"


