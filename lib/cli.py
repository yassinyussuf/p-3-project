import sqlite3

def create_tables():
    connection = sqlite3.connect("company.db")
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS departments(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS managers (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   first_name TEXT NOT NULL,
                   last_name TEXT NOT NULL,
                   email TEXT NOT NULL,
                   mobile_number TEXT NOT NULL,
                   department_id INTEGER,
                   FOREIGN KEY (department_id) REFERENCES departments(id)
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   first_name TEXT NOT NULL,
                   last_name TEXT NOT NULL,
                   email TEXT NOT NULL,
                   mobile_number TEXT NOT NULL,
                   hire_date TEXT NOT NULL,
                   salary TEXT NOT NULL,
                   department_id INTEGER,
                   manager_id INTEGER,
                   FOREIGN KEY (department_id) REFERENCES departments(id),
                   FOREIGN KEY (manager_id) REFERENCES managers(id)
    )''')

    connection.commit()
    connection.close()

create_tables()

class CompanyDB:
    def __init__(self):
        self.connection = sqlite3.connect('company.db')
        self.cursor = self.connection.cursor()

    def add_department(self, name):
        self.cursor.execute('INSERT INTO departments (name) VALUES (?)', (name,))
        self.connection.commit()
        print("Department added successfully.")

    def add_manager(self, first_name, last_name,email,mobile_number, department_id):
        self.cursor.execute('INSERT INTO managers (first_name, last_name,email,mobile_number, department_id) VALUES (?,?,?,?,?)',
                            (first_name, last_name,email,mobile_number, department_id))
        self.connection.commit()
        print("Manager added successfully.")

    def add_employee(self, first_name, last_name, email, mobile_number,hire_date,salary, department_id, manager_id):
        self.cursor.execute('INSERT INTO employees (first_name, last_name, email , mobile_number,hire_date,salary,department_id, manager_id) VALUES (?,?,?,?,?,?,?,?)',
                            (first_name, last_name, email,mobile_number,hire_date,salary, department_id, manager_id))
        self.connection.commit()
        print("Employee added successfully.")

    def department_exists(self, department_id):
        self.cursor.execute('SELECT * FROM departments WHERE id = ?', (department_id,))
        return self.cursor.fetchone() is not None

    def manager_exists(self, manager_id):
        self.cursor.execute('SELECT * FROM managers WHERE id = ?', (manager_id,))
        return self.cursor.fetchone() is not None

    def list_departments(self):
        self.cursor.execute("SELECT * FROM departments")
        departments = self.cursor.fetchall()
        if departments:
            for department in departments:
                print(f"Department ID: {department[0]}, Name: {department[1]}")
        else:
            print("No departments found.")

    def list_managers(self):
        query = '''
            SELECT managers.id, managers.first_name, managers.last_name, departments.name
            FROM managers
            LEFT JOIN departments ON managers.department_id = departments.id
        '''
        self.cursor.execute(query)
        managers = self.cursor.fetchall()
        if managers:
            for manager in managers:
                print(f"Manager ID: {manager[0]}, First Name: {manager[1]}, Last Name: {manager[2]}, Department: {manager[3]}")
        else:
            print("No managers found.")

    def list_employees(self):
        query = '''
            SELECT employees.id, employees.first_name, employees.last_name, departments.name AS department, 
            managers.first_name AS manager_first_name, managers.last_name AS manager_last_name
            FROM employees
            LEFT JOIN departments ON employees.department_id = departments.id
            LEFT JOIN managers ON employees.manager_id = managers.id
        '''
        self.cursor.execute(query)
        employees = self.cursor.fetchall()
        if employees:
            for employee in employees:
                manager_info = f"{employee[4]} {employee[5]}" if employee[4] and employee[5] else "None"
                print(f"Employee ID: {employee[0]}, First Name: {employee[1]}, Last Name: {employee[2]}, Department: {employee[3]}, Manager: {manager_info}")
        else:
            print("No employees found.")

    def delete_department_by_id(self, department_id):
        if self.department_exists(department_id):
            self.cursor.execute("DELETE FROM departments WHERE id=?", (department_id,))
            self.connection.commit()
            print(f"Department with ID {department_id} deleted")
        else:
            print(f"Department with ID {department_id} does not exist")

    def delete_manager_by_id(self, manager_id):
        if self.manager_exists(manager_id):
            self.cursor.execute("DELETE FROM managers WHERE id=?", (manager_id,))
            self.connection.commit()
            print(f"Manager with ID {manager_id} deleted")
        else:
            print(f"Manager with ID {manager_id} does not exist")

    def delete_employee_by_id(self, employee_id):
        self.cursor.execute("DELETE FROM employees WHERE id=?", (employee_id,))
        self.connection.commit()
        print(f"Employee with ID {employee_id} deleted")

    def close(self):
        self.connection.close()

def main():
    db = CompanyDB()

    while True:
        print("\n1. Add Department")
        print("2. Add Manager")
        print("3. Add Employee")
        print("4. List Departments")
        print("5. List Managers")
        print("6. List Employees")
        print("7. Delete department by ID")
        print("8. Delete manager by ID")
        print("9. Delete employee by ID")
        print("10. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            name = input("Enter Department's name: ")
            db.add_department(name)
        elif choice == '2':
            first_name = input("Enter Manager's first name: ")
            last_name = input("Enter Manager's last name: ")
            email = input("Enter Manager's email: ")
            mobile_number = input("Enter Manager's mobile_number: ")
            department_id = int(input("Enter Department's ID: "))
            if db.department_exists(department_id):
                db.add_manager(first_name, last_name,email,mobile_number, department_id)
            else:
                print("Department does not exist.")
        elif choice == '3':
            first_name = input("Enter Employee's first name: ")
            last_name = input("Enter Employee's last name: ")
            email = input("Enter Employees email: ")
            mobile_number = input("Enter Employees mobile_number: ")
            hire_date = input("Enter Employees hire_date:")
            salary = input("Enter Employees salary: ")
            department_id = int(input("Enter Department's ID: "))
            manager_id = int(input("Enter Manager's ID: "))
            if db.department_exists(department_id) and db.manager_exists(manager_id):
                db.add_employee(first_name, last_name, email ,mobile_number,hire_date,salary,department_id, manager_id)
            else:
                print("Department or Manager does not exist.")
        elif choice == '4':
            db.list_departments()
        elif choice == '5':
            db.list_managers()
        elif choice == '6':
            db.list_employees()
        elif choice == '7':
            department_id = int(input("Enter Department ID to delete: "))
            db.delete_department_by_id(department_id)
        elif choice == '8':
            manager_id = int(input("Enter Manager ID to delete: "))
            db.delete_manager_by_id(manager_id)
        elif choice == '9':
            employee_id = int(input("Enter Employee ID to delete: "))
            db.delete_employee_by_id(employee_id)
        elif choice == '10':
            db.close()
            break
        else:
            print("Invalid choice. Please try again")  

if __name__ == '__main__':
    main()
