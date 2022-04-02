create database vishakhadb;

use vishakhadb;

CREATE TABLE usertable (
    ID DOUBLE NOT NULL AUTO_INCREMENT,
    USERNAME VARCHAR(30),
    USERPASSWORD VARCHAR(100),
    USERTYPE VARCHAR(10)
    );
ALTER TABLE USERTABLE ADD CONSTRAINT USERTABLE_PK PRIMARY KEY( ID );

INSERT INTO usertable (USERNAME, USERPASSWORD,USERTYPE) VALUES ('Admin1','4356a21b1b6643f1514a7c50e80d6fbdc0486a97567d193ce483c2538493713a','A');
INSERT INTO usertable (USERNAME, USERPASSWORD,USERTYPE) VALUES ('Tom','4356a21b1b6643f1514a7c50e80d6fbdc0486a97567d193ce483c2538493713a','F');
INSERT INTO usertable (USERNAME, USERPASSWORD,USERTYPE) VALUES ('Harry','4356a21b1b6643f1514a7c50e80d6fbdc0486a97567d193ce483c2538493713a','B');


CREATE PROCEDURE add_usertable (IN in_username varchar, IN in_USERPASSWORD varchar,IN in_USERTYPE varchar )
BEGIN
INSERT INTO usertable(USERNAME, USERPASSWORD,USERTYPE,tbl_last_date) VALUES (in_username,in_USERPASSWORD,in_USERTYPE,sysdate);

END; 

CREATE TABLE hospital (
    hid           DOUBLE NOT NULL primary key AUTO_INCREMENT,
    plotno        VARCHAR(30),
    street        VARCHAR(30),
    city          VARCHAR(30),
    state         VARCHAR(30),
    zipcode       VARCHAR(30),
    speciality    VARCHAR(30) COMMENT 'Speciality of the hospital(Heart/Cancer/Surgery)',
    ecchotline    BIGINT COMMENT 'EmergencyHotlineNumber',
    phoneno       BIGINT,
    adminphone    BIGINT,
    tbl_last_date DATETIME
);


CREATE TABLE hdepartment (
    did           DOUBLE NOT NULL PRIMARY KEY AUTO_INCREMENT, 
    dname         VARCHAR(30) COMMENT 'DepartmentName',
    phoneno       BIGINT,
    buildingname  VARCHAR(30),
    floor         VARCHAR(30) COMMENT 'Location of the dept, Floor in the building',
    hid           DOUBLE NOT NULL,
    tbl_last_date DATETIME
);


CREATE TABLE rooms (
    hid           DOUBLE NOT NULL,
    roomno        DOUBLE NOT NULL,
    floor         SMALLINT,
    building      VARCHAR(30),
    cost          DECIMAL(6, 2) COMMENT 'CostperNightoftheRoom',
    availability  CHAR(1) COMMENT 'RoomAvailableOrNot',
    tbl_last_date DATETIME
);

ALTER TABLE rooms ADD CONSTRAINT rooms_pk PRIMARY KEY ( roomno,
                                                        hid );


CREATE TABLE doctor (
    did             DOUBLE PRIMARY KEY AUTO_INCREMENT NOT NULL COMMENT 'DoctorId',
    firstname       VARCHAR(30),
    lastname        VARCHAR(30),
    houseno         VARCHAR(30),
    street          VARCHAR(30),
    city            VARCHAR(30),
    state           VARCHAR(30),
    zipcode         VARCHAR(30),
    officephoneno   BIGINT,
    personalphoneno BIGINT,
    eccno           BIGINT COMMENT 'Emergency call No',
    eccname         VARCHAR(30),
    speciality      VARCHAR(30),
    tbl_last_date   DATETIME
);


CREATE TABLE hospital_doctor (
    hid           DOUBLE NOT NULL,
    did           DOUBLE NOT NULL,
    type          CHAR(1) COMMENT 'EitherFulltimeDoctororCunsultant',
    tbl_last_date DATETIME
);
ALTER TABLE hospital_doctor ADD CONSTRAINT hospital_doctor_pk PRIMARY KEY ( hid,
                                                                            did );
CREATE TABLE consulting (
    hid             DOUBLE NOT NULL,
    did             DOUBLE NOT NULL,
    contractdate    DATETIME COMMENT 'ContractStartDate',
    contractno      VARCHAR(30),
    contractenddate DATETIME,
    hours           DECIMAL(4, 2) COMMENT 'NoOfHoursWorking',
    salary          DECIMAL(10, 2) COMMENT 'SalaryPerHour',
    overtimerate    DECIMAL(10, 2) COMMENT 'OvertimeSalary',
    shift           DATETIME
);
alter table consulting modify COLUMN shift VARCHAR(30);
ALTER TABLE consulting ADD CONSTRAINT consulting_pk PRIMARY KEY ( hid,
                                                                  did );
