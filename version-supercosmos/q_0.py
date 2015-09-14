#===========================================================================
#
# q_0.py
#
# Python script to query mysql database to determine the
# Q0
#
#===========================================================================
#
# S. Weston
# AUT University
# May 2014
#===========================================================================

def q_0():

    global Q
    print "\nStarting q0 calculation"

    execfile('constants.py')
    execfile('get_sigma_foreground.py')
	
    print "simga_foreground :",sigma_foreground
    print "\n"
    b=1/(2*(sigma_foreground**2))
    print "b           :",b

# Connect to the local database with the atlas uid

    db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

    sql1=("SELECT radius,nr_random,nr_real, "
      " (1-(nr_random/(select count(*) from atlas_dr3."+field+"_coords))), "
      " (1-(nr_real/(select count(*) from atlas_dr3."+field+"_coords))), "
      " (1-(nr_real/(select count(*) from atlas_dr3."+field+"_coords)))/(1-(nr_random/(select count(*) from atlas_dr3."+field+"_coords))) "
      " FROM atlas_dr3."+field+"_q0 ")

    print sql1,"\n"
    db.query(sql1)

    r=db.use_result()

# fetch results, returning char we need float !

    rows=r.fetch_row(maxrows=10)

# Close connection to the database

    db.close()

    x=numpy.empty([10],dtype=float)
    y=numpy.empty([10],dtype=float)

    i=0
    for row in rows:
        print row
        radius=float(row[0])
        real_random=float(row[5])
        print radius,real_random
        x[i]=radius
        y[i]=real_random
        i=i+1


    def func(x,a):
        return 1-a+a*numpy.exp(-b*x**2)

    popt,pcov=curve_fit(func,x,y)

    print "a = %s " % (popt[0])
	
    perr = numpy.sqrt(numpy.diag(pcov))
    print "perr +- %s " % perr

    xx=numpy.linspace(1.0,10.0,num=100)
    yy=func(xx,*popt)

#plot_title=field+" Q0 = %s " % (popt[0])
#    plot_title=field+" y = %s * x ** (- r^2/2 Simga^2) " % (popt[0])
    plot_title=field
#    plt.title(plot_title)
    plt.xlabel('Radius (arcsec)')
    plt.ylabel('Real/Random Normalised')
    plt.plot(x,y,'ro',label="Original Data")
    plt.plot(xx,yy,label="Fitted Curve")
    plt.axis([0,11,0,1])
#    plt.legend(loc='upper right')
#    No grid for publication
#    plt.grid()
#output_dir='I:/PhD 2012/Marsfield April 2014/'
    output_dir='D:/temp/'
    filename=field+'_q0.eps'
    fullname=output_dir+filename
    plt.savefig(fullname,format="eps")
    plt.show()
 
    print "Q0                      : %f" % popt[0]
    Q=popt[0]

# Connect to the local database with the atlas uid

    db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")
	
# Put Q0 into the working table, so don't have to re-run this each time

    db.query("update gama12.gama12_working set q0=%s \
	          where field like '%s';" % (Q,schema))
    db.close()

    print "End or q_0\n"





