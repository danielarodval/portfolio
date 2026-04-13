CREATE TABLE employees(
	employeeID char(10) not NULL,
	salary REAL,
	gender char(10),
	email VARCHAR(50),
	[name] VARCHAR(100),
	[address] VARCHAR(200),
	startdate date,
	phone VARCHAR(12),
	PRIMARY KEY (employeeID)
);

CREATE TABLE departments(
	dno char(10) not NULL,
	dname VARCHAR(50),
	NumberOfEmployees REAL,
	budget REAL,
	PRIMARY KEY (dno)
);

CREATE TABLE child(
    [name] VARCHAR(100) not NULL,
	employeeID char(10) not NULL, 
	dob date,
	age REAL,
	gender char(10),
	PRIMARY KEY ([name]),
    FOREIGN KEY (employeeID) REFERENCES employees ON DELETE CASCADE
);


CREATE TABLE depend(
	employeeID char(10) NOT NULL,
	[name] VARCHAR(100) NOT NULL,
	PRIMARY KEY (employeeID, [name]),
    FOREIGN KEY (employeeID) REFERENCES employees ON DELETE CASCADE,
    FOREIGN KEY ([name]) REFERENCES child ON DELETE CASCADE
);

CREATE TABLE manages(
	since date,
	employeeID char(10) not NULL,
	dno char(10) not NULL,
	PRIMARY KEY (employeeID, dno),
	FOREIGN KEY (employeeID) REFERENCES employees,
    FOREIGN KEY (dno) REFERENCES departments
);

CREATE TABLE works_in(
	employeeID char(10) not NULL,
	dno char(10) not NULL,
	PRIMARY KEY (employeeID, dno),
	FOREIGN KEY (employeeID) REFERENCES employees,
    FOREIGN KEY (dno) REFERENCES departments
);

INSERT INTO employees (employeeID, salary, gender, email, [name], [address], startdate, phone) VALUES ('1',10000,'Male','test@test.com','John Smith','123 Fruit Drive','01-01-1999','555-123-4567')
INSERT INTO departments (dno, dname, NumberOfEmployees, budget) VALUES ('12','Marketing',52,50000)
INSERT INTO child ([name], employeeID, dob, age, gender) VALUES ('Jane','1','01-01-1999',12,'Female')
INSERT INTO depend (employeeID, [name]) VALUES ('1','Jane')
INSERT INTO manages (since, employeeID, dno) VALUES ('01-01-2005','1','12')
INSERT INTO works_in (employeeID, dno) VALUES ('01-01-1999','12')


CREATE VIEW mothers_day_flower_orders AS
	SELECT emp.employeeID, emp.[name], emp.email, emp.gender, dep.dname, dep.employeeID, cld.[name], cld.age
	FROM employees emp
-- Microsoft SQL Server Management Studio