-- Recommended Problem 5

CREATE OR REPLACE FUNCTION public.f_GetEmployeeStatus(_employee_id INTEGER)
RETURNS CHARACTER VARYING
AS $BODY$
DECLARE _dept_id SMALLINT := NULL;
	_salary DECIMAL(10,2) := NULL;
	_last_name VARCHAR(50) := NULL;
	_job_id SMALLINT := NULL;
	_max_salary_allowed DECIMAL(10,2) := NULL;
	_min_salary_allowed DECIMAL(10,2) := NULL;
	_department_head_id INTEGER := NULL;
	_department_head_last_name VARCHAR(50) := NULL;
	_dependents_no BIGINT := NULL;
	_deviations CHARACTER VARYING := '';
	_problems_detected BOOLEAN := FALSE;
BEGIN
 -- Checking validity of the _employee_id supplied
 IF NOT EXISTS (SELECT employee_id FROM public.employees WHERE employee_id = _employee_id)
 THEN
	RETURN format('Problem(s) Detected: The employee''s record for employee_id = %s does not exist', _employee_id);
 END IF;
 
 -- Checking Depatment ID
 SELECT department_id, salary, job_id, last_name
 INTO _dept_id, _salary, _job_id, _last_name
 FROM public.employees
 WHERE employee_id = _employee_id;
 IF _dept_id IS NULL
 THEN
	_deviations := 'Problem(s) Detected: The Employee is not assigned to any department';
	_problems_detected := TRUE;
 END IF;
 
 -- Checking Salary
 IF _salary IS NOT NULL
 THEN
	SELECT min_salary, max_salary
	INTO _min_salary_allowed, _max_salary_allowed
	FROM public.jobs
	WHERE job_id = _job_id;
	IF _min_salary_allowed IS NOT NULL	-- employees.job_id is NOT a foreign key. Thus, potentially, an employee might be assigned a non-existent job
	THEN
		IF _salary > _max_salary_allowed
		THEN
			IF _problems_detected = TRUE
			THEN
				_deviations := _deviations || '; ';
			ELSE
				_deviations := 'Problem(s) detected: ';
				_problems_detected := TRUE;
			END IF;
			_deviations := _deviations || 'Salary exceeds the maximum allowed salary';
		END IF;	-- _salary > _max_salary_allowed
		IF _salary < _min_salary_allowed
		THEN
			IF _problems_detected = TRUE
			THEN
				_deviations := _deviations || '; ';
			ELSE
				_deviations := 'Problem(s) detected: ';
				_problems_detected := TRUE;
			END IF;
			_deviations := _deviations || 'Salary is below the minimum allowed salary';
		END IF;	-- _salary < _min_salary_allowed
	END IF;
 END IF;
 
 -- Checking Department Head
 SELECT department_head
 INTO _department_head_id
 FROM public.departments
 WHERE department_id = _dept_id;
 IF _department_head_id IS NULL
 THEN
	NULL;	-- Nothing to check: the department head for the employee's department is not assigned
 ELSIF _department_head_id = _employee_id	-- The employee is a department head of his/her department
 THEN
	IF EXISTS (SELECT employee_id FROM public.employees WHERE department_id = _dept_id AND employee_id != _employee_id AND last_name = _last_name)
	THEN
		IF _problems_detected = TRUE
		THEN
			_deviations := _deviations || '; ';
		ELSE
			_deviations := 'Problem(s) detected: ';
			_problems_detected := TRUE;
		END IF;
		_deviations := _deviations || 'The employee is a department head, and there are other employees in his/her department with the same last name';
	END IF;
 ELSE	-- The employee is not a department head
	SELECT last_name
	INTO _department_head_last_name
	FROM public.employees
	WHERE employee_id = _department_head_id;
	IF _department_head_last_name = _last_name
	THEN
		IF _problems_detected = TRUE
		THEN
			_deviations := _deviations || '; ';
		ELSE
			_deviations := 'Problem(s) detected: ';
			_problems_detected := TRUE;
		END IF;
		_deviations := _deviations || 'The employee is not a department head, but his/her last name is the same as the last name of the department head of his/her department';
	END IF;
 END IF;
 
 -- Checking Dependents
 SELECT COUNT(dependent_id)
 INTO _dependents_no
 FROM public.dependents
 WHERE employee_id = _employee_id;
 IF _dependents_no > 2
 THEN
	IF _problems_detected = TRUE
	THEN
		_deviations := _deviations || '; ';
	ELSE
		_deviations := 'Problem(s) detected: ';
		_problems_detected := TRUE;
	END IF;
	_deviations := _deviations || 'The employee has more than two dependents';
 END IF;
 
 -- Returning the Summary
 IF _problems_detected = TRUE
 THEN
	RETURN (_deviations || '.');
 ELSE
	RETURN 'Everything looks fine.';
 END IF;
END;
$BODY$ LANGUAGE plpgsql
PARALLEL SAFE;

-- Testing the function
/*
SELECT public.f_GetEmployeeStatus(107);

SELECT public.f_GetEmployeeStatus(100);

SELECT public.f_GetEmployeeStatus(1070);
*/