CREATE TABLE full_time (
    hid      DOUBLE NOT NULL,
    did      DOUBLE NOT NULL,
    hiredate DATETIME,
    salary   DECIMAL(10, 2)
);
ALTER TABLE full_time ADD CONSTRAINT full_time_pk PRIMARY KEY ( hid,
                                                                did );
CREATE TABLE disease (
    icdcode       VARCHAR(5) NOT NULL,
    name          VARCHAR(30) NOT NULL,
    description   VARCHAR(30) NOT NULL,
    type          VARCHAR(30) NOT NULL COMMENT 'TypeofDisease(Seasonal/chronic/viral/genetic..etc)',
    tbl_last_date DATETIME
);
ALTER TABLE disease ADD CONSTRAINT disease_pk PRIMARY KEY ( icdcode );


/*CHANGED*/ 
CREATE TABLE insurance_plan (
    planid                DOUBLE NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'InsurancePlanId',
    insurancename         VARCHAR(30) NOT NULL,
    insuranceprovider     VARCHAR(30) NOT NULL COMMENT 'InsuranceCompany',
    inPatientCoverage  DECIMAL(4, 2) NOT NULL,
    outPatientCoverage DECIMAL(4, 2) NOT NULL,
    tbl_last_date         DATETIME
);


CREATE TABLE patients (
    pid            DOUBLE NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Patient Id',
    firstname      VARCHAR(30),
    lastname       VARCHAR(30),
    houseno        VARCHAR(30),
    street         VARCHAR(30),
    city           VARCHAR(30),
    state          VARCHAR(30),
    zipcode        VARCHAR(30),
    phoneno        BIGINT,
    dob            DATETIME COMMENT 'DateOfBirth',
    race           VARCHAR(30),
    maritialstatus VARCHAR(30),
    gender         CHAR(1),
    bloodgroup     CHAR(3),
    planid         DOUBLE NOT NULL,
    tbl_last_date  DATETIME
);

CREATE UNIQUE INDEX patients__idx ON
    patients (
        planid
    ASC );

CREATE TABLE emergency_contact (
    ecid          DOUBLE NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'EmergencyContactId',
    pid           DOUBLE NOT NULL,
    firstname     VARCHAR(30),
    lastname      VARCHAR(30),
    houseno       VARCHAR(30),
    street        VARCHAR(30),
    city          VARCHAR(30),
    state         VARCHAR(30),
    zipcode       VARCHAR(30),
    phoneno       BIGINT,
    relationship  VARCHAR(30) COMMENT 'Relationship to the Patient',
    tbl_last_date DATETIME
);


CREATE TABLE pat_appointment (
    pid                   DOUBLE NOT NULL ,
    appointmentid         BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    nextvisitdateschedued DATETIME,
    visitdatecheckin      CHAR(1) COMMENT 'Visit date will be checked in yes when patient make it to the appointment',
    tbl_last_date         DATETIME
);



CREATE TABLE patient_reg (
    pid           DOUBLE NOT NULL,
    reg_date      DATETIME NOT NULL,
    patient_type  CHAR(1) NOT NULL,
    tbl_last_date DATETIME
);

ALTER TABLE patient_reg ADD CONSTRAINT patient_reg_pk PRIMARY KEY ( pid,reg_date);

CREATE TABLE inPatient (
    pid                DOUBLE NOT NULL,
    reg_date           DATETIME NOT NULL,
    dischargedate      DATETIME NOT NULL,
    roomno       DOUBLE,
    hid DOUBLE
);

ALTER TABLE inPatient ADD CONSTRAINT inPatient_PK PRIMARY KEY ( pid,
                                                                      reg_date );
CREATE TABLE outPatient (
    pid          DOUBLE NOT NULL,
    hid          DOUBLE
    reg_date     DATETIME NOT NULL,
    followupdate DATETIME NOT NULL
);

ALTER TABLE outPatient ADD CONSTRAINT outPatient_PK PRIMARY KEY ( pid,
                                                                        reg_date );


CREATE TABLE treatment (
    treatmentid     DOUBLE NOT NULL PRIMARY KEY AUTO_INCREMENT,
    treatmenttype   CHAR(1) NOT NULL,
    pid             DOUBLE NOT NULL,
    reg_date        DATETIME NOT NULL,
    treatmentresult CHAR(1) NOT NULL COMMENT 'CforComplete/FforFail/TforTerminated',
    description     VARCHAR(50),
    hid             DOUBLE NOT NULL,
    did             DOUBLE NOT NULL,
    icdcode         VARCHAR(5),
    tbl_last_date   DATETIME
);



