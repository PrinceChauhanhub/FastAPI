
from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator

from typing import List, Dict, Optional, Annotated
#step1
class Patient(BaseModel):
    name: str
    email : EmailStr
    urls : AnyUrl
    age : int 
    weight : float = Field(gt=0)
    married : Annotated[bool, Field(default=None,description="is patient married or not")]   ## False is by default value
    allergies : Optional[List[str]] = None   ## Stores a list
    contact_details: Dict[str, str]   ## Stores a dictionary
    
    @field_validator('email')
    @classmethod
    def email_validator(cls,value):
        valid_domains = ['hdfc.com','icici.com']
        domain_name = value.split('@')[-1]
        
        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')
        
        return value
    
    ## want name in capital letters
    @field_validator('name')
    def transform_name(cls, value):
        return value.upper()
    
    @field_validator('age',mode='before')
    def validate_age(cls, value):
        if 0 < value < 100:
            return value
        else:
            raise ValueError("age should be in between 0 and 100")
    
def insert_patient_data(patient : Patient):
        
    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print("inserted into database") 

#stpe2  
patient_info = {'name':'Prince','email':'abc@hdfc.com',"urls":"http://linkedin.com/Princechauhan22",'age':22, 'weight':72.2,'married':False,'allergies':['pollen','dust'],'contact_details':{'phone':'233334612'}}

patient1 = Patient(**patient_info)  #validation happens 

insert_patient_data(patient1)    
    