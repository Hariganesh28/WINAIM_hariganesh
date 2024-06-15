--  Create departments table
CREATE TABLE departments (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL
);
--  Create employees table
CREATE TABLE employees (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    department_id INT,
    hire_date DATE,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);
--  Create salaries table
CREATE TABLE salaries (
    salary_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    salary DECIMAL(10, 2) NOT NULL,
    from_date DATE NOT NULL,
    to_date DATE NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);
-- Insert department records
INSERT INTO departments (department_name)
VALUES
    ('HR'),
    ('IT'),
    ('Finance');
-- Insert employee records
INSERT INTO employees (first_name, last_name, department_id, hire_date)
VALUES
    ('Magesh', 'Raj', 1, '2023-07-01'),
    ('Priya', 'Patel', 2, '2022-11-30'),
    ('Rahul', 'Sharma', 1, '2023-03-20'),
    ('Pooja', 'Srinivas', 3, '2021-08-10'),
    ('Amit', 'Verma', 2, '2022-05-05');


-- Insert salary records
INSERT INTO salaries (employee_id, salary, from_date, to_date)
VALUES
    (1, 25000.00, '2023-07-01', '2023-12-31'),
    (2, 70000.00, '2022-11-30', '2023-12-31'),
    (3, 80000.00, '2023-03-20', '2023-12-31'),
    (4, 55000.00, '2021-08-10', '2022-08-09'),
    (5, 75000.00, '2022-05-05', '2023-05-04'),
    (1, 62000.00, '2024-01-01', '2024-12-31'),
    (3, 82000.00, '2024-01-01', '2024-12-31');

-- Select employees hired within the last year
SELECT *
FROM employees
WHERE hire_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR);

-- Select department names and total salary expenditure per department
SELECT d.department_name, SUM(s.salary) AS total_salary_expenditure
FROM departments d
JOIN employees e ON d.department_id = e.department_id
JOIN salaries s ON e.employee_id = s.employee_id
GROUP BY d.department_name;

-- Select top 5 employees with highest salaries with department names
SELECT e.first_name, e.last_name, d.department_name, s.salary
FROM employees e
JOIN departments d ON e.department_id = d.department_id
JOIN salaries s ON e.employee_id = s.employee_id
ORDER BY s.salary DESC
LIMIT 5;




