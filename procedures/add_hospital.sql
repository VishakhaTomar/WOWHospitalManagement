CREATE DEFINER=`root`@`localhost` PROCEDURE `add_hospital`(IN in_hname varchar(30), IN in_plotNo varchar(30), IN in_street varchar(100),IN in_city varchar(30),IN in_state varchar(30),IN in_zipcode varchar(30),IN in_speciality varchar(30),IN ecc_hotline BIGINT(10),IN in_phone BIGINT(10), IN in_adminphone BIGINT(10),in curd char(1), in in_hid double, out result int(1) )
BEGIN
case curd
when 'A' then INSERT INTO hospital(hname,plotno,street,city,state,zipcode,speciality,ecchotline,phoneno,adminphone,tbl_last_date) VALUES (in_hname,in_plotNo,in_street,in_city,in_state,in_zipcode,in_speciality,ecc_hotline,in_phone,in_adminphone,sysdate());
when 'U' then update hospital SET hname= in_hname,plotno=in_plotNo ,street=in_street,city=in_city,state=in_state,zipcode=in_zipcode,speciality=in_speciality,ecchotline=ecc_hotline,phoneno=in_phone,adminphone=in_adminphone, tbl_last_date=sysdate() where hid=in_hid;
when 'D' then delete from hospital where hid=in_hid;
else set result= -1;
END case; 
end