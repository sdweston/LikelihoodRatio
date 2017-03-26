To create radio contour's

ds9.7.2 -zscale -invert ELAIS_I...fits -crop 9.48984 -43.282766 100 100 wcs fk5 arcsec -contour open
        -contour loadlevels ds9.lev -contour yes -contour save tst1.con -contour close -zoom to fit

To overlay radio contours on non-radio image:


ds9.7.2 -zscale -invert mosaic...fits -crop 9.48984 -43.282766 100 100 wcs fk5 arcsec -contour open
        -contour load tst1.con -contour close -zoom to fit -saveimage tst1.jpeg 100 -exit
