
from pydantic import BaseModel, EmailStr, AnyUrl, Field

from typing import List, Dict, Optional, Annotated
#step1
class Patient(BaseModel):
    name: Annotated[str, Field(max_length=50,title="Name of the Patient",description="The name of patient in less than 50 chars",examples=['Nitish','Prince'])]
    email : EmailStr
    urls : AnyUrl
    age : int = Field(gt=0, lt=100)
    weight : float = Field(gt=0)
    married : Annotated[bool, Field(default=None,description="is patient married or not")]   ## False is by default value
    allergies : Optional[List[str]] = None   ## Stores a list
    contact_details: Dict[str, str]   ## Stores a dictionary
 
def insert_patient_data(patient : Patient):
        
    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print("inserted into database") 

#stpe2  
patient_info = {'name':'Prince','email':'abc@gmail.com',"urls":"http://linkedin.com/Princechauhan22",'age':22, 'weight':72.2,'married':False,'allergies':['pollen','dust'],'contact_details':{'phone':'233334612'}}

patient1 = Patient(**patient_info)

insert_patient_data(patient1)    
    