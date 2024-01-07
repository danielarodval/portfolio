-- PROBLEM 1
--ALTER TABLE public.departments
--ADD department_head INTEGER NULL;

--ALTER TABLE public.departments
--ADD FOREIGN KEY (department_head)
--REFERENCES public.employees(employee_id);

--PART A
CREATE OR REPLACE FUNCTION assign_department_head() 
RETURNS TRIGGER AS $$
BEGIN
IF NEW.department_head IS NULL THEN
RAISE INFO 'OK: Department set automatically';
RETURN NEW;
ELSE

-- Check if the department_head belongs to another department
DECLARE
head_count INTEGER;
BEGIN
SELECT COUNT(*) INTO head_count FROM public.employees
WHERE employee_id = NEW.department_head AND department_id != NEW.department_id;
IF head_count > 0 THEN
RAISE INFO 'ROLLBACK: Employee belongs to Department %', @department_id;
ROLLBACK;
RETURN NULL;
END IF;
END;

-- Update the department_id of the head if it's not set already
UPDATE public.employees SET department_id = NEW.department_id
WHERE employee_id = NEW.department_head AND department_id IS NULL;

-- If not null from above return new
END IF;
RAISE INFO 'OK';
RETURN NEW;
END;
$$ LANGUAGE plpgsql PARALLEL SAFE;

CREATE OR REPLACE TRIGGER department_head_trigger
BEFORE INSERT OR UPDATE ON public.departments
FOR EACH ROW
EXECUTE FUNCTION assign_department_head();

-- PART B

CREATE OR REPLACE FUNCTION prevent_employee_update()
RETURNS TRIGGER AS $$
DECLARE
head_count INTEGER;
BEGIN
-- Prevent changing employee_id
IF OLD.employee_id != NEW.employee_id THEN
RAISE INFO 'ROLLBACK: Cannot change employee_id';
ROLLBACK;
RETURN NULL;
END IF;
    
-- Prevent changing department_id for Department Heads
SELECT COUNT(*) INTO head_count FROM public.employees
WHERE OLD.employee_id IN (SELECT department_head FROM public.departments WHERE department_id = NEW.department_id);
IF head_count > 0 AND OLD.department_id != NEW.department_id THEN
RAISE INFO 'ROLLBACK: Cannot change department_id for Department Head';
ROLLBACK;
RETURN NULL;
END IF;
RAISE INFO 'OK';
RETURN NEW;
END;
$$ LANGUAGE plpgsql PARALLEL SAFE;

CREATE OR REPLACE TRIGGER employee_update_trigger
BEFORE UPDATE ON public.employees
FOR EACH ROW
EXECUTE FUNCTION prevent_employee_update();

--TEST CASES PART A
UPDATE public.departments
SET department_head = 178
WHERE department_id = 8;
-- OK

UPDATE public.departments
SET department_head = 101
WHERE department_id = 8;
-- ROLLBACK: Employee belongs to Department 9

UPDATE public.employees
SET department_id = NULL
WHERE employee_id = 101;

UPDATE public.departments
SET department_head = 101
WHERE department_id = 8;
-- OK: Department set automatically

-- TEST CASES PART B
UPDATE public.employees
SET department_id = 9
WHERE employee_id = 177;
-- OK
UPDATE public.employees
SET department_id = 9
WHERE employee_id = 101;
-- ROLLBACK: Changing department for a Department Head
UPDATE public.employees
SET department_id = NULL
WHERE employee_id = 101;
-- ROLLBACK: Setting department to NULL for a Department Head
