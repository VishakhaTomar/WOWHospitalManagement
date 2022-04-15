CREATE DEFINER=`root`@`localhost` PROCEDURE `add_department`(IN in_deptname varchar(30), IN in_deptphoneno INT(10),IN in_deptbuilding varchar(30),IN in_deptfloor varchar(30),in curd char(1), in in_hid double,in in_did double, out result int(1) )
BEGIN
case curd
when 'A' then INSERT INTO hdepartment(dname,phoneno,buildingname,floor,hid,tbl_last_date) VALUES (in_deptname,in_deptphoneno,in_deptbuilding,in_deptfloor,in_hid,sysdate());
when 'U' then update hdepartment SET hid=in_hid ,dname=in_deptname,phoneno=in_deptphoneno,buildingname=in_deptbuilding,floor=in_deptfloor,tbl_last_date=sysdate() where hid=in_hid and did= in_did;
when 'D' then delete from hdepartment where hid=in_hid and did= in_did;
else set result= -1;
END case; 
end