from datetime import date, datetime
from sqlalchemy import Table, Column, String, ForeignKey, DateTime, Integer, Date
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

Base = declarative_base()

class Employee(Base):
    __tablename__ = "employee"
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    other_names = Column(String)
    date_of_joining = Column(Date, default=date(2012,1,1))
    status_id = Column(Integer, default=1)
    desigination = relationship("Desigination", backref=backref("employee"))

    def __repr__(self):
        return '<Employee %r>' % self.first_name

class Desigination(Base):
    __tablename__ = "desigination"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    employee_id =Column(Integer, ForeignKey("employee.id"))

    def __repr__(self):
        return '<Desigination %r>' % self.title
        

class EmployeeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Employee
        include_relationships = True
        load_instance = True


class DesiginationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Desigination
        include_fk = True
        load_instance = True