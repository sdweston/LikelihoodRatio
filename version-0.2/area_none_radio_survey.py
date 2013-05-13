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

    ra2=8.0
    ra1=9.5
    dec2=-44.5
    dec1=-43.0

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


