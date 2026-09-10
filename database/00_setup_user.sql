-- 00_setup_user.sql
-- Run this script in Oracle SQL Developer as SYS or SYSTEM to create the application user.

-- Optional: if you are using Oracle 12c+ with pluggable databases and want to create a common user, 
-- you may need to uncomment the following line depending on your setup.
-- ALTER SESSION SET "_ORACLE_SCRIPT"=true;

-- 1. Create the user
CREATE USER campushub IDENTIFIED BY campushub123;

-- 2. Grant connection and resource privileges
GRANT CONNECT, RESOURCE TO campushub;
GRANT CREATE SESSION TO campushub;
GRANT CREATE TABLE TO campushub;
GRANT CREATE VIEW TO campushub;
GRANT CREATE SEQUENCE TO campushub;

-- 3. Assign quota so the user can actually insert data
ALTER USER campushub QUOTA UNLIMITED ON USERS;

-- 4. Verify user was created
SELECT username, account_status FROM dba_users WHERE username = 'CAMPUSHUB';
