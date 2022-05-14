CREATE DEFINER=`root`@`localhost` PROCEDURE `add_insurance`(IN in_insurancename varchar(30), IN in_insuranceprovider varchar(30),IN in_inPatientCoverage DECIMAL(4,2),IN in_outPatientCoverage DECIMAL(4,2),in curd char(1), in in_planid int(10),out result int(1) )
BEGIN
case curd
when 'A' then INSERT INTO insurance_plan(insurancename,insuranceprovider,inPatientCoverage,outPatientCoverage,tbl_last_date) VALUES (in_insurancename,in_insuranceprovider,in_inPatientCoverage,in_outPatientCoverage,sysdate());
when 'U' then update insurance_plan SET insurancename=in_insurancename ,insuranceprovider=in_insuranceprovider,inPatientCoverage=in_inPatientCoverage,outPatientCoverage=in_outPatientCoverage,tbl_last_date=sysdate() where  planid=in_planid;
when 'D' then delete from insurance_plan where planid=in_planid;
else set result= -1;
END case; 
end