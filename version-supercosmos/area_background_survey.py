#===========================================================================
#
# area_background_survey.py
#
# Python script to query gama12 mysql database to determine the
# area of the survey for a sub-set of the survey.
#
#===========================================================================
#
# S. Weston
# AUT University
# March 2015
#===========================================================================


# Following up from our chat I will send you the two data sets to try the 
# XID code on. These are the NVSS catalogue and Supercosmos selected from 
# the "GAMA 12" region:
# J2000 RA:   174 to 186 deg (11:36:00 to 12:24:00)
#         Dec:  -2.0 deg to +2.0 deg

		 
def area_background_survey():

    global ra1
    global ra2
    global dec1
    global dec2   
	
    global nvss_ra1
    global nvss_ra2
    global nvss_dec1
    global nvss_dec2


#    area_sqdeg=term1* term3* term2
# 1 sq deg = 12 960 000 sq arc seconds
# 1 sq minute = 3600 sq arc seconds


#   Supercosmos_gama12
    ra1=174.138458333
    ra2=186.185083333
    dec1=-2.08702777778
    dec2=1.94011111111

#     Define an area of nvss_ to search NN and determine n(m) over.
	  
    nvss_ra1=174.00046
    nvss_ra2=185.99975
    nvss_dec1=-1.99958
    nvss_dec2=1.99975


 	  
#    print "GAMA12 Area square degrees : %f" % area_sqdeg

    rad_ra1=math.radians(ra1)
    rad_ra2=math.radians(ra2)
    dec1_dec2=(dec1+dec2)/2
    print "(dec1 + dec2)/2                 = %f" % dec1_dec2

    term1=ra1-ra2
    print "(ra1-ra2)                       = %f" % term1

    term2=dec1-dec2
    print "(dec1-dec2)                     = %f" % term2

    term3=math.cos(math.radians(dec1_dec2))
    print "math.cos((rad_dec1+rad_dec2)/2) = %f" % term3

    area_sqdeg=term1* term3* term2

    print "Area Supercosmos square degrees : %f" % area_sqdeg

    area_supercosmos_arcsec=area_sqdeg*(3600**2)
    print "Area SuperCosmos square arcsec  : %f" % area_supercosmos_arcsec

# Determine swire search area for n(m)

    print "Swire areas"
	
    nvss_rad_ra1=math.radians(nvss_ra1)
    nvss_rad_ra2=math.radians(nvss_ra2)
    nvss_dec1_dec2=(nvss_dec1+nvss_dec2)/2

    print "(dec1 + dec2)/2                 = %f" % nvss_dec1_dec2
 	
    nvss_term1=nvss_ra1-nvss_ra2

    nvss_term2=nvss_dec1-nvss_dec2

    nvss_term3=math.cos(math.radians(nvss_dec1_dec2))
	
    print "(ra1-ra2)                       = %f" % nvss_term1
    print "(dec1-dec2)                     = %f" % nvss_term2
    print "math.cos((rad_dec1+rad_dec2)/2) = %f" % nvss_term3

    area_nvss_sqdeg=nvss_term1* nvss_term3* nvss_term2

    print "Area NVSS square degrees : %f" % area_nvss_sqdeg
	
    area_nvss_arcsec=area_nvss_sqdeg*(3600**2)
    print "GAMA12 n(m) Area square arcsec  : %f" % area_nvss_arcsec
	
    return area_nvss_arcsec, area_supercosmos_arcsec


