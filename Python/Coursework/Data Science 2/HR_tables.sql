CREATE TABLE public.regions(
	region_id SMALLINT NOT NULL,
	region_name VARCHAR(30) NOT NULL,
	PRIMARY KEY (region_id),
	UNIQUE(region_name)
);

CREATE TABLE public.countries(
	country_id CHAR(2) NOT NULL,
	country_name VARCHAR(30) NOT NULL,
	region_id SMALLINT NOT NULL,
	PRIMARY KEY (country_id),
	FOREIGN KEY (region_id) REFERENCES public.regions(region_id)
);

CREATE TABLE public.locations(
	location_id SMALLINT NOT NULL,
	street_address VARCHAR(200) NOT NULL DEFAULT 'N/A',
	postal_code VARCHAR(15) NULL,
	city VARCHAR(50) NOT NULL,
	state_province VARCHAR(30) NULL,
	country_id CHAR(2) NOT NULL,
	PRIMARY KEY (location_id),
	FOREIGN KEY (country_id) REFERENCES public.countries(country_id)
);

CREATE TABLE public.jobs(
	job_id SMALLINT NOT NULL,
	job_title VARCHAR(100) NOT NULL,
	min_salary DECIMAL(10,2) NOT NULL DEFAULT 0.00,
	max_salary DECIMAL(10,2) NOT NULL DEFAULT 0.00,
	PRIMARY KEY (job_id),
	CHECK (min_salary = 0.00 OR max_salary = 0.00 OR min_salary <= max_salary)
);

CREATE TABLE public.departments(
	department_id SMALLINT NOT NULL,
	department_name VARCHAR(200) NOT NULL,
	location_id SMALLINT NOT NULL,
	PRIMARY KEY (department_id),
	FOREIGN KEY (location_id) REFERENCES public.locations(location_id)
);

CREATE TABLE public.employees(
	employee_id SERIAL NOT NULL,
	first_name VARCHAR(50) NOT NULL DEFAULT '',
	last_name VARCHAR(50) NOT NULL DEFAULT '',
	email VARCHAR(255) NOT NULL DEFAULT '',
	phone_number VARCHAR(20) NOT NULL DEFAULT '',
	hire_date DATE NOT NULL,
	job_id SMALLINT NOT NULL,
	salary DECIMAL(10,2),
	manager_id INTEGER NULL,
	department_id SMALLINT NULL,
	PRIMARY KEY (employee_id),
	FOREIGN KEY (manager_id) REFERENCES public.employees(employee_id),
	FOREIGN KEY (department_id) REFERENCES public.departments(department_id),
	CHECK(TRIM(first_name) != '' OR TRIM(last_name) != '')
);

CREATE TABLE public.dependents(
	dependent_id SERIAL NOT NULL,
	first_name VARCHAR(50) NOT NULL DEFAULT '',
	last_name VARCHAR(50) NOT NULL DEFAULT '',
	relationship VARCHAR(15) NOT NULL DEFAULT 'Other Relative',
	employee_id INTEGER NOT NULL,
	PRIMARY KEY (dependent_id),
	FOREIGN KEY (employee_id) REFERENCES public.employees(employee_id),
	CHECK(TRIM(first_name) != '' OR TRIM(last_name) != ''),
	CHECK(relationship IN ('Child', 'Sibling', 'Parent', 'Other Relative'))
);
