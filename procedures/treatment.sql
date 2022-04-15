CREATE DEFINER=`root`@`localhost` PROCEDURE `appointments`(IN in_type CHAR(1),IN in_patientID int(10), IN in_apptDate DATETIME, IN curd char(1),IN in_aptID INTEGER(10), out result int(1) )
BEGIN
case curd
when 'A' then 
begin
	IF in_type ='B' then
    begin
			INSERT INTO pat_appointment(pid,nextvisitdateschedued,visitdatecheckin,tbl_last_date) VALUES (in_patientID,in_apptDate,'N',sysdate());
	end;
	ELSEIF in_type ='C' then
	begin
			UPDATE pat_appointment SET visitdatecheckin='Y' WHERE appointmentid=in_aptID;
	end;
	ELSE set result= -1;
    END IF;
end;
when 'U' then UPDATE pat_appointment SET pid=in_patientID,nextvisitdateschedued=in_apptDate,visitdatecheckin='N' WHERE appointmentid=in_aptID;
when 'D' then delete from pat_appointment where appointmentid=in_aptID;
else set result= -1;
END case; 
end