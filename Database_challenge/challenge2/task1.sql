-- MySQL root 계정으로 로그인
mysql -u root -p

-- mysql 데이터베이스 사용
USE mysql;

-- 새로운 사용자 생성
CREATE USER 'fishbread_user'@'localhost' IDENTIFIED BY 'password123';

-- 사용자에게 모든 데이터베이스에 대한 모든 권한 부여
GRANT ALL PRIVILEGES ON *.* TO 'fishbread_user'@'localhost';

-- 권한 적용
FLUSH PRIVILEGES;

-- 부여된 권한 확인
SHOW GRANTS FOR 'fishbread_user'@'localhost';
