import csv
import os

#radio_image_fits='d:\\elaiss1\\atlas_elaiss1_map.fits'
radio_image_fits='d:\\elaiss1\\atlas_elaiss1_map.fits'

# Can't load this 2GB fits file on windows ?
#nonradio_image_fits='d:\\elaiss1\\elais_s1_uncorrected_area.fits'
nonradio_image_fits='d:\\elaiss1\\swire_ES1_M1_v4_mosaic.fits'


#with open('swire-es1-postage-stamp-info.csv', 'rb') as csvfile:
with open('D:\\elaiss1\\elaiss1_radio_pairs.csv', 'r') as csvfile:
     csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
     for row in csvreader:
#         print ' '.join(row)
         cid1=row[0]
         ra1=row[1]
         dec1=row[2]
         cid2=row[3]
         ra2=row[4]
         dec2=row[5]

                 
         print cid1," ",ra1," ",dec1," ",cid2," ",ra2," ",dec2
		 
#        Create region file with text for cid and cross for atlas source posn.
#        f_ra=float(ra_atlas)+0.007
#         f_dec=float(dec_atlas)+0.01
         region_file_name='D:\\ecdfs\\'+cid1+'.reg'
         f=open(region_file_name,'w')
         f.write('global color=red font="helvetica 10 normal "\n')
#         f.write('fk5;circle('+str(f_ra)+' , '+str(f_dec)+',0.1") # text={'+cid+'}\n')
         f.write('fk5;circle( '+ra1+' , '+dec1+' ,1") # point=cross text={'+cid1+'}\n')
         f.write('fk5;circle( '+ra2+' , '+dec2+' ,1") # point=cross text={'+cid2+'}\n')
         f.close()

         contour_file_name=cid1+'.con'
         postage_stamp_filename1='atlas_'+cid1+'_'+cid2+'.jpeg'
                  
         cmd1='ds9 -zscale -invert '+radio_image_fits+' -crop '+ra1+' '+dec1 + \
             ' 150 150 wcs fk5 arcsec -contour open -contour loadlevels contour_ds9.lev -contour yes ' + \
             ' -regions '+region_file_name+ ' -colorbar no ' +\
              '-contour save '+contour_file_name+' -contour close -zoom to fit ' +\
             '-saveimage '+postage_stamp_filename1+' 100 -exit' 
#             '-contour save '+contour_file_name+' -contour close -zoom to fit -exit'
         print cmd1

         postage_stamp_filename2='swire_atlas_'+cid1+'_'+cid2+'.jpeg'
         cmd2='ds9 -zscale -invert '+ nonradio_image_fits+' -crop '+ra1+' '+dec1 + \
              ' 150 150 wcs fk5 arcsec -contour open -contour load '+contour_file_name+ \
              ' -regions '+region_file_name+ ' -colorbar no ' +\
              ' -contour close -zoom to fit -saveimage '+postage_stamp_filename2+' 100 -exit'
#         print cmd2

         os.system(cmd1)
         os.system(cmd2)

