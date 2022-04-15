CREATE DEFINER=`root`@`localhost` PROCEDURE `add_doctorhospital`( IN in_doctype char(1),IN in_searchdoctor Int(30), IN in_hospitalid INT(30),IN in_hiredate datetime,IN in_fulsalary DECIMAL(4,2),IN in_contractstartdate datetime, IN in_contractno varchar(30),IN in_contractenddate datetime,  IN in_hours DECIMAL(4,2),IN in_consalary DECIMAL(4,2), IN in_overtimerate DECIMAL(6,2), IN in_shift varchar(30),in curd char(1),out result int(1) )
BEGIN

	case curd
	when 'A' then INSERT INTO hospital_doctor(hid,did,type,tbl_last_date) VALUES (in_hospitalid,in_searchdoctor,in_doctype,sysdate());
    
	when 'U' then update hospital_doctor SET hid=in_hospitalid ,did=in_searchdoctor,type=in_doctype,tbl_last_date=sysdate() where  hid=in_hospitalid and did=in_searchdoctor;
	when 'D' then delete from hospital_doctor where hid=in_hospitalid and did=in_searchdoctor;
	else set result= -1;
	END case; 
    
    IF in_doctype = 'F' then
				case  curd 
                when 'A' then INSERT INTO full_time(hid,did,hiredate,salary,tbl_last_date) VALUES (in_hospitalid,in_searchdoctor,in_hiredate,in_fulsalary,sysdate());
                when 'U'  then update full_time SET hid=in_hospitalid ,did=in_searchdoctor,hiredate=in_hiredate,salary= in_fulsalary,tbl_last_date=sysdate() where  hid=in_hospitalid and did=in_searchdoctor;
                when 'A' then delete from full_time where hid=in_hospitalid and did=in_searchdoctor;
                else set result = -1;
                END case;
                
	ELSEIF in_doctype = 'C' then
				case  curd 
                when 'A' then INSERT INTO consulting(hid,did,contractdate,contractno,contractenddate,hours,salary,overtimerate,shift,tbl_last_date) VALUES (in_hospitalid,in_searchdoctor,in_contractstartdate,in_contractno,in_contractenddate,in_hours,in_consalary,in_overtimerate,in_shift,sysdate());
                when 'U'  then update consulting SET hid=in_hospitalid ,did=in_searchdoctor,contractdate=in_contractstartdate,contractno= in_contractno,contractenddate= in_contractenddate,hours=in_hours ,salary=in_consalary,overtimerate= in_overtimerate,shift=in_shift, tbl_last_date=sysdate() where  hid=in_hospitalid and did=in_searchdoctor;
                when 'A' then delete from consulting where hid=in_hospitalid and did=in_searchdoctor;
                else set result = -1;
                END case;
	ELSE 
	set result = -1;
	END IF;
END