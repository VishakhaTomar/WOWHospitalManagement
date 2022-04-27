CREATE DEFINER=`VishakhaTomar`@`%` TRIGGER `vishakhadb`.`treatment_AFTER_UPDATE` AFTER UPDATE ON `treatment` FOR EACH ROW
BEGIN
    declare treatmentstatus char(1);
    if new.treatmentresult ='C' then
        BEGIN 
            call create_invoice(old.pid,old.reg_date,old.treatmentid);
        END;
    END IF;
END