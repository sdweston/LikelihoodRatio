import csv
import os

radio_image_fits='/storage-a/sweston/fits/ELAIS_I_allch_map-background.fits'

nonradio_image_fits='/storage-a/sweston/swire_Es1_I1/final/elais_s1_uncorrected.fits'

#with open('swire-es1-postage-stamp-info.csv', 'rb') as csvfile:
with open('test.csv', 'rb') as csvfile:
     csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
     for row in csvreader:
#         print ' '.join(row)
         cid=row[0]
         idx_spitzer=row[1]
         ra_spitzer=row[2]
         dec_spitzer=row[3]
         ra_radio=row[4]
         dec_radio=row[5]
         lr=row[6]
         rel=row[7]
         print cid," ",idx_spitzer," ",ra_radio," ",dec_radio," ",ra_spitzer," ",dec_spitzer," ",lr," ",rel
         f_rel=float(rel)
         f_lr=float(lr)
         f_ra=float(ra_radio)
         f_dec=float(dec_radio)
         #print cid," ",idx_radio," ",ra_radio," ",dec_spitzer," ",lr," ",rel

#        Create region file with text for reliability value into image.
         ra2=f_ra+0.007
         dec2=f_dec+0.01
         region_file_name=cid+'_'+ra_radio+'_'+dec_radio+'.reg'
         f=open(region_file_name,'w')
         f.write('global color=blue font="helvetica 10 normal "\n')
         f.write('fk5;circle('+str(ra2)+' , '+str(dec2)+',0.1") # text={Reliability      : '+rel+'}\n')
         f.write('fk5;circle('+str(ra2)+' , '+str(dec2-0.002)+',0.1") # text={Likelihood Ratio : '+lr+'}\n')
         f.write('global color=red\n')
         f.write('fk5;circle( '+ra_spitzer+' , '+dec_spitzer+' ,1") # point=cross\n')
         f.write('fk5;circle( '+ra_radio+' , '+dec_radio+' ,10") # point=cross\n')
         f.close()

         contour_file_name=cid+'_'+ra_radio+'_'+dec_radio+'.con'
         cmd1='ds9.7.2 -zscale -invert '+radio_image_fits+' -crop '+ra_spitzer+' '+dec_spitzer + \
             ' 100 100 wcs fk5 arcsec -contour open -contour loadlevels ds9.lev -contour yes ' + \
             '-contour save '+contour_file_name+' -contour close -zoom to fit -exit'
         print cmd1

         postage_stamp_filename=cid+'_'+ra_radio+'_'+dec_radio+'.jpeg'
         cmd2='ds9.7.2 -zscale -invert '+ nonradio_image_fits+' -crop '+ra_radio+' '+dec_radio + \
              ' 100 100 wcs fk5 arcsec -contour open -contour load '+contour_file_name+ \
              ' -regions '+region_file_name+ ' -colorbar no ' +\
              ' -contour close -zoom to fit -saveimage '+postage_stamp_filename+' 100 -exit'
         print cmd2

         os.system(cmd1)
         os.system(cmd2)

