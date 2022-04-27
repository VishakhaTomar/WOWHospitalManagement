--HISTORY TABLE

--Patient table-----------------------------------------------------------------------

CREATE TABLE patients_HISTORY AS SELECT * FROM patients WHERE 1=2;
ALTER TABLE patients_HISTORY ADD CONSTRAINT pk_patients_HISTORY PRIMARY KEY (pid);

            --trigger
CREATE DEFINER=`root`@`localhost` TRIGGER `patients_BEFORE_DELETE` BEFORE DELETE ON `patients` FOR EACH ROW 
BEGIN
INSERT INTO patients_HISTORY SELECT * FROM patients WHERE pid=OLD.pid;
  update patients_HISTORY 
  set tbl_last_date=current_timestamp()
  where pid=OLD.pid;
END

-- pat_registration table-------------------------------------------------------------------
CREATE TABLE patient_reg_HISTORY AS SELECT * FROM patient_reg WHERE 1=2;
ALTER TABLE patient_reg_HISTORY ADD CONSTRAINT pk_patient_reg_HISTORY PRIMARY KEY (pid, reg_date);
                            
            ---trigger
CREATE DEFINER=`root`@`localhost` TRIGGER `patient_reg_BEFORE_DELETE` BEFORE DELETE ON `patient_reg` FOR EACH ROW 
BEGIN
INSERT INTO patient_reg_HISTORY SELECT * FROM patient_reg WHERE pid=OLD.pid and reg_date=OLD.reg_date;
  update patient_reg_HISTORY 
  set tbl_last_date=current_timestamp()
  where pid=OLD.pid and reg_date=OLD.reg_date;
END


--pat_treatment table-----------------------------------------------------------------------
CREATE TABLE treatment_HISTORY AS SELECT * FROM treatment WHERE 1=2;
ALTER TABLE treatment_HISTORY ADD CONSTRAINT pk_treatment_HISTORY PRIMARY KEY (treatmentid);
                            
            ---trigger
CREATE DEFINER=`root`@`localhost` TRIGGER `treatment_BEFORE_DELETE` BEFORE DELETE ON `treatment` FOR EACH ROW 
BEGIN
INSERT INTO treatment_HISTORY SELECT * FROM treatment WHERE treatmentid=OLD.treatmentid;
  update treatment_HISTORY 
  set tbl_last_date=current_timestamp()
  where treatmentid=OLD.treatmentid;
END

--doctor table-----------------------------------------------------------------------
CREATE TABLE doctor_HISTORY AS SELECT * FROM doctor WHERE 1=2;
ALTER TABLE doctor_HISTORY ADD CONSTRAINT pk_doctor_HISTORY PRIMARY KEY (did);
                            
            ---trigger
CREATE DEFINER=`root`@`localhost` TRIGGER `doctor_BEFORE_DELETE` BEFORE DELETE ON `doctor` FOR EACH ROW 
BEGIN
INSERT INTO doctor_HISTORY SELECT * FROM doctor WHERE did=OLD.did;
  update doctor_HISTORY 
  set tbl_last_date=current_timestamp()
  where did=OLD.did;
END


--hospital table-----------------------------------------------------------------------
CREATE TABLE hospital_HISTORY AS SELECT * FROM hospital WHERE 1=2;
ALTER TABLE hospital_HISTORY ADD CONSTRAINT pk_hospital_HISTORY PRIMARY KEY (hid);
                            
            ---trigger
CREATE DEFINER=`root`@`localhost` TRIGGER `hospital_BEFORE_DELETE` BEFORE DELETE ON `hospital` FOR EACH ROW
BEGIN
INSERT INTO hospital_HISTORY SELECT * FROM hospital WHERE hid=OLD.hid;
  update hospital_HISTORY 
  set tbl_last_date=current_timestamp()
  where hid=OLD.hid;
END


--doctor_hospital table-----------------------------------------------------------------------
CREATE TABLE hospital_doctor_HISTORY AS SELECT * FROM hospital_doctor WHERE 1=2;
ALTER TABLE hospital_doctor_HISTORY ADD CONSTRAINT pk_hospital_doctor_HISTORY PRIMARY KEY (did, hid);
                            
            ---trigger
