CREATE DEFINER=`root`@`localhost` PROCEDURE `add_patient`( IN in_type char(1), IN in_fname varchar(30),IN in_lname varchar(30), IN in_pthousenum varchar(30),IN in_ptstreet varchar(30),IN in_ptcity varchar(30),IN in_ptstate varchar(30), IN in_ptzipcode varchar(30),IN in_ptcontact_number INTEGER(15), IN in_ptdob datetime,IN in_ptRace varchar(30), IN in_Maritial_Status varchar(30), IN in_ptgender char(1) ,IN in_blood_group char(3),IN in_plan_name varchar(30),in curd char(1),IN in_pid INTEGER(10), out result int(1) )
BEGIN
	IF in_type = 'P' then
			CASE curd
			when 'A' then INSERT INTO patients(firstname,lastname,houseno,street,city,state,zipcode,phoneno,dob,race,maritialstatus,gender,bloodgroup,planid,tbl_last_date) VALUES (in_fname,in_lname,in_pthousenum,in_ptstreet,in_ptcity,in_ptstate,in_ptzipcode,in_ptcontact_number,in_ptdob,in_ptRace,in_Maritial_Status,in_ptgender,in_blood_group,(select planid from insurance_plan where insurancename =in_plan_name) ,sysdate());
			when 'U' then update patients SET firstname=in_fname ,lastname=in_lname,houseno=in_pthousenum ,street=in_ptstreet ,city= in_ptcity,state=in_ptstate,zipcode=in_ptzipcode,phoneno=in_ptcontact_number,dob=in_ptdob,race=in_ptRace,maritialstatus=in_Maritial_Status,gender=in_ptgender,bloodgroup=in_blood_group,planid=(select planid from insurance_plan where insurancename =in_plan_name),tbl_last_date=sysdate() where  pid=in_pid;
			when 'D' then delete from patients where pid=in_pid;
			else set result= -1;
			END case;
	ELSEIF in_type = 'E' then
			CASE curd
			when 'A' then INSERT INTO emergency_contact(pid,firstname,lastname,houseno,street,city,state,zipcode,phoneno,relationship,tbl_last_date) VALUES (in_fname,in_lname,in_pthousenum,in_ptstreet,in_ptcity,in_ptstate,in_ptzipcode,in_ptcontact_number,in_ptRace,sysdate());
			when 'U' then update emergency_contact SET pid=in_pid,firstname=in_fname ,lastname=in_lname,houseno=in_pthousenum ,street=in_ptstreet ,city= in_ptcity,state=in_ptstate,zipcode=in_ptzipcode,phoneno=in_ptcontact_number,relationship=in_ptRace,tbl_last_date=sysdate() where  pid=in_pid;
			when 'D' then delete from emergency_contact where pid=in_pid;
			else set result= -1;
			END case;
	ELSE 
		set result= -1;
	END IF;
END