CREATE TABLE drug_prescription (
    drupid           SMALLINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    prescriptionname VARCHAR(30) NOT NULL,
    cost             DECIMAL(6, 2) NOT NULL COMMENT 'Cost_per_dose',
    tbl_last_date    DATETIME
);


CREATE TABLE lab (
    labid         DOUBLE NOT NULL  PRIMARY KEY AUTO_INCREMENT,
    labname       VARCHAR(30) NOT NULL,
    cost          DECIMAL(6, 2) NOT NULL,
    sample        VARCHAR(30) NOT NULL COMMENT 'type of sample required',
    tbl_last_date DATETIME
);


CREATE TABLE surgery (
    surgeryid     SMALLINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    surgeryname   VARCHAR(30) NOT NULL,
    description   VARCHAR(30) NOT NULL,
    cost          DECIMAL(6, 2) NOT NULL,
    tbl_last_date DATETIME
);
alter table surgery drop COLUMN time;

CREATE TABLE p_drug_pres (
    treatmentid DOUBLE NOT NULL,
    drupid      SMALLINT,
    doses       DOUBLE NOT NULL COMMENT 'No_of_Doses'
);

ALTER TABLE p_drug_pres ADD CONSTRAINT p_drug_pres_pk PRIMARY KEY ( treatmentid );


CREATE TABLE p_lab (
    treatmentid DOUBLE NOT NULL,
    testdate    DATETIME NOT NULL,
    labid       DOUBLE,
    testtype    VARCHAR(30) COMMENT 'what_type_of_test_it_is',
    result      CHAR(1) COMMENT 'Positvie/Negative/potential'
);
ALTER TABLE p_lab ADD CONSTRAINT p_lab_pk PRIMARY KEY ( treatmentid,
                                                        testdate );


CREATE TABLE p_surgery (
    treatmentid DOUBLE NOT NULL,
    SurgeryDate      DATETIME NOT NULL,
    surgeryid   SMALLINT,
    result      CHAR(1) COMMENT 'SforSuccessfull/UforUnsuccessfull'
);
ALTER TABLE p_surgery ADD CONSTRAINT p_surgery_pk PRIMARY KEY ( treatmentid,SurgeryDate );



CREATE TABLE invoice (
    invoiceno          BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    InvoiceDate             DATETIME NOT NULL,
    pid                DOUBLE NOT NULL,
    reg_date           DATETIME NOT NULL,
    labcost            DECIMAL(6, 2) NOT NULL,
    prescriptionname   VARCHAR(30) NOT NULL,
    drugcost           DECIMAL(6, 2) NOT NULL,
    surgerycost        DECIMAL(6, 2) NOT NULL,
    roomcost           DECIMAL(6, 2) NOT NULL,
    totalcost          DECIMAL(6, 2) NOT NULL,
    payablebypatient   DECIMAL(6, 2) NOT NULL,
    payablebyinsurance DECIMAL(6, 2) NOT NULL,
    tbl_last_date      DATETIME
);
/*ALTER TABLE invoice MODIFY COLUMN pid DOUBLE NOT NULL;*/
CREATE UNIQUE INDEX invoice__idx ON
    invoice (
        pid
    ASC,
        reg_date
    ASC );




CREATE TABLE payment_insurance (
    invoiceno     BIGINT NOT NULL,
    paymentmethod VARCHAR(30),
    tbl_last_date DATETIME
);
ALTER TABLE payment_insurance ADD CONSTRAINT invoice_pk PRIMARY KEY ( invoiceno );

CREATE TABLE payment_patient (
    invoiceno     BIGINT NOT NULL,
    creditcardno  BIGINT,
    cardtype      VARCHAR(30) COMMENT 'Mater/Maestro/Visa',
    tbl_last_date DATETIME
);
ALTER TABLE payment_patient ADD CONSTRAINT invoice_pk PRIMARY KEY ( invoiceno );




ALTER TABLE consulting
    ADD CONSTRAINT consulting_hospital_doctor_fk FOREIGN KEY ( hid,
                                                               did )
        REFERENCES hospital_doctor ( hid,
                                     did );

ALTER TABLE emergency_contact
    ADD CONSTRAINT emergency_contact_patients_fk FOREIGN KEY ( pid )
        REFERENCES patients ( pid );

ALTER TABLE full_time
    ADD CONSTRAINT full_time_hospital_doctor_fk FOREIGN KEY ( hid,
                                                              did )
        REFERENCES hospital_doctor ( hid,
                                     did );

ALTER TABLE hdepartment
    ADD CONSTRAINT hdepartment_hospital_fk FOREIGN KEY ( hid )
        REFERENCES hospital ( hid );

ALTER TABLE hospital_doctor
    ADD CONSTRAINT hospital_doctor_doctor_fk FOREIGN KEY ( did )
        REFERENCES doctor ( did );

