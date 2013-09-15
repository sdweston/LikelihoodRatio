import _mysql
import sys

db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

db.query("insert into elais_s1.ES1_RandomCat(id,ra,declination) values ('r02','5.6','40.1');")


db.commit()

db.close()
