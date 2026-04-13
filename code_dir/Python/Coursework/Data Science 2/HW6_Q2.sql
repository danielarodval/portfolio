-- PROBLEM 2
CREATE OR REPLACE FUNCTION public.f_GetAvgDeptSalary(_department_name
VARCHAR(200))
RETURNS DECIMAL(10,2)
AS $BODY$
DECLARE
total_salary DECIMAL(10,2);
num_employees INTEGER;
BEGIN
SELECT COALESCE(AVG(salary), 0.00), COUNT(*) INTO total_salary, num_employees
FROM public.employees e
INNER JOIN public.departments d ON e.department_id = d.department_id
WHERE d.department_name = _department_name;

IF num_employees = 0 THEN
RETURN 0.00;
ELSE
RETURN total_salary;
END IF;

RETURN -1.00;
END;
$BODY$ LANGUAGE plpgsql
PARALLEL SAFE;

SELECT public.f_GetAvgDeptSalary('IT')