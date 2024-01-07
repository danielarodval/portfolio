-- Recommended Problem 1
-- Step-by-Step Approach

SELECT department_id, AVG(salary)
FROM public.employees
GROUP BY department_id;

WITH dept_avg_salary (department_id, avg_sal) AS (
	SELECT department_id, AVG(salary) AS avg_sal
	FROM public.employees
	GROUP BY department_id
)
SELECT e.employee_id, e.department_id, e.salary, d.avg_sal
FROM public.employees e
INNER JOIN dept_avg_salary d
ON e.department_id = d.department_id
WHERE e.salary <= d.avg_sal * 0.8;

WITH dept_avg_salary (department_id, avg_sal) AS (
	SELECT department_id, AVG(salary) AS avg_sal
	FROM public.employees
	GROUP BY department_id
)
SELECT e.employee_id, e.salary, e.department_id, d.avg_sal
FROM public.employees e
INNER JOIN dept_avg_salary d
ON e.department_id = d.department_id
WHERE e.salary <= d.avg_sal * 0.8;

ALTER TABLE public.employees DISABLE TRIGGER ALL;
-- This is executed to disable the triggers not allowing salaries to go below or above max/min salaries for certain jobs.

WITH dept_avg_salary (department_id, avg_sal) AS (
	SELECT department_id, AVG(salary) AS avg_sal
	FROM public.employees
	GROUP BY department_id
)
UPDATE public.employees
SET salary = e.salary * 1.15
FROM public.employees e
INNER JOIN dept_avg_salary d
ON e.department_id = d.department_id
WHERE e.salary <= d.avg_sal * 0.8;

-- Checking
SELECT * FROM public.employees
WHERE employee_id = 107;

-- Alternative way
SELECT * ---Select all
FROM public.employees e1---Select all from employees table
WHERE e1.salary <= (SELECT AVG(salary) FROM public.employees e2 WHERE department_id =e1.department_id) * 0.8;

UPDATE public.employees---if the employee earns less than 20 percent of the average, UPDATE
SET salary = e1.salary * 1.15---increase the salary by 15%
FROM public.employees e1---select the table to update the salary, below will do it only when the below criteris is satisfied
WHERE e1.salary <= (SELECT AVG(salary) FROM public.employees e2 WHERE department_id =e1.department_id) * 0.8;---compares each employees salary, to the average salary from the employees table(pulled from second FROM) and matches to compare the employee to its own department then multiple by .8 to get 20 percent lower of the average