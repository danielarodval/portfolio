-- Recommended Problem 3

/*
ALTER TABLE departments
ADD COLUMN department_head INTEGER NULL;

ALTER TABLE departments
ADD FOREIGN KEY (department_head) REFERENCES employees(employee_id);
*/

SELECT d.department_id, d. department_name, COALESCE(e.first_name || ' ' || e.last_name, '-- NOT ASSIGNED--') AS dept_head,---COALESCE is essentially a concat/concatenation function
	(SELECT COUNT(employee_id) FROM public.employees WHERE department_id = d.department_id) AS employees_no,---pulls the count of employees
	loc.street_address || ', ' || loc.city || ', ' || c.country_name  AS dept_addres---creates an address from the different records
FROM public.departments d---
LEFT OUTER JOIN public.employees e---Left outer join is used to retain all records for departments and matched records from employees  
ON d.department_head = e.employee_id---
INNER JOIN locations loc---returns all records that have matching values in both tables, matching the departments with their respective locations
ON d.location_id = loc.location_id ---ID matching
INNER JOIN public.countries c---returns all records that have matching values in both tables, matching the locations with their respective countries
ON loc.country_id = c.country_id;--ID matching