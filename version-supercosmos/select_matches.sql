SELECT t1.nvss_id, t2.recno, t2.ra_2000 as 'nvss_ra_2000', t2.decl_2000 as 'nvss_dec_2000', 
       t1.supercosmos_id, t3.ra_2000 as 'supercosmos_ra_2000', t3.dec_2000 as 'supercosmos_dec_2000',
       t1.lr, t1.reliability
FROM gama12.gama12_matches as t1, 
	 nvss_gama12.nvss_gama12 as t2,
     supercosmos_gama12.supercosmos_gama12 as t3
where t1.lr is not null
and   t1.nvss_id=t2.id
and   t1.supercosmos_id=t3.id