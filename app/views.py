# import requests
from werkzeug.exceptions import NotFound
from app.utils import render_template, expose, url_for, application
from app.models import Employee, Desigination
from sqlalchemy.orm import sessionmaker
from app.datasets.dataset1 import employee_data, employee_designation
from app.datasets.dataset3 import get_dataset3
from datetime import date, datetime

employee_actions=get_dataset3()

@expose('/')
@expose('/home')
def homepage(request):
    employee_details=employee_list(request)
    return render_template('index.html', sentdata=employee_details)

@expose('/scrapp')  
def scrapp(request):
    session = create_db_session()
    session.query(Employee).delete()
    session.query(Desigination).delete()
    session.commit()
    for data in employee_data:
        empl = Employee(first_name=data['first_name'], last_name=data['last_name'], other_names=data['other_names'], date_of_joining=data['date_of_joining'], status_id=data['status_id'])
        session.add(empl)

    for data in employee_designation:
        empl_des=Desigination(employee_id=data['employee_id'],title=data['title'])
        session.add(empl_des)
    session.commit()
    session.close()
    employee_details=employee_list(request)
    return render_template('index.html', sentdata=employee_details)


@expose('/employees')  
def employee_list(request):
    session = create_db_session()
    result = session.query(Employee).join(Desigination).all()
    employee_details=[] 
    staff_status=['Active','Left','Pending']
    roles_data=['Admin','Editor','Viewer','-']
    for row in result:
        for inv in row.desigination:
            employee_details.append([row.id, row.first_name,row.last_name, row.other_names, staff_status[row.status_id-1] , inv.title, roles_data[staff_role_check(row.id)], years_between(row.date_of_joining)])
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
    for data in employee_actions:
        if data['employee_id'] == employee_id and data['blog_action_id'] in [1,3,7,4,5,8,10,13]:
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