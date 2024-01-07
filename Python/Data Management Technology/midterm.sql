/** Object:  View [dbo].[mothersDayFloralOrders]    Script Date: 2/17/2023 5:23:50 PM **/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE view [dbo].[mothersDayFloralOrders] 
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
                --GROUP BY dno
                );
GO

CREATE TABLE Shelves(
    ShelfID INT,
    ShelfLength REAL,
    ShelfHeight REAL,
	PRIMARY KEY (ShelfID)
);

CREATE TABLE [Objects](
    ObjectID INT,
    ObjectName  VARCHAR(100),
    ShelfID INT NOT NULL,
    PRIMARY KEY (ObjectID),
    FOREIGN KEY (ShelfID) REFERENCES Shelves
);

SELECT [ProductID], SUM([LineTotal]) AS Total_Revenue
FROM SalesOrder sales
GROUP BY sales.[ProductID]
ORDER BY Total_Revenue DESC

SELECT [ProductID], SUM([OrderQty]) AS Total_Quantity
FROM SalesOrder sales
GROUP BY sales.[ProductID]
ORDER BY Total_Quantity DESC