
from pydantic import BaseModel, EmailStr, AnyUrl, Field, model_validator

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
    
    @model_validator(mode='after')
    def validate_emergency_contact(cls,model):
        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError("PAtients older than 60 must have an emergency number")
        return model
    
def insert_patient_data(patient : Patient):
        
    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print("inserted into database") 

#stpe2  
patient_info = {'name':'Prince','email':'abc@hdfc.com',"urls":"http://linkedin.com/Princechauhan22",'age':65, 'weight':72.2,'married':False,'allergies':['pollen','dust'],'contact_details':{'phone':'233334612','emergency':'54355432'}}

patient1 = Patient(**patient_info)  #validation happens 

insert_patient_data(patient1)    
    