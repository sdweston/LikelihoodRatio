Hi Stuart,

Here is a tar ball of the two files:

https://www.dropbox.com/sh/rbenmlkiztc7isq/AAD3VUZrXflxfm4mAI5s4VOia?dl=0

in csv format. 

For supercomos we will use the B_J magnitude. The RA+dec should be straight forward. The NVSS file should be obvious too. I list all the columns below.

cheers,

Nick

Supercosmos:

true 	RA 	$1 	Double 	DEGREES 	Celestial Right Ascension 	D20.12 	1D
true 	DEC 	$2 	Double 	DEGREES 	Celestial Declination 	D20.12 	1D
true 	EPOCH 	$3 	Float 	year 	Epoch 	F9.3 	1E
true 	MU_ACOSD 	$4 	Float 	mas/yr 	Proper motion in RA 	E12.4 	1E
true 	MU_D 	$5 	Float 	mas/yr 	Proper motion in DEC 	E12.4 	1E
true 	SIGMU_A 	$6 	Float 	mas/yr 	Estimated error in RA pm 	E12.4 	1E
true 	SIGMU_D 	$7 	Float 	mas/yr 	Estimated error in DEC pm 	E12.4 	1E
true 	B_J 	$8 	Float 	magnitude 	Photographic B(J) magnitude 	F7.3 	1E
true 	R_1 	$9 	Float 	magnitude 	1st epoch photographic R magnitude 	F7.3 	1E
true 	R_2 	$10 	Float 	magnitude 	2nd epoch photographic R magnitude 	F7.3 	1E
true 	I 	$11 	Float 	magnitude 	Photographic I magnitude 	F7.3 	1E
true 	AREA 	$12 	Integer 	pixels 	Image area 	I9 	1J
true 	A_I 	$13 	Integer 	0.01 um 	Weighted semi-major axis 	I7 	1J
true 	B_I 	$14 	Integer 	0.01 um 	Weighted semi-minor axis 	I7 	1J
true 	PA 	$15 	Integer 	degrees 	Celestial position angle 	I3 	1J
true 	CLASS 	$16 	Integer 		Image classification flag 	I2 	1J
true 	N_0_1 	$17 	Float 	sigma 	N(0,1) profile classification statistic 	F8.3 	1E
true 	BLEND 	$18 	Integer 		Deblending flag (0 if not deblended) 	I6 	1J
true 	QUALITY 	$19 	Integer 		Image quality flag 	I10 	1J
true 	FIELD 	$20 	Integer 		Survey field number 	I5 	1J

NVSS: 

true 	_RAJ2000 	$1 	Double 	deg 		pos.eq.ra 	double 	
true 	_DEJ2000 	$2 	Double 	deg 		pos.eq.dec 	double 	
true 	recno 	$3 	Integer 		Record number within the original table (starting from 1) 	meta.record 	int 	
true 	NVSS 	$4 	String 		Source name (1) 	meta.id;meta.main 	char 	
true 	RAJ2000 	$5 	String 	"h:m:s" 	Right Ascension J2000 (2) 	pos.eq.ra;meta.main 	char 	HMS->degrees
true 	DEJ2000 	$6 	String 	"d:m:s" 	Declination J2000 (2) 	pos.eq.dec;meta.main 	char 	DMS->degrees
true 	e_RAJ2000 	$7 	Float 	s 	Mean error on RA 	stat.error;pos.eq.ra 	float 	
true 	e_DEJ2000 	$8 	Float 	arcsec 	Mean error on Dec 	stat.error;pos.eq.dec 	float 	
true 	S1.4 	$9 	Double 	mJy 	Integrated 1.4GHz flux density of radio source 	phot.flux.density;em.radio.750-1500MHz 	double 	
true 	e_S1.4 	$10 	Float 	mJy 	Mean error on S1.4 	stat.error 	float 	
true 	l_MajAxis 	$11 	Character 		Limit flag on MajAxis 	meta.code.error;phys.angSize 	char 	
true 	MajAxis 	$12 	Float 	arcsec 	Fitted (deconvolved) major axis of radio source 	phys.angSize;em.radio;meta.modelled 	float 	
true 	l_MinAxis 	$13 	Character 		Limit flag on MinAxis 	meta.code.error;phys.angSize 	char 	
true 	MinAxis 	$14 	Float 	arcsec 	Fitted (deconvolved) minor axis of radio source 	phys.angSize;em.radio;meta.modelled 	float 	
true 	f_resFlux 	$15 	String 		[PS* ] Residual Code (3) 	meta.code 	char 	
