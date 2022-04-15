CREATE DEFINER=`root`@`localhost` PROCEDURE `create_invoice`( In in_patientID INTEGER(30), IN in_reg_Date DATE, In in_trtmentid INTEGER(30) )
BEGIN
declare maxid DOUBLE;
Insert into invoice (InvoiceDate,pid,reg_date,labcost,prescriptionname,drugcost,surgerycost,roomcost,totalcost,payablebyinsurance,payablebypatient,tbl_last_date)
		Values 
        (sysdate(),
        in_patientID,
        in_reg_Date,
		(select ifnull((select a.cost from lab a join p_lab b on a.labid=b.labid where b.treatmentid=in_trtmentid ),0)as totallabcost),
		(select ifnull((select a.prescriptionname from drug_prescription a join p_drug_pres b on a.drupid=b.drupid where b.treatmentid=in_trtmentid ),'No Prescriptions')as Prescriptions),
		(select ifnull((select a.cost*b.doses from drug_prescription a join p_drug_pres b on a.drupid=b.drupid where b.treatmentid=in_trtmentid ),0)as drugcost),

		(select ifnull((select a.cost from surgery a join p_surgery b on a.surgeryid=b.surgeryid where b.treatmentid=in_trtmentid ),0)as surgerycost),
		(select ifnull((select a.cost from rooms a join inPatient b on a.roomno=b.roomno and a.hid =b.hid where b.pid=in_patientID and b.reg_date= in_reg_Date),0)as roomcost),

		0,
        (select a.inPatientCoverage from insurance_plan a join patients b on a.planid=b.planid where b.pid=in_patientID),
        0,
        sysdate()
        );
        
END