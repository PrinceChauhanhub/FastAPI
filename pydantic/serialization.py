from pydantic import BaseModel

class Address(BaseModel):
    
    city : str
    state : str
    pin : str
class Patient(BaseModel):
    name : str
    gender : str
    age : int
    address : Address   ##it is a complex data made up of different data types e.g 'house 2 , sec -66, gurgaon, haryana 120222
    
address_dict = {'city':'gurgaon','state':'haryana','pin':'122001'}

address1 = Address(**address_dict)

patient_dict = {'name':'prince','gender':'male','age':22,'address':address1}

patient1 = Patient(**patient_dict)

temp = patient1.model_dump()

print(temp)
print(type(temp))

temp1 = patient1.model_dump_json()

print(temp1)
print(type(temp1))

## exclude -  to exclude the field while dumping

### include - to include only the required field while dumping

## exclude_unset = True  jo field object creation ke time set kri gyi thi whi dikhayi jayengi