ALTER TABLE hospital_doctor
    ADD CONSTRAINT hospital_doctor_hospital_fk FOREIGN KEY ( hid )
        REFERENCES hospital ( hid );

ALTER TABLE inPatient
    ADD CONSTRAINT inPatient_Patient_Reg_FK FOREIGN KEY ( pid,
                                                             reg_date )
        REFERENCES patient_reg ( pid,
                                 reg_date );

ALTER TABLE inPatient
    ADD CONSTRAINT inPatient_Rooms_FK FOREIGN KEY ( roomno,
                                                       hid )
        REFERENCES rooms ( roomno,
                           hid );

ALTER TABLE invoice
    ADD CONSTRAINT invoice_patient_reg_fk FOREIGN KEY ( pid,
                                                        reg_date )
        REFERENCES patient_reg ( pid,
                                 reg_date );

ALTER TABLE outPatient
    ADD CONSTRAINT OutPatient_Patient_Reg_FK FOREIGN KEY ( pid,
                                                              reg_date )
        REFERENCES patient_reg ( pid,
                                 reg_date );

ALTER TABLE p_drug_pres
    ADD CONSTRAINT p_drug_pres_drug_prescription_fk FOREIGN KEY ( drupid )
        REFERENCES drug_prescription ( drupid );

ALTER TABLE p_drug_pres
    ADD CONSTRAINT p_drug_pres_treatment_fk FOREIGN KEY ( treatmentid )
        REFERENCES treatment ( treatmentid );
/**/
ALTER TABLE p_lab
    ADD CONSTRAINT p_lab_lab_fk FOREIGN KEY ( labid )
        REFERENCES lab ( labid );

ALTER TABLE p_lab
    ADD CONSTRAINT p_lab_treatment_fk FOREIGN KEY ( treatmentid )
        REFERENCES treatment ( treatmentid );

ALTER TABLE p_surgery
    ADD CONSTRAINT p_surgery_surgery_fk FOREIGN KEY ( surgeryid )
        REFERENCES surgery ( surgeryid );

ALTER TABLE p_surgery
    ADD CONSTRAINT p_surgery_treatment_fk FOREIGN KEY ( treatmentid )
        REFERENCES treatment ( treatmentid );

ALTER TABLE pat_appointment
    ADD CONSTRAINT pat_appointment_patients_fk FOREIGN KEY ( pid )
        REFERENCES patients ( pid );

ALTER TABLE patient_reg
    ADD CONSTRAINT patient_reg_patients_fk FOREIGN KEY ( pid )
        REFERENCES patients ( pid );

ALTER TABLE patients
    ADD CONSTRAINT patients_insurance_plan_fk FOREIGN KEY ( planid )
        REFERENCES insurance_plan ( planid );

ALTER TABLE payment_insurance
    ADD CONSTRAINT payment_insurance_invoice_fk FOREIGN KEY ( invoiceno )
        REFERENCES invoice ( invoiceno );

ALTER TABLE payment_patient
    ADD CONSTRAINT payment_patient_invoice_fk FOREIGN KEY ( invoiceno )
        REFERENCES invoice ( invoiceno );

ALTER TABLE rooms
    ADD CONSTRAINT rooms_hospital_fk FOREIGN KEY ( hid )
        REFERENCES hospital ( hid );

ALTER TABLE treatment
    ADD CONSTRAINT treatment_disease_fk FOREIGN KEY ( icdcode )
        REFERENCES disease ( icdcode );
/**/
ALTER TABLE treatment
    ADD CONSTRAINT treatment_hospital_doctor_fk FOREIGN KEY ( hid,
                                                              did )
        REFERENCES hospital_doctor ( hid,
                                     did );

ALTER TABLE treatment
    ADD CONSTRAINT treatment_patient_reg_fk FOREIGN KEY ( pid,
                                                          reg_date )
        REFERENCES patient_reg ( pid,
                                 reg_date );

ALTER TABLE usertable AUTO_INCREMENT=100;
ALTER TABLE hospital AUTO_INCREMENT=200;
ALTER TABLE hdepartment AUTO_INCREMENT=300;
ALTER TABLE doctor AUTO_INCREMENT=400;
ALTER TABLE insurance_plan AUTO_INCREMENT=1000000;
ALTER TABLE patients AUTO_INCREMENT=20000;
ALTER TABLE emergency_contact AUTO_INCREMENT=2000;
ALTER TABLE pat_appointment AUTO_INCREMENT=900000;
ALTER TABLE treatment AUTO_INCREMENT=8000000;
ALTER TABLE drug_prescription AUTO_INCREMENT=60;
ALTER TABLE lab AUTO_INCREMENT=70000;
ALTER TABLE surgery AUTO_INCREMENT=79000;
ALTER TABLE invoice AUTO_INCREMENT=11990000;

