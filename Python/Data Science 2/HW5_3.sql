SELECT con.country_name, COUNT(emp.employee_id) AS employees_no, SUM(emp.salary) AS total_salary
FROM departments dep 
INNER JOIN employees emp ON dep.department_id = emp.department_id
INNER JOIN locations loc ON dep.location_id = loc.location_id
INNER JOIN countries con ON loc.country_id = con.country_id
GROUP BY con.country_name

HAVING SUM(emp.salary) != 0
ORDER BY con.country_name;

SELECT depart.department_name, COUNT(depend.dependent_id) AS dependents_no
FROM departments depart 
INNER JOIN employees emp ON depart.department_id = emp.department_id
LEFT JOIN dependents depend ON depend.employee_id = emp.employee_id
GROUP BY depart.department_name
ORDER BY dependents_no DESC, department_name