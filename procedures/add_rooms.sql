CREATE DEFINER=`root`@`localhost` PROCEDURE `add_rooms`(IN in_roomNo varchar(30), IN in_Floor SMALLINT,IN in_Building varchar(30),IN in_Cost DECIMAL(6, 2),IN in_Avialability char(1),in curd char(1), in in_hid double, out result int(1) )
BEGIN
case curd
when 'A' then INSERT INTO rooms(hid,roomno,floor,building,cost,availability,tbl_last_date) VALUES (in_hid,in_roomNo,in_Floor,in_Building,in_Cost,in_Avialability,sysdate());
when 'U' then update rooms SET hid=in_hid ,roomno=in_roomNo,floor=in_Floor,building=in_Building,cost=in_Cost,availability=in_Avialability, tbl_last_date=sysdate() where hid=in_hid and roomno= in_roomNo;
when 'D' then delete from rooms where hid=in_hid and roomno= in_roomNo;
else set result= -1;
END case; 
end