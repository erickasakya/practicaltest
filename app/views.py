from sqlalchemy.sql.elements import or_, and_
from werkzeug.exceptions import NotFound
from app.utils import render_template, expose, url_for, application, render_response
from app.models import Employee, Desigination, EmployeeSchema, DesiginationSchema
from sqlalchemy.orm import sessionmaker
from app.datasets.dataset1 import employee_data as employee_details, employee_designation
from app.datasets.dataset2 import actions_data
from app.datasets.dataset3 import get_dataset3
from datetime import date, datetime

employee_schema = EmployeeSchema(many=True)
employee_schema1 = EmployeeSchema()

employee_actions=get_dataset3()

@expose('/')
@expose('/home')
def homepage(request):
    return render_template('index.html', sentdata=[])

@expose('/scrapp')  
def scrapp(request):
    session = create_db_session()
    session.query(Employee).delete()
    session.query(Desigination).delete()
    session.commit()
    for data in employee_details:
        empl = Employee(first_name=data['first_name'], last_name=data['last_name'], other_names=data['other_names'], date_of_joining=data['date_of_joining'], status_id=data['status_id'])
        session.add(empl)

    for data in employee_designation:
        empl_des=Desigination(employee_id=data['employee_id'],title=data['title'])
        session.add(empl_des)
    session.commit()
    session.close()
    return render_template('index.html')


@expose('/employees/list')  
def employee_list1(request):
    resp_results=employee_list()
    return render_response({"data": resp_results})

@expose('/employee_details')  
def employee_data(request):
    employee_id=request.args.get('employee_id')
    role_actions=actions_data[staff_role_check(employee_id)]

    actions_keys = role_actions.keys()
    actions_values = role_actions.values()

    actions=[]
    for action_id, action in zip(actions_keys, actions_values):
        actions.append(dict(id= action_id, action= action))

    session = create_db_session()

    employee_data=session.query(Employee).filter(Employee.id == int(employee_id)).first()
    employee_data=employee_schema1.dump(employee_data)
    
    result = session.query(Employee).filter(or_(Employee.first_name.like(employee_data['last_name']),Employee.last_name.like(employee_data['last_name']), Employee.other_names.like(employee_data['last_name'])),or_(or_(Employee.first_name.like(employee_data['other_names']),Employee.last_name.like(employee_data['other_names']), Employee.other_names.like(employee_data['other_names'])),or_(Employee.first_name.like(employee_data['first_name']),Employee.last_name.like(employee_data['first_name']), Employee.other_names.like(employee_data['first_name'])))).filter(Employee.id != int(employee_id)).all()

    similar_employees=employee_schema.dump(result)
    
    session.close()
    response={
        "role_actions": actions,
        "similar_employees": similar_employees
    }
    return render_response(response)

def employee_list():
    session = create_db_session()
    result = session.query(Employee).join(Desigination).all()
    employee_details=[] 
    staff_status=['Active','Left','Pending']
    roles_data=['Admin','Editor','Viewer','-']
    for row in result:
        for inv in row.desigination:
            employee_details.append({"id":row.id,"first_name":row.first_name,"last_name":row.last_name,"other_names":row.other_names,"staff_status":staff_status[row.status_id-1] , "designation":inv.title,"role": roles_data[staff_role_check(row.id)], "time_spent": years_between(row.date_of_joining)})
    session.close()
    return employee_details
     

def years_between(d1):
    now = date.today()
    d1 = datetime.strptime(str(d1), "%Y-%m-%d")
    d2 = datetime.strptime(str(now), "%Y-%m-%d")
    days= abs((d2 - d1).days)
    
    if days >=730:
        return "Old"
    return "New"

def staff_role_check(employee_id):
    employee_action_id=[]
    if 'success' in employee_actions:
        return 0

    for data in employee_actions:
        if data['employee_id'] == int(employee_id) and data['blog_action_id'] in [1,3,7,4,5,8,10,13]:
            employee_action_id.append(data['blog_action_id'])
    roles=[[1,3,7,4,5,8,10,13], [1,4,5,7,10,13], [4]]
    counter=0
    for role in roles:
        if areEqual(role,employee_action_id,len(role),len(employee_action_id)):
            return counter
        counter +=1

    return counter

def areEqual(arr1, arr2, n, m):
    if (n != m):
        return False
    arr1.sort()
    arr2.sort()
    for i in range(0, n - 1):
        if (arr1[i] != arr2[i]):
            return False
    return True

def create_db_session():
    Session = sessionmaker(bind=application.database_engine)
    session = Session()
    return session