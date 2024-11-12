use WCMS;
select * from users;
DELIMITER $$

CREATE PROCEDURE count_records(IN table_name VARCHAR(255))
BEGIN
    SET @sql = CONCAT('SELECT COUNT(*) FROM ', table_name);
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END $$

DELIMITER ;

select * from habitat;
select * from species;
ALTER TABLE species
ADD COLUMN habitat_id INT,
ADD CONSTRAINT fk_habitat
FOREIGN KEY (habitat_id) REFERENCES habitat(habitat_id);

CREATE TABLE audit_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    table_name VARCHAR(255),
    operation VARCHAR(50),
    record_id INT,
    old_value TEXT,
    new_value TEXT,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DELIMITER $$

CREATE TRIGGER after_species_insert
AFTER INSERT ON species
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (table_name, operation, record_id, new_value)
    VALUES ('species', 'INSERT', NEW.species_id, NEW.common_name);
END$$

DELIMITER ;


select * from movement;
select * from health_record;
select * from interaction;
select * from species;