CREATE DEFINER=`root`@`localhost` TRIGGER `hospital_doctor_BEFORE_DELETE` BEFORE DELETE ON `hospital_doctor` FOR EACH ROW
BEGIN
  INSERT INTO hospital_doctor_HISTORY SELECT * FROM hospital_doctor WHERE did=OLD.did and hid=OLD.hid;
  update hospital_doctor_HISTORY 
  set tbl_last_date=current_timestamp()
  where did=OLD.did and hid=OLD.hid;
END


--invoice table-----------------------------------------------------------------------
CREATE TABLE invoice_HISTORY AS SELECT * FROM invoice WHERE 1=2;
ALTER TABLE invoice_HISTORY ADD CONSTRAINT pk_invoice_HISTORY PRIMARY KEY (invoiceno);
                            
            ---trigger
CREATE DEFINER=`root`@`localhost` TRIGGER `invoice_BEFORE_DELETE` BEFORE DELETE ON `invoice` FOR EACH ROW
BEGIN
INSERT INTO invoice_HISTORY SELECT * FROM invoice WHERE invoiceno=OLD.invoiceno;
  update invoice_HISTORY 
  set tbl_last_date=current_timestamp()
  where invoiceno=OLD.invoiceno;
END


------------------------------------------------------------------------------------------------------------------------------------
--DENORMALISED TABLES
------------------------------------------------------------------------------------------------------------------------------------

---------hospital table-

CREATE TABLE dw_hospital (
    hid           BIGINT(10) NOT NULL,
    hname         VARCHAR(30),
    city          VARCHAR(30),
    state         VARCHAR(30),
    zipcode       VARCHAR(30),
    speciality    VARCHAR(30) COMMENT 'Speciality of the hospital(Heart/Cancer/Surgery)',
    dptid         BIGINT(10) NOT NULL, 
    dname         VARCHAR(30) COMMENT 'DepartmentName',
    buildingname  VARCHAR(30),
    floor         VARCHAR(30) COMMENT 'Location of the dept, Floor in the building',
    roomno        VARCHAR(30),
    cost          DECIMAL(6, 2) COMMENT 'CostperNightoftheRoom',
    did             BIGINT(10) NOT NULL COMMENT 'DoctorId',
    firstname       VARCHAR(30),
    lastname        VARCHAR(30),
    docspeciality      VARCHAR(30),
    doctype            CHAR(1) COMMENT 'EitherFulltimeDoctororCunsultant',
    contractdate    DATE COMMENT 'ContractStartDate',
    contractenddate DATE,
    hours           DECIMAL(4, 2) COMMENT 'NoOfHoursWorking',
    con_salary      DECIMAL(5, 2) COMMENT 'SalaryPerHour',
    overtimerate    DECIMAL(5, 2) COMMENT 'OvertimeSalary',
    shift           VARCHAR(7) COMMENT 'Shiftdays',),
    hiredate        DATE,
    full_salary     DECIMAL(10, 2),
    tbl_last_date   DATETIME
)PARTITION by list (type)
          PARTITION P11 VALUES ('F'), 
          PARTITION P12 VALUES ('C')
         ); 



--pat_reg_treatment table----




