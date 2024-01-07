import pandas as pd

def fill_dept_stats(file_name):
    df = pd.read_csv(file_name,header=None,names=['name','department','salary'])
    
    global Depts 
    Depts = pd.concat([(df['department'].value_counts() * 3).rename('employeeCount'), (df.groupby('department')['salary'].sum() * 3).rename('totalSalary'), (df.groupby('department')['salary'].mean() * 3).rename('avgSalary')],axis=1)
    Depts.reset_index(inplace=True)
def get_dept_stats(dept_name):
    try:
        Depts['index'].isin([dept_name])
    except:
        print('Department not found')
        return 0,0,0
    else:
        return int(Depts.loc[Depts['index'].isin([dept_name])].employeeCount),float(Depts.loc[Depts['index'].isin([dept_name])].totalSalary),float(Depts.loc[Depts['index'].isin([dept_name])].avgSalary)


fill_dept_stats('C:/Users/danma/Downloads/ISC 4242/Emp_salary.csv')

dept = 'R&D'
emp_no, total_sal, avg_sal = get_dept_stats(dept)
print('Department: ' + dept + ', Employees No.: '+ str(emp_no) + ', Total Salary: '+ str(round(total_sal,2)) + ', Average Salary: '+ str(round(avg_sal,2)) + '\n')

dept = 'Accounting'
emp_no, total_sal, avg_sal = get_dept_stats(dept)
print('Department: ' + dept + ', Employees No.: '+ str(emp_no) + ', Total Salary: '+ str(round(total_sal,2)) + ', Average Salary: '+ str(round(avg_sal,2)) + '\n')

dept = 'Implementation'
emp_no, total_sal, avg_sal = get_dept_stats(dept)
print('Department: ' + dept + ', Employees No.: '+ str(emp_no) + ', Total Salary: '+ str(round(total_sal,2)) + ', Average Salary: '+ str(round(avg_sal,2)) + '\n')

dept = 'Support'
emp_no, total_sal, avg_sal = get_dept_stats(dept)
print('Department: ' + dept + ', Employees No.: '+ str(emp_no) + ', Total Salary: '+ str(round(total_sal,2)) + ', Average Salary: '+ str(round(avg_sal,2)) + '\n')