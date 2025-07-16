from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json

app = FastAPI()
        
## Creating Pydantic Model to Create
class Patient(BaseModel):
    id : Annotated[str, Field(..., description = 'Id of the Patient',examples=['P001'])]
    name: Annotated[str, Field(..., description='Name of the Patieny')]
    city : Annotated[str, Field(..., description="City where the patient lives")]
    age : Annotated[int, Field(..., gt = 0, lt = 120, description="Age of the Patient")]
    gender : Annotated[Literal['male', 'female', 'others'],Field(..., description="Gender of the Patient")]
    height : Annotated[float, Field(..., gt = 0, description="HHeight of Patient in meters")]
    weight : Annotated[float, Field(..., gt = 0,description="Weight of the patient in KG")]
    
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'underweight'
        elif self.bmi <25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Overweight'
        else:
            return 'obese'

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city : Annotated[Optional[str], Field(default=None)]
    age : Annotated[Optional[int], Field(default=None, gt= 0)]
    gender : Annotated[Optional[Literal['male','female']], Field(default=None)]
    height :Annotated[Optional[float], Field(default=None, gt = 0)]
    weight :Annotated[Optional[float], Field(default=None, gt = 0)]


def load_data():
    with open('patients.json','r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data ,f)
        

@app.get("/")
def hello():
    return {"message":"Patient Management System API"}
 

@app.get("/view")
def view():
    data = load_data()
    
    return data


@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description="ID of the patient in the DB",example="P001")):
    ## load all the patients
    data = load_data()
    
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,detail="Patient data not found")


## ... triple dot means it is required and if not ... means optional
@app.get("/sort")
def sort_patients(sort_by: str = Query(...,description="sort on the basis of height, weight and bmi"),order: str= Query('asc', description="sort in aesc or desc order")):
    valid_fields = ['height','weight','bmi']
    
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail = f"invalid field select from {valid_fields}")
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail="Invalid order select between asc and desc")
    data = load_data()
    
    sort_order = True if order=='desc' else False
    
    sorted_data = sorted(data.values(),key = lambda x:x.get(sort_by,0),reverse=sort_order)
    
    return sorted_data


@app.post('/create')
def create_patient(patient: Patient):  # patient variable of Patient datatype which is pydantic model
    ## Load existing data
    data = load_data()
    
    ## Check if the patient already exist or not
    if patient.id in data:
        raise HTTPException(status_code=400,detail='Patient Already exist')
    ## New patient add to the database
    
    #first convert pydantic data to dictionary
    data[patient.id] = patient.model_dump(exclude=['id'])
    
    ## save into the json file
    save_data(data)
    
    ## returning a response
    return JSONResponse(status_code=201,content={'message':'Patient Create Successfully'})


@app.put('/edit/{patient_id}')
def update_patient(patient_id : str, patient_update: PatientUpdate):
    
    # patient_update variable of pydantic object
    
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient Data Not Found")
    
    #extracting the existing patient data in json
    existing_patient_info = data[patient_id]
    
    # coverting patient_update pydantic object to dictionary
    updated_patient_info = patient_update.model_dump(exclude_unset = True)
    
    # exclude_unset= True bcs is se sirf vo data ayega jisme user ne value di hai....agar hm is false rkhte to sara data aa jata with the by default value of none jo hme nhi chaiye..
    
    
    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value
    
    
    ## suppose user weight mein update kr rha h to vo to change ho jayega lekin weight change ka mtlb h bmi aur verdict bhi change hona kyui vo weight pr dependent hain ....so hme isko shi krna pdega 
   
        
    # existing_patient_info se- > pydantic object create krnege patient class ka...jis se jaise hi hm dictionary ko pydantic objec tmein convert krenge ek new value bnega aur us process mein computed field dubara calculate hongi...to fir data new hoga.......then fir wapas convert krenge pydantic object ko dicionary mein aur fir ye last wala step kr denge data[patient_id] = existing_patient_info jis se data save ho jayega

    ## existing_patient_info -> pydantic object -> updated bmi + verdict -> pydantic object -> dict -> save operation
    
    existing_patient_info['id'] = patient_id
    patient_pydantic_obj = Patient(**existing_patient_info)
    
    # pydantic_object -> dict
    existing_patient_info = patient_pydantic_obj.model_dump(exclude = ['id'])
    
    ## add this dict to data
    data[patient_id] = existing_patient_info
    
    #save data
    save_data(data)
    
    return JSONResponse(status_code=200, content={'message':'Patient data updated'})