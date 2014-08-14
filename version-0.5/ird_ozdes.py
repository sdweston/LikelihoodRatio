create temporary table if not exists atlas_dr3.cdfs_ird as ( 
          select cid,swire_index_spitzer,reliability 
          from atlas_dr3.cdfs_matches  
          where reliability > 0.3 and reliability < 0.7) ;

select cid,count(cid) as cnt from atlas_dr3.cdfs_ird 
       group by cid having cnt >1;
	   
# We now have the cid's for the infared multiple candidates
# so go back to matches with these cid's and get the fusion_spitzer_id's, and ra,dec

# Then do nearest neighbour with OzDES on ra,dec with a search radius of say 1"
# So modify this logic for the tables:

    print "find all matches within search radius\n"
	
    sql1=("insert into "+schema+"."+field+"_matches(cid,swire_index_spitzer,dx,dy,r_arcsec,flux) "
              "select t1.id, "
              "t2.ID_12, "
              "(t1.ra-"+str(posn_offset_ra)+"-t2.ra_12)*cos(t1.decl-"+str(posn_offset_dec)+"), "
              "t1.decl-"+str(posn_offset_dec)+"-t2.dec_12, "
              "sqrt(pow((t1.ra-"+str(posn_offset_ra)+"-t2.ra_12)*cos(t1.decl-"+str(posn_offset_dec)+"),2)+pow(t1.decl-"+str(posn_offset_dec)+"-t2.dec_12,2))*3600, "
			  "t2.flux_ap2_36 "
              "from "+schema+"."+field+"_coords as t1, fusion."+field+" as t2 "
              "where pow((t1.ra-"+str(posn_offset_ra)+"-t2.ra_12)*cos(t1.decl-"+str(posn_offset_dec)+"),2)+" 
              "pow(t1.decl-"+str(posn_offset_dec)+"-t2.dec_12,2) <= pow("+str(sr)+"/3600,2) "
              " and   t2.ra_12 > "+str(ra1)+" and t2.ra_12 < "+str(ra2)+" "
              " and   t2.dec_12 > "+str(dec1)+" and t2.dec_12 < "+str(dec2)+" limit 0,3000000; ")
			  
# Print out the OzDES id, ra, dec and Z