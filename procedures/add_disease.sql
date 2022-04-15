CREATE DEFINER=`root`@`localhost` PROCEDURE `add_disease`(IN in_icdcodes varchar(30), IN in_diseasename varchar(30),IN in_description varchar(100),IN in_diseasetype varchar(30),in curd char(1), out result int(1) )
BEGIN
case curd
when 'A' then INSERT INTO disease(icdcode,name,description,type,tbl_last_date) VALUES (in_icdcodes,in_diseasename,in_description,in_diseasetype,sysdate());
when 'U' then update disease SET icdcode=in_icdcodes ,name=in_diseasename,description=in_description,type=in_diseasetype,tbl_last_date=sysdate() where  icdcode=in_icdcodes;
when 'D' then delete from disease where icdcode=in_icdcodes;
else set result= -1;
END case; 
end