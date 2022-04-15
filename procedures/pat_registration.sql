CREATE DEFINER = `root` @`localhost` PROCEDURE `pat_registration` (
    IN in_patientID INTEGER (30),
    IN in_reg_Date DATE,
    IN in_hospitalID INTEGER (30),
    IN in_patient_type char (1),
    IN in_followup date,
    IN in_roomNo INTEGER (10),
    IN in_discharge_date DATE,
    IN curd char (1),
    out result int (1)
) 
BEGIN 
declare roomnumber INTEGER (10);

    CASE curd
        WHEN 'A' THEN 
            BEGIN
                INSERT INTO  patient_reg (pid, reg_date, hid, patient_type, tbl_last_date)
                VALUES
                    (
                        in_patientID,in_reg_Date,in_hospitalID,in_patient_type,sysdate()
                    );
            END;

        WHEN 'U' THEN
            UPDATE patient_reg 
            SET 
                hid = in_hospitalID, patient_type = in_patient_type, tbl_last_date = sysdate()
            WHERE
                pid = in_patientID AND reg_date = in_reg_Date;

        WHEN 'D' THEN
            DELETE FROM patient_reg
            WHERE
                pid = in_patientID AND reg_date = in_reg_Date;

        ELSE
            SET result = -1;

    END CASE;

    IF in_patient_type = 'I' THEN 
        CASE curd
            WHEN 'A' THEN 
            BEGIN
                INSERT INTO inPatient (pid, reg_date, dischargedate, roomno, hid)
                VALUES
                    (
                        in_patientID, in_reg_Date,in_discharge_date,in_roomNo,in_hospitalID
                    );

                UPDATE rooms
                SET
                    availability = 'N'
                WHERE
                    hid = in_hospitalID
                    AND roomno = in_roomNo;

            END;

            WHEN 'U' THEN 
            BEGIN
                SELECT
                roomno INTO roomnumber
                FROM
                    inPatient
                WHERE
                    pid = in_patientID
                    AND reg_date = in_reg_Date;

                UPDATE
                    inPatient
                SET
                    dischargedate = in_discharge_date,
                    roomno = in_roomNo,
                    hid = in_hospitalID
                WHERE
                    pid = in_patientID
                    AND reg_date = in_reg_Date;

                UPDATE
                    rooms
                SET
                    availability = 'N'
                WHERE
                    hid = in_hospitalID
                    AND roomno = in_roomNo;

                UPDATE
                    rooms
                SET
                    availability = 'Y'
                WHERE
                    hid = in_hospitalID
                    AND roomno = roomnumber;

            END;

            WHEN 'D' THEN 
                BEGIN
                UPDATE
                    rooms
                SET
                    availability = 'Y'
                WHERE
                    hid = in_hospitalID AND roomno = roomnumber;

                DELETE FROM
                    inPatient
                WHERE
                    pid = in_patientID AND reg_date = in_reg_Date;

                UPDATE
                    rooms
                SET
                    availability = 'Y'
                WHERE
                    hid = in_hospitalID  AND roomno = roomnumber;

                END;

            ELSE  SET
                result = -1;

        END CASE;

    ELSEIF in_patient_type = 'O' THEN 
        CASE  curd
            WHEN 'A' THEN
                INSERT INTO
                    outPatient (pid, reg_date, followupdate)
                VALUES
                    (in_patientID, in_reg_Date, in_followup);

            WHEN 'U' THEN
            UPDATE
                outPatient
            SET
                followupdate = in_followup
            WHERE
                pid = in_patientID AND reg_date = in_reg_Date;

        WHEN 'D' THEN
            DELETE FROM
                outPatient
            WHERE
                pid = in_patientID AND reg_date = in_reg_Date;

        ELSE SET
            result = -1;

        END CASE;

    ELSE
    SET
        result = -1;

    END IF;

END