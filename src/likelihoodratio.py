import math
import array
import _mysql
import numpy
import scipy
import matplotlib.pyplot as plt
import astropysics as astro

from astropysics.constants import c,G

def auks():
    global pie
    global e
    global eradian
    pie=math.pi
    e=math.e
    eradian=180.0/math.pi

def print_header():
	print "Likelihood Ratio"
	
def print_end():
    print "End"

#def Q_0():
# This function takes three source catalogs
# 1) The radio data
# 2) the Swire data
# 3) the randon data
# It yields the four fields. Q0, e_Q0, Sigma(Positional accuracy), e_sigma(error in sigma).

#===================================================================================================
def QCalcReal():
# Compute distance to nearest swire source from radio objects.
# Connect to the local database with the atlas uid

  db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

# Lets run a querry

  db.query("select t1.cid, t2.index_spitzer, \
            pow((t1.RA_Deg-t2.RA_SPITZER)*cos(t1.Dec_Deg),2)+ \
            pow(t1.Dec_Deg-t2.DEC_SPITZER,2)\
            from ecdfs.coords as t1, swire_cdfs.cdfs as t2 \
            where pow((t1.RA_Deg-t2.RA_SPITZER)*cos(t1.Dec_Deg),2)+ \
            pow(t1.Dec_Deg-t2.DEC_SPITZER,2) <= pow(10/3600,2) \
            order by t1.cid;")

  r=db.use_result()

  # fetch results, returning char we need float !

  rows=r.fetch_row(maxrows=100)

  # Close connection to the database

  db.close()

  # print returned rows

  for row in rows:
      print row

  return

#===================================================================================================

execfile('area_none_radio_survey.py')

auks()
print_header()	
print "Pi      :",pie
print "e       :",e
print "eradian :",eradian

#Print physical constants
print "c       :",c
print "G       :",G

#QCalcReal()

area=area_none_radio_survey()
print "Area returned  : %f" % area

print_end()