CREATE TABLE dw_patients (
    pid           INT NOT NULL,
    firstname      VARCHAR,
    lastname       VARCHAR,
    city           VARCHAR,
    state          VARCHAR,
    zipcode        VARCHAR,
    dob            DATE ,
    race           VARCHAR,
    maritialstatus VARCHAR,
    gender         CHAR(1),
    bloodgroup     CHAR(3),
    reg_date        DATE ,
    hid             INT, 
    planid         INT,
    patient_type    CHAR(1) ,
    dischargedate      DATE ,
    roomno          INT,
    treatmentid     INT,
    treatmenttype   CHAR(1) ,
    treatmentresult CHAR(1) ,
    did             INT,
    icdcode         VARCHAR(5), 
    invoiceno          INT,
    InvoiceDate             DATE,
    labcost            DECIMAL(6, 2),
    drugcost           DECIMAL(6, 2),
    surgerycost        DECIMAL(6, 2),
    roomcost           DECIMAL(6, 2),
    totalcost          DECIMAL(6, 2),
    payablebypatient   DECIMAL(6, 2),
    payablebyinsurance DECIMAL(6, 2),
    tbl_last_date  timestamp
);
)  PARTITION BY RANGE (dob) 
      ( PARTITION P1 VALUES less than(to_date('01-JAN-1985', 'DD-MON-YYYY')),   
        PARTITION P2 VALUES less than(to_date('01-JAN-2000', 'DD-MON-YYYY')),   
        PARTITION  P3 VALUES less than(to_date('01-JAN-2015', 'DD-MON-YYYY')),   
        PARTITION  P4 VALUES less than(to_date('01-JAN-2030', 'DD-MON-YYYY'))  
      );



-- ALTER TABLE dw_patients_insurance_invoice ADD CONSTRAINT dw_patients_insurance_invoice_PK PRIMARY KEY ( invoiceno,pid,reg_date );


select d.hid,b.city, b.state,b.zipcode,b.speciality ,a.did, a.dname , a.buildingname,a.floor,c.roomno,c.cost,
d.did, e.firstname, e.lastname, e.speciality, d.type, g.contractdate, g.contractenddate, g.hours, g.salary , g.overtimerate,
g.shift
from
hdepartment a, hospital b,rooms c,hospital_doctor d,doctor e,consulting g 
where 
    a.hid = b.hid and
    c.hid = b.hid and
    d.hid = b.hid and
    g.hid = d.hid and
    e.did = d.did and
    d.did = g.did 
union 
select d.hid, b.hname,b.city, b.state,b.zipcode,b.speciality ,a.did, a.dname , a.buildingname,a.floor,c.roomno,c.cost,
d.did, e.firstname, e.lastname, e.speciality, d.type,f.hiredate, f.salary 
from 
hdepartment a, hospital b,rooms c,hospital_doctor d,doctor e ,full_time f
where 
    a.hid = b.hid and
    c.hid = b.hid and
    d.hid = b.hid and
    f.hid = d.hid and
    e.did= d.did and
    d.did = f.did 
    


------------------------------------------------------------------------------------------------------------------------------------
----PARTITIONS IN OLTP------------------------
-----------------------------------------------------------------------------------------------------------------------------------


select b.pid,a.firstname,a.lastname,a.city,a.state,a.zipcode,a.dob,a.race, a.maritialstatus, a.gender, a.bloodgroup, a.planid, b.reg_date,b.hid, d.icdcode,b.patient_type,c.dischargedate, c.roomno, d.treatmentid,d.treatmenttype, d.treatmentresult, d.did, e.invoiceno,e.InvoiceDate,e.labcost,e.drugcost, e.surgerycost,e.roomcost, e.totalcost, e.payablebypatient, e.payablebyinsurance
from 
patients a, patient_reg b, inpatient c, treatment d, invoice e
where   b.pid=a.pid and
        b.reg_date=c.reg_date and
        b.pid=c.pid and
        b.pid=d.pid and
        b.reg_date=d.reg_date and
        b.pid=e.pid and
        b.reg_date=e.reg_date

Oupatient:

select b.pid,a.firstname,a.lastname,a.city,a.state,a.zipcode,a.dob,a.race, a.maritialstatus, a.gender, a.bloodgroup, a.planid, b.reg_date,b.hid, d.icdcode,b.patient_type, d.treatmentid,d.treatmenttype, d.treatmentresult, d.did, e.invoiceno,e.InvoiceDate,e.labcost,e.drugcost, e.surgerycost,e.roomcost, e.totalcost, e.payablebypatient, e.payablebyinsurance
from 
patients a, patient_reg b, outpatient c, treatment d, invoice e
where   b.pid=a.pid and
        b.reg_date=c.reg_date and
        b.pid=c.pid and
        b.pid=d.pid and
        b.reg_date=d.reg_date and
        b.pid=e.pid and
        b.reg_date=e.reg_date