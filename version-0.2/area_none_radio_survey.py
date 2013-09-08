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

# http://home.strw.leidenuniv.nl/~jarle/Surveys/DeepFields/SWIRE-ELAIS-S1-All.html
# SWIRE ELAIS_S1 at 3.5mu 4.2 deg sq

#http://home.strw.leidenuniv.nl/~jarle/Surveys/DeepFields/E-CDF-S-All.html
# Spitzer CDFS at 3.5mu 143.2 min sq
 
    ra2=8.0
    ra1=9.5
    dec2=-44.5
    dec1=-43.0



#    area_sqdeg=term1* term3* term2
# 1 sq deg = 12 960 000 sq arc seconds
# 1 sq minute = 3600 sq arc seconds

    if field == 'ecdfs': 
#     ATLAS ES1 2.697 sq deg, 
      area_arcsec=3.566 * 12960000
	  ra1=7.357132
      ra2=9.77962
      dec1=-44.601035
      dec2=-42.899883

    else:
#     ATLAS CDFS 3.566 sq deg
      area_arcsec=2.697 * 12960000
      ra1=51.474385
      ra2=54.023942
      dec1=-28.841196
      dec2=-27.213252

	  
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

#    area_arcsec=area_sqdeg*60*(3600**2)

    print "Area square arcsec  : %f" % area_arcsec

    return area_arcsec


