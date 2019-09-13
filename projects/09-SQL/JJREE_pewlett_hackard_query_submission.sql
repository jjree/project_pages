-- 0. initial queries to observe tables and their columns; also utilized for reference
select * from departments;
select * from dept_emp;
select * from dept_manager;
select * from employees;
select * from salaries;
select * from titles;

-- 1. List the following details of each employee: employee number, last name, first name, gender, and salary.
--------------------------------------------------------------
select 		emp.emp_no, emp.last_name, emp.first_name, emp.gender, sal.salary 
from 		employees emp
inner join 	salaries sal 
on 			emp.emp_no = sal.emp_no
order by 	emp.emp_no;

-- query without join
-- select 		emp.emp_no, emp.last_name, emp.first_name, emp.gender, sal.salary 
-- from 		employees emp, salaries sal
-- where		emp.emp_no=sal.emp_no
-- order by 	emp.emp_no;

-- 2. List employees who were hired in 1986.
---------------------------------------------------------------
select 		* 
from 		employees
where 		extract(year from employees.hire_date) = 1986;

-- 3. List the manager of each department with the following information: 
-- department number, department name, the manager's employee number, last name, 
-- first name, and start and end employment dates.
---------------------------------------------------------------
select 		mgr.dept_no, dept.dept_name, mgr.emp_no, emp.last_name, emp.first_name, mgr.from_date, mgr.to_date
from 		dept_manager mgr
inner join 	departments dept 
on 			mgr.dept_no=dept.dept_no
inner join 	employees emp 
on 			mgr.emp_no = emp.emp_no;

-- 4. List the department of each employee with the following information: employee number, last name, first name, and department name.
---------------------------------------------------------------
select 		emp.emp_no, emp.last_name, emp.first_name, dept.dept_name
from 		employees emp
inner join 	dept_emp de
on 			emp.emp_no=de.emp_no
inner join 	departments dept
on 			de.dept_no=dept.dept_no
order by 	emp.emp_no;

-- 5. List all employees whose first name is "Hercules" and last names begin with "B."
---------------------------------------------------------------
select 		* 
from 		employees 
where 		first_name = 'Hercules' and last_name LIKE 'B%';

-- 6. List all employees in the Sales department, including their employee number, last name, first name, and department name.
---------------------------------------------------------------
select 		emp.emp_no, emp.last_name, emp.first_name, dept.dept_name
from 		employees emp
inner join 	dept_emp de
on 			emp.emp_no=de.emp_no
inner join 	departments dept
on 			de.dept_no=dept.dept_no
where 		dept.dept_name = 'Sales';

-- 7. List all employees in the Sales and Development departments, including their employee number, last name, first name, and department name.
---------------------------------------------------------------
select 		emp.emp_no, emp.last_name, emp.first_name, dept.dept_name
from		employees emp
inner join 	dept_emp de
on 			emp.emp_no=de.emp_no
inner join 	departments dept
on 			de.dept_no=dept.dept_no
where 		dept.dept_name = 'Sales' or dept.dept_name = 'Development'
order by 	emp.emp_no;

-- 8. In descending order, list the frequency count of employee last names, i.e., how many employees share each last name.
---------------------------------------------------------------
select 		emp.last_name, count(emp.last_name)
from 		employees emp
group by 	emp.last_name
order by 	count(emp.last_name) DESC;
