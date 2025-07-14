# def insert_patient_data(name, age):
#     print(name)
#     print(age)
#     print("inserted into database")
    
# insert_patient_data('nitish','thirty')

## there is no type validation in this if we want age as integer but user enter it in string but it accept it

## If we use type hunting but still it can take age as string without throwing an error


# def insert_patient_data(name, age):
#     if type(name)==str and type(age)==int:
        
#         print(name)
#         print(age)
#         print("inserted into database")
#     else:
#         raise TypeError("Incorrect datatype")
# insert_patient_data('nitish',30)

## the above type validation is good but if no. of input are more we need to do it with too many variables. 


## USing PYdantic 

from pydantic import BaseModel

#step1
class Patient(BaseModel):
    name: str
    age : int
    

def insert_patient_data( patient : Patient):
        
    print(patient.name)
    print(patient.age)
    print("inserted into database")


    
#stpe2 
patient_info = {'name':'Prince','age':22}

patient1 = Patient(**patient_info)

insert_patient_data(patient1)    
    
