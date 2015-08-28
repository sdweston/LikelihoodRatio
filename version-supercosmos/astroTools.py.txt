#! /usr/bin/python
#
# http://supernovae.in2p3.fr/~baumont/phAse/src/HTML/astroTools.py
# Credit: Sylvain Baumont and the SNLS team at LPNHE.
#  convHMS : Convert the RA in H:M:S of an object present
#  into floating point degrees.
#
#  convDMS : Convert the DEC in D:M:S of an object present
#  into floating point degrees.
#
#  dateobs2mmjd : Convert the Observation Date YYYY-MM-DD
#  into Modified Julien Date.
#

import time,calendar
import string

# Convert HH:MM:SS.SSS into Degrees :
def convHMS(ra):
   try :
      sep1 = ra.find(':')
      hh=int(ra[0:sep1])
      sep2 = ra[sep1+1:].find(':')
      mm=int(ra[sep1+1:sep1+sep2+1])
      ss=float(ra[sep1+sep2+2:])
   except:
      raise
   else:
      pass
   
   return(hh*15.+mm/4.+ss/240.)

# Convert +DD:MM:SS.SSS into Degrees :
def convDMS(dec):

   Csign=dec[0]
   if Csign=='-':
      sign=-1.
      off = 1
   elif Csign=='+':
      sign= 1.
      off = 1
   else:
      sign= 1.
      off = 0

   try :
      sep1 = dec.find(':')
      deg=int(dec[off:sep1])
      sep2 = dec[sep1+1:].find(':')
      arcmin=int(dec[sep1+1:sep1+sep2+1])
      arcsec=float(dec[sep1+sep2+2:])
   except:
      raise
   else:
      pass

   return(sign*(deg+(arcmin*5./3.+arcsec*5./180.)/100.))

# Convert RA (deg) to H.M.S:
def deg2HMS( RAin ):

   if(RAin<0):
      sign = -1
      ra   = -RAin
   else:
      sign = 1
      ra   = RAin

   h = int( ra/15. )
   ra -= h*15.
   m = int( ra*4.)
   ra -= m/4.
   s = ra*240.

   if(sign == -1):
      out = '-%02d:%02d:%06.3f'%(h,m,s)
   else: out = '+%02d:%02d:%06.3f'%(h,m,s)
   
   return out
   
# Convert Decl. (deg) to D.M.S:
def deg2DMS( Decin ):

   if(Decin<0):
      sign = -1
      dec  = -Decin
   else:
      sign = 1
      dec  = Decin

   d = int( dec )
   dec -= d
   dec *= 100.
   m = int( dec*3./5. )
   dec -= m*5./3.
   s = dec*180./5.

   if(sign == -1):
      out = '-%02d:%02d:%06.3f'%(d,m,s)
   else: out = '+%02d:%02d:%06.3f'%(d,m,s)

   return out
   
      
# Convert YYYY-MM-DD into MMJD :
def dateobs2mmjd(dateobs):
    tuple_time = time.strptime(dateobs, "%Y-%m-%d" )
    dateobs_as_seconds = time.mktime(tuple_time)
    refepoch = time.strptime("2003-01-01", "%Y-%m-%d" )
    refepoch_as_seconds = time.mktime(refepoch)
    
    return (dateobs_as_seconds-refepoch_as_seconds)/3600./24.+1


# Convert YYYY-MM-DDTHH:MM:SS.SSS into MMJD :
def timeobs2mmjd(timeobs):
   day = timeobs[0:timeobs.find('T')]
   time= timeobs[timeobs.find('T')+1:]
   try :
      hour= int(time[0:2])
      min = int(time[3:5])
      sec = float(time[6:])
   except :
      raise 'Format', timeobs
   else :
      mmjd = dateobs2mmjd(day)+(((sec/60.)+min)/60.+hour)/24.
      
   return mmjd
   
# Convert YYYY-MM-DDTHH:MM:SS.SSS into UTC :
def timeobs2secUT(timeobs):

   try :
      tuple = time.strptime(timeobs[0:19], '%Y-%m-%dT%H:%M:%S')
   except :
      raise 'Format', timeobs
   else :
      secs = time.mktime(tuple)

   return secs

# MMJD -> Date YYYY-MM-DD & HH:MM
def mmjd2date( mmjd ):
  
    refepoch = time.strptime("2003-01-01", "%Y-%m-%d" )
    refepoch_as_seconds = time.mktime(refepoch)
    epoch = refepoch_as_seconds + mmjd*24.*60.*60.
    tuple_date = time.gmtime( epoch )
    date = time.strftime('%Y-%m-%dT%H:%M', tuple_date)

    day = date[:date.find('T')]
    hour= date[date.find('T')+1:]

    return [day, hour]


# Cut YYYY-MM-DDTHH:MM:SS.SSS into [Y,M,D,H,M,S]:
def splitESOdate( timeobs ):
   
   date = timeobs[0:timeobs.find('T')]
   time= timeobs[timeobs.find('T')+1:]
   try :
      year   = int( date[:4]  )
      mounth = int( date[5:7] )
      day    = int( date[8:10] )
      hour= int(time[0:2])
      min = int(time[3:5])
      sec = float(time[6:])
   except :
      print '! Bad Obs Date Format : %s .'%timeobs
      raise
   else :
      pass

   return [year, mounth, day, hour, min, sec ]

# Return the ObsDe=ate at ESO convention :  date of beginning of night.
# Use GMT to handle change in mounth :
def getESOnight( timeobs ):

   try :
      [y,m,d,h,min,sec] = splitESOdate( timeobs)
   except:
      print '! Not ESO date format : %s '%timeobs
      raise
   else :
      if h < 12 : corr = -1.
      else : corr = 0.

   day = '%s-%s-%s'%(y,m,d)
   tuple   = time.strptime(day,'%Y-%m-%d')
   sec     = calendar.timegm(tuple)+corr*24.*60.*60.
   ESOtime = time.gmtime(sec)
   ESOday  = time.strftime('%Y-%m-%d', ESOtime)
   
   return ESOday


# Return the hour modulus 12. from HH:MM:SS :
def ESOhour ( hour ):
   try :
      h = int(hour[:2])
      m = int(hour[3:5])
      s = int(hour[6:8])
   except:
      print '! Format error : %s .'%hour
      raise

   ESOhour = h+m/60.+s/3600.

   if ESOhour > 12. : ESOhour -= 24.

   return ESOhour

   
# MIDAS MJD @ MMJD=0 :
mmjd2mjd = 52640.0
mmjd2gmt = 12052.0