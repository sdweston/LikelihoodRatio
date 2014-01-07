select cid,ra_deg,dec_deg 
from ecdfs.coords
where cid  in (select cid1 
from ecdfs.radio_pairs
where flux1/flux2 > 1.0
and flux1/flux2 < 2.1
and ang_sep_arcsec/sqrt(flux1+flux2) > 2.0
and ang_sep_arcsec/sqrt(flux1+flux2) < 10.0);