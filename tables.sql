create database hostelm;
use hostelm;

CREATE TABLE IF NOT EXISTS signup (
    email_id VARCHAR(255) NOT NULL,
    reg_no VARCHAR(255) PRIMARY KEY,
    password VARCHAR(255) NOT NULL
);


INSERT INTO signup (email_id, reg_no, password) VALUES
('006itech@gmail.com', '715522244006', 'kitkat106'),
('007itech@gmail.com', '715522244007', 'kitkat107'),
('008itech@gmail.com', '715522244008', 'kitkat108'),
('009itech@gmail.com', '715522244009', 'kitkat109'),
('010itech@gmail.com', '715522244010', 'kitkat110'),
('011itech@gmail.com', '715522244011', 'kitkat111'),
('012itech@gmail.com', '715522244012', 'kitkat112'),
('013itech@gmail.com', '715522244013', 'kitkat113'),
('014itech@gmail.com', '715522244014', 'kitkat114'),
('015itech@gmail.com', '715522244015', 'kitkat115');


select * from signup;

drop table login;




-- 1. student table
CREATE TABLE student (
    reg_no VARCHAR(255) PRIMARY KEY,
    name VARCHAR(100),
    dept VARCHAR(50),
    year INT,
    phone_no VARCHAR(15),
    hometown VARCHAR(100),
    gender VARCHAR(12),
    FOREIGN KEY (reg_no) REFERENCES signup(reg_no)
);


-- 2. mess (token) table
CREATE TABLE mess (
    reg_no varchar(255) ,
    name VARCHAR(100),
    date DATE,
    token_name VARCHAR(100),
    price DECIMAL(10, 2),
    PRIMARY KEY (reg_no, date, token_name),
    FOREIGN KEY (reg_no) REFERENCES signup(reg_no)
);

-- 3. outing table
CREATE TABLE outing (
    reg_no varchar(255) ,
    name VARCHAR(100),
    out_time TIME,
    date DATE,
    in_time TIME,
    PRIMARY KEY (reg_no, date, out_time),
   FOREIGN KEY (reg_no) REFERENCES signup(reg_no)
);

-- 4. boys table
CREATE TABLE boys (
    reg_no varchar(255) ,
    name VARCHAR(100),
    room_no INT,
    block_no INT,
    roommates_id INT,
    FOREIGN KEY (reg_no) REFERENCES signup(reg_no)
);

alter table boys
modify room_no varchar(10),
modify block_no varchar(10),
modify roommates_id varchar(255);

-- 5. girls table
CREATE TABLE girls (
     reg_no varchar(255) ,
    name VARCHAR(100),
    room_no INT,
    roommates_id INT,
    FOREIGN KEY (reg_no) REFERENCES signup(reg_no)
);

alter table girls
modify roommates_id varchar(255);

-- 6. complaints table
CREATE TABLE complaints (
     reg_no varchar(255) ,
    name VARCHAR(100),
    room_no INT,
    category VARCHAR(50),
    complaint TEXT,
    PRIMARY KEY (reg_no, room_no, category),
    FOREIGN KEY (reg_no) REFERENCES signup(reg_no)
);



drop table house_keeping;

-- 8. home (in and out times) table
CREATE TABLE home (
     reg_no varchar(255) ,
    name VARCHAR(100),
    out_time TIME,
    out_date DATE,
    in_time TIME,
    in_date DATE,
    PRIMARY KEY (reg_no, out_date, out_time),
    FOREIGN KEY (reg_no) REFERENCES signup(reg_no)
);

-- 9. parent details table
CREATE TABLE parent_details (
     reg_no varchar(255) ,
    name VARCHAR(100),
    father_name VARCHAR(100),
    mother_name VARCHAR(100),
    father_occupation VARCHAR(100),
    father_no VARCHAR(15),
    mother_no VARCHAR(15),
    FOREIGN KEY (reg_no) REFERENCES signup(reg_no)
);





-- 1. student table
INSERT INTO student (reg_no, name, dept, year, phone_no, hometown, gender) VALUES
(715522244006, 'Arun Ganesh B', 'CSBS', 2, '9629830361', 'Erode', 'Male'),
(715522244007, 'Karthik N', 'ECE', 1, '9845123456', 'Chennai', 'Male'),
(715522244008, 'Vijay K', 'MECH', 3, '9712345678', 'Coimbatore', 'Male'),
(715522244009, 'Priya M', 'EEE', 2, '9845671234', 'Salem', 'Female'),
(715522244010, 'Anu L', 'CIVIL', 1, '9823456712', 'Madurai', 'Female'),
(715522244011, 'Rohit P', 'IT', 4, '9845678912', 'Tiruppur', 'Male'),
(715522244012, 'Suresh R', 'CSBS', 2, '9845123789', 'Erode', 'Male'),
(715522244013, 'Harshika Shri B', 'CSBS', 2, '9845000011', 'Erode', 'Female'),
(715522244014, 'Manisha S', 'ECE', 1, '9845000022', 'Chennai', 'Female'),
(715522244015, 'Sneha K', 'MECH', 3, '9845000033', 'Coimbatore', 'Female');

-- 2. mess table
INSERT INTO mess (reg_no, name, date, token_name, price) VALUES
(715522244006, 'Arun Ganesh B', '2024-02-23', 'Chicken Token', 20),
(715522244007, 'Karthik N', '2024-02-23', 'Egg Token', 10),
(715522244008, 'Vijay K', '2024-02-23', 'Mutton Token', 50),
(715522244009, 'Priya M', '2024-02-23', 'Mushroom Token', 30),
(715522244010, 'Anu L', '2024-02-23', 'Chicken Token', 20),
(715522244011, 'Rohit P', '2024-02-23', 'Egg Token', 10),
(715522244012, 'Suresh R', '2024-02-23', 'Mutton Token', 50),
(715522244013, 'Harshika Shri B', '2024-02-23', 'Mushroom Token', 30),
(715522244014, 'Manisha S', '2024-02-23', 'Chicken Token', 20),
(715522244015, 'Sneha K', '2024-02-23', 'Egg Token', 10);

-- 3. outing table
INSERT INTO outing (reg_no, name, out_time, date, in_time) VALUES
(715522244006, 'Arun Ganesh B', '09:00:00', '2024-05-19', '17:00:00'),
(715522244007, 'Karthik N', '10:00:00', '2024-05-19', '18:00:00'),
(715522244008, 'Vijay K', '08:00:00', '2024-05-19', '16:00:00'),
(715522244009, 'Priya M', '11:00:00', '2024-05-19', '19:00:00'),
(715522244010, 'Anu L', '07:00:00', '2024-05-19', '15:00:00'),
(715522244011, 'Rohit P', '12:00:00', '2024-05-19', '20:00:00'),
(715522244012, 'Suresh R', '13:00:00', '2024-05-19', '21:00:00'),
(715522244013, 'Harshika Shri B', '09:00:00', '2024-05-19', '17:00:00'),
(715522244014, 'Manisha S', '10:00:00', '2024-05-19', '18:00:00'),
(715522244015, 'Sneha K', '08:00:00', '2024-05-19', '16:00:00');

-- 4. boys table
INSERT INTO boys (reg_no, name, room_no, block_no, roommates_id) VALUES
(715522244006, 'Arun Ganesh B', 'A-301', 'A', 715522244007),
(715522244007, 'Karthik N', 'B-201', 'B', 715522244006),
(715522244008, 'Vijay K', 'A-401', 'A', 715522244011),
(715522244011, 'Rohit P', 'A-501', 'A', 715522244008),
(715522244012, 'Suresh R', 'A-301', 'A', 715522244006);

-- 5. girls table
INSERT INTO girls (reg_no, name, room_no, roommates_id) VALUES
(715522244009, 'Priya M', '301', 715522244013),
(715522244010, 'Anu L', '201', 715522244014),
(715522244013, 'Harshika Shri B', '301', 715522244009),
(715522244014, 'Manisha S', '201', 715522244010),
(715522244015, 'Sneha K', '501', 715522244013);

-- 6. complaints table
INSERT INTO complaints (reg_no, name, room_no, category, complaint) VALUES
(715522244009, 'Priya M', 301, 'Food', 'Mess rep is not responsible'),
(715522244010, 'Anu L', 201, 'Civil', 'Room needs repair'),
(715522244013, 'Harshika Shri B', 301, 'Housekeeping', 'Room not cleaned'),
(715522244014, 'Manisha S', 201, 'Electric', 'Fan not working'),
(715522244015, 'Sneha K', 501, 'Other', 'WiFi not working');



-- 8. home table
INSERT INTO home (reg_no, name, out_time, out_date, in_time, in_date) VALUES
(715522244009, 'Priya M', '18:30:00', '2024-05-18', '10:00:00', '2024-05-21'),
(715522244010, 'Anu L', '17:00:00', '2024-05-19', '09:00:00', '2024-05-22'),
(715522244013, 'Harshika Shri B', '16:30:00', '2024-05-20', '08:00:00', '2024-05-23'),
(715522244014, 'Manisha S', '15:30:00', '2024-05-21', '07:00:00', '2024-05-24'),
(715522244015, 'Sneha K', '14:30:00', '2024-05-22', '06:00:00', '2024-05-25');

-- 9. parent details table
INSERT INTO parent_details (reg_no, name, father_name, mother_name, father_occupation, father_no, mother_no) VALUES
(715522244009, 'Priya M', 'Mohan M', 'Lakshmi M', 'Business', '9876543211', '9865432121'),
(715522244010, 'Anu L', 'Lakshman L', 'Rani L', 'Teacher', '9876543212', '9865432122'),
(715522244013, 'Harshika Shri B', 'Balu B', 'Sita B', 'Engineer', '9876543213', '9865432123'),
(715522244014, 'Manisha S', 'Shankar S', 'Meena S', 'Doctor', '9876543214', '9865432124'),
(715522244015, 'Sneha K', 'Kumar K', 'Rekha K', 'Business', '9876543215', '9865432125');


alter table parent_details
drop mother_no;

select * from mess;

select * from parent_details;





CREATE TABLE admin (
    admin_id varchar(30) PRIMARY KEY,
    email_id VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);



-- Insert values into admins table
INSERT INTO admin (admin_id, email_id, password) VALUES
('7155ad001', 'admin001@gmail.com', 'hostel@001'),
('7155ad002', 'admin002@gmail.com', 'hostel@002'),
('7155ad003', 'admin003@gmail.com', 'hostel@003'),
('7155ad004', 'admin004@gmail.com', 'hostel@004'),
('7155ad005', 'admin005@gmail.com', 'hostel@005');

select * from admin;

