SELECT dep.department_name, emp.employee_id, emp.last_name, emp.first_name, emp.salary, loc.city, loc.state_province, con.country_name
FROM departments dep 
INNER JOIN employees emp ON dep.department_id = emp.department_id
INNER JOIN locations loc ON dep.location_id = loc.location_id
INNER JOIN countries con ON loc.country_id = con.country_id
ORDER BY dep.department_name, emp.last_name, emp.first_name