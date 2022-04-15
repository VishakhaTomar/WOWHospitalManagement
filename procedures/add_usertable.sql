CREATE DEFINER=`root`@`localhost` PROCEDURE `add_usertable`(IN in_username varchar(30), IN in_USERPASSWORD varchar(100),IN in_USERTYPE varchar(30), in mnt char(1), in in_userid double, out result int(1) )
BEGIN
case mnt
when 'A' then INSERT INTO usertable(USERNAME, USERPASSWORD,USERTYPE,tbl_last_date) VALUES (in_username,in_USERPASSWORD,in_USERTYPE,sysdate());
when 'U' then update usertable SET USERNAME=in_username ,USERPASSWORD=in_USERPASSWORD,USERTYPE=in_USERTYPE,tbl_last_date=sysdate() where id=in_userid;
when 'D' then delete from usertable where id=in_userid;
else set result= -1;
END case; 
end