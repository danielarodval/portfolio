create TABLE employees (
    employeeID char(10), 
    salary REAL, 
    gender char(10),
    email VARCHAR(50),
    [name] VARCHAR(100),
    [address] VARCHAR(200),
    startdate date,
    phone VARCHAR(12),
    PRIMARY KEY (employeeID)    
	);

CREATE TABLE children(
    [name] VARCHAR(100),  
    dob DATE,
    age INT, 
    gender CHAR(10),
    PRIMARY key ([name])
    ); 

    Create table [dependent](
            employeeID char(10) not NULL,
            name VARCHAR(100) not null,
            PRIMARY key (employeeID, [name]),
            FOREIGN KEY (employeeID) REFERENCES employees on DELETE cascade,
            FOREIGN key (name) REFERENCES children on DELETE cascade
    );

    create TABLE departments(
        dno char(10), 
        dname VARCHAR(100),
        numberofemployees real, 
        budget real,
        PRIMARY key (dno)
    );

    create table managers (
        dno char(10) not null,
        employeeID char (10) not null,
        since date, 
        PRIMARY key (dno, employeeID),
        FOREIGN key (dno) REFERENCES departments on DELETE  NO ACTION, 
        foreign key (employeeID) REFERENCES employees on DELETE NO ACTION
    );

CREATE TABLE worksIn(
    employeeID char(10) not null,
    dno char(10) not null,
    PRIMARY key (employeeID, dno),
    FOREIGN key (employeeID) REFERENCES employees on DELETE CASCADE,
    FOREIGN key (dno) REFERENCES departments on delete cascade
)

--------
create view mothersDayFloralOrders 
as 
select emp.employeeID, emp.[name] as employee_name, emp.email, emp.address, emp.gender, departments.dname, man.[name] as manager_name, children.name, children.age 
from employees emp inner join worksIn on emp.employeeID = worksIn.employeeID
    inner join departments on departments.dno = worksIn.dno
    left join manages man1 on departments.dno = man1.dno
    left join employees man on man.employeeID = man1.employeeID
    inner join dependent on emp.employeeID = dependent.employeeID
    inner join children on dependent.[name] = children.[name]
where emp.gender = 'Female'
AND since = (
				SELECT MAX(since) 
				FROM dbo.manages man2
				WHERE man2.dno = man1.dno
				GROUP BY dno
				);

SELECT * FROM mothersDayFloralOrders