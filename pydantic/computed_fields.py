
from pydantic import BaseModel, EmailStr, AnyUrl, Field, computed_field

from typing import List, Dict, Optional, Annotated
#step1
class Patient(BaseModel):
    name: str
    email : EmailStr
    urls : AnyUrl
    age : int
    weight : float ##meter
    height : float ##kg
    married : Annotated[bool, Field(default=None,description="is patient married or not")]   ## False is by default value
    allergies : Optional[List[str]] = None   ## Stores a list
    contact_details: Dict[str, str]   ## Stores a dictionary
 
    @computed_field
    @property
    def calculate_bmi(self) -> float:
        bmi = round(self.weight / (self.height**2),2)
        return bmi
def insert_patient_data(patient : Patient):
        
    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.calculate_bmi)
    print("inserted into database") 

#stpe2  
patient_info = {'name':'Prince','email':'abc@gmail.com',"urls":"http://linkedin.com/Princechauhan22",'age':22, 'weight':72.2,'height':1.72,'married':False,'allergies':['pollen','dust'],'contact_details':{'phone':'233334612'}}

patient1 = Patient(**patient_info)

insert_patient_data(patient1)    
    