CREATE DEFINER=`root`@`localhost` PROCEDURE `add_treatment`(IN in_patientID int(10), IN in_reg_date DATETIME,IN in_hospitalid int(10),
 IN in_doctorid int(10), IN in_disease varchar(5),IN in_descpt VARCHAR(50), IN in_trtmnt_type CHAR(1), IN in_trtmnt_result CHAR(1),
 IN in_testdate datetime , IN in_labid int(10), IN in_testresult CHAR(1), IN in_drupid int(10), IN in_doses INT(5), 
 IN curd char(1),IN in_trtmntID INTEGER(10), out result int(1) )
BEGIN
	case curd
	when 'A' then INSERT INTO treatment(pid,reg_date,hid,did,icdcode,description,treatmenttype,treatmentresult,tbl_last_date) VALUES (in_patientID,in_reg_date,in_hospitalid,in_doctorid,in_disease,in_descpt,in_trtmnt_type,in_trtmnt_result,sysdate()); 
					COMMIT;
	when 'U' then update treatment SET pid=in_patientID,reg_date=in_reg_date,hid=in_hospitalid,did=in_doctorid,icdcode=in_disease,description=in_descpt,treatmenttype=in_trtmnt_type,treatmentresult=in_trtmnt_result, tbl_last_date=sysdate() where  treatmentid=in_trtmntID;
	when 'D' then delete from treatment where treatmentid=in_trtmntID;
	else set result= -1;
	END case; 

    IF in_trtmnt_type = 'L' then
				case  curd 
                when 'A' then INSERT INTO p_lab(treatmentid,testdate,labid,result,tbl_last_date) VALUES ((select max(treatmentid) from treatment),in_testdate,in_labid,in_testresult,sysdate());
                when 'U'  then update p_lab SET testdate= in_testdate,labid=in_labid,result=in_testresult ,tbl_last_date=sysdate() where treatmentid=in_trtmntID;
                when 'A' then delete from p_lab where treatmentid=in_trtmntID;
                else set result = -1;
                END case;
	ELSEIF in_trtmnt_type = 'D' then
				case  curd 
                when 'A' then INSERT INTO p_drug_pres(treatmentid,drupid,doses,tbl_last_date) VALUES ((select max(treatmentid) from treatment),in_drupid,in_doses,sysdate());
                when 'U'  then update p_drug_pres SET drupid=in_drupid,doses=in_doses,tbl_last_date=sysdate() where treatmentid=in_trtmntID;
                when 'A' then delete from p_drug_pres where treatmentid=in_trtmntID;
                else set result = -1;
                END case;
	ELSEIF in_trtmnt_type='S' then
				case  curd 
                when 'A' then INSERT INTO p_surgery(treatmentid,SurgeryDate,surgeryid,result,tbl_last_date) VALUES ((select max(treatmentid) from treatment),in_testdate,in_labid,in_testresult,sysdate());
                when 'U'  then update p_surgery SET SurgeryDate=in_testdate,surgeryid= in_labid,result= in_testresult,tbl_last_date=sysdate() where treatmentid=in_trtmntID;
                when 'A' then delete from p_surgery where treatmentid=in_trtmntID;
                else set result = -1;
                END case;
				
	ELSE 
	set result = -1;
	END IF;
end