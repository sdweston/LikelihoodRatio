import csv

ra=[]
dec=[]
cid=[]

with open('D:\\ecdfs\\radio_pairs_coords_cid2.csv', 'r') as csvfile:
     csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
     for row in csvreader:
#         print ' '.join(row)
        cid.append(row[0])
        ra.append(row[1])
        dec.append(row[2])

i=len(ra)
print "Array Len ",i,"\n"

for i in cid:
    print i,"\n"
