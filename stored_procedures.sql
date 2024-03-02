-- Stored procedure for user login
DELIMITER $$
CREATE PROCEDURE `Login`(
    IN p_email VARCHAR(150)
)
BEGIN
    SELECT *
    FROM users 
    WHERE email = p_email;
END$$
DELIMITER ;

-- Stored procedure for user registration
DELIMITER $$
CREATE PROCEDURE `Register`(
    IN p_id VARCHAR(36),
    IN p_full_name VARCHAR(150),
    IN p_email VARCHAR(150),
    IN p_password VARCHAR(255)
)
BEGIN
    DECLARE user_count INT;

    SELECT COUNT(*) INTO user_count FROM users WHERE email = p_email;

    IF user_count = 0 THEN
        INSERT INTO users (id, full_name, email, password, user_type, created_at)
        VALUES (p_id, p_full_name, p_email, p_password, 'customer', NOW());
        SELECT 'success';
    ELSE
        SELECT 'already_exists';
    END IF;
END$$
DELIMITER ;

-- Stored procedure for updating user information
DELIMITER $$
CREATE PROCEDURE `Update_user`(
    IN p_id VARCHAR(36),
    IN p_full_name VARCHAR(150),
    IN p_email VARCHAR(150),
    IN p_password VARCHAR(255)
)
BEGIN
    DECLARE v_count INT;

    SELECT COUNT(*) INTO v_count FROM users WHERE id = p_id;

    IF v_count != 0 THEN
        UPDATE users SET full_name = p_full_name, email = p_email, password = p_password WHERE id = p_id;
        SELECT 'success';
    ELSE
        SELECT 'not_exist';
    END IF;
END$$
DELIMITER ;

-- Stored procedure to retrieve user information by ID
DELIMITER $$
CREATE PROCEDURE `User_by_id`(IN p_id VARCHAR(36))
BEGIN
	SELECT id, full_name, email, user_type, created_at
    FROM users
    WHERE id = p_id;
END$$
DELIMITER ;

-- Stored procedure to retrieve a list of customer users
DELIMITER $$
CREATE PROCEDURE `User_list`()
BEGIN
	SELECT id, full_name, email, user_type, created_at
    FROM users
    WHERE user_type = 'customer';
END$$
DELIMITER ;
