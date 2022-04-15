CREATE DEFINER=`root`@`localhost` PROCEDURE `add_doctor`(IN in_firstname varchar(30), IN in_lastname varchar(100),IN in_houseno varchar(100),IN in_docstreet varchar(100),IN in_city varchar(30),IN in_state varchar(30),IN in_zipcode varchar(30),IN in_offphone BIGINT(10),IN in_perphone BIGINT(10), IN in_eccPhone BIGINT(10),IN in_eccname varchar(30),IN in_speciality varchar(30),in curd char(1), in in_did int(30), out result int(1) )
BEGIN
case curd
when 'A' then INSERT INTO doctor(firstname,lastname,houseno,street,city,state,zipcode,officephoneno,personalphoneno,eccno,eccname,speciality,tbl_last_date) VALUES (in_firstname,in_lastname,in_houseno,in_docstreet,in_city,in_state,in_zipcode,in_offphone,in_perphone,in_eccPhone,in_eccname,in_speciality,sysdate());
when 'U' then update doctor SET firstname=in_firstname,lastname= in_lastname,houseno= in_houseno,street=in_docstreet,city=in_city,state=in_state,zipcode=in_zipcode,officephoneno=in_offphone,personalphoneno=in_perphone,eccno=in_eccPhone,eccname=in_eccname,speciality=in_speciality,tbl_last_date=sysdate() where did=in_did;
when 'D' then delete from doctor where did=in_did;
else set result= -1;
END case; 
end