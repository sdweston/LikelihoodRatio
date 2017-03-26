set session wait_timeout=86400;
select t1.id, t1.fpeak, t1.fint, t2.id, t2.fpeak, t2.fint, 
	   format(sqrt(pow((t1.RA-t2.RA)*cos(radians(t1.Decl)),2)+pow(t1.Decl-t2.Decl,2))*3600,6)
       from first.first_01 as t1, first.first_01 as t2
       where pow((t1.RA-t2.RA)*cos(radians(t1.Decl)),2)+pow(t1.Decl-t2.Decl,2) <= pow(10/3600,2)
       and t1.id!=t2.id
       limit 0,20000;