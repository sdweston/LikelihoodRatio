#===========================================================================
#
# area_none_radio_survey.py
#
# Python script to query SWIRE_ES1 mysql database to determine the
# area of the survey for a sub-set of the survey.
#
#===========================================================================
#
# S. Weston
# AUT University
# March 2013
#===========================================================================

def area_none_radio_survey():

    global ra1
    global ra2
    global dec1
    global dec2

# http://home.strw.leidenuniv.nl/~jarle/Surveys/DeepFields/SWIRE-ELAIS-S1-All.html
# SWIRE ELAIS_S1 at 3.5mu 4.2 deg sq

#http://home.strw.leidenuniv.nl/~jarle/Surveys/DeepFields/E-CDF-S-All.html
# Spitzer CDFS at 3.5mu 143.2 min sq
 
#    area_sqdeg=term1* term3* term2
# 1 sq deg = 12 960 000 sq arc seconds
# 1 sq minute = 3600 sq arc seconds

    if swire_schema == 'swire_cdfs': 
#     ATLAS CDFS 3.566 sq deg
      area_arcsec=3.566 * 12960000
      ra1=51.474385
      ra2=54.023942
      dec1=-28.841196
      dec2=-27.213252


    else:
#     ATLAS ES1 2.697 sq deg, 
      area_arcsec=2.697 * 12960000
      ra1=7.357132
      ra2=9.77962
      dec1=-44.601035
      dec2=-42.899883

	  
#    print "Area square degrees : %f" % area_sqdeg

    rad_ra1=math.radians(ra1)
    rad_ra2=math.radians(ra2)
    dec1_dec2=(dec1+dec2)/2
    print "(dec1 + dec2)/2 : %f" % dec1_dec2

    term1=ra1-ra2
    print "(ra1-ra2)                       = %f" % term1

    term2=dec1-dec2
    print "(dec1-dec2)                     = %f" % term2

    term3=math.cos(math.radians(dec1_dec2))
    print "math.cos((rad_dec1+rad_dec2)/2) = %f" % term3

    area_sqdeg=term1* term3* term2

    print "Area square degrees : %f" % area_sqdeg

    area_arcsec=area_sqdeg*(3600**2)
    print "Area square arcsec  : %f" % area_arcsec

    return area_arcsec


