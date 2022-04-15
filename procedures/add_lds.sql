CREATE DEFINER=`root`@`localhost` PROCEDURE `add_lds`( IN in_type char(1),IN in_labname varchar(30), IN in_labcost DECIMAL(4,2),IN in_labsample varchar(30),IN in_prescriptionname varchar(30),IN in_drugcost DECIMAL(4,2),IN in_surgeryname varchar(30), IN in_surgerydescription varchar(30),IN insurgerycost DECIMAL(6,2) ,in curd char(1), in in_inputid int(10),out result int(1) )
BEGIN
IF in_type ="L" then 
	case curd
	when 'A' then INSERT INTO lab(labname,cost,sample,tbl_last_date) VALUES (in_labname,in_labcost,in_labsample,sysdate());
	when 'U' then update lab SET labname=in_labname ,cost=in_labcost,sample=in_labsample,tbl_last_date=sysdate() where  labid=in_inputid;
	when 'D' then delete from lab where labid=in_inputid;
	else set result= -1;
	END case; 

ELSEIF in_type ="S" then
	case curd
	when 'A' then INSERT INTO surgery(surgeryname,description,cost,tbl_last_date) VALUES (in_surgeryname,in_surgerydescription,insurgerycost,sysdate());
	when 'U' then update surgery SET surgeryname=in_surgeryname,description= in_surgerydescription,cost=insurgerycost,tbl_last_date=sysdate() where  surgeryid=in_inputid;
	when 'D' then delete from surgery where surgeryid=in_inputid;
	else set result= -1;
	END case;

ELSEIF in_type ="D" then
	case curd
	when 'A' then INSERT INTO drug_prescription(prescriptionname,cost,tbl_last_date) VALUES (in_prescriptionname,in_drugcost,sysdate());
	when 'U' then update drug_prescription SET prescriptionname=in_prescriptionname ,cost=in_drugcost,tbl_last_date=sysdate() where  drupid=in_inputid;
	when 'D' then delete from drug_prescription where drupid=in_inputid;
	else set result= -1;
	END case; 

ELSE 
	set result = -1;
END IF;
end