from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import json

app = FastAPI()


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
        
## Creating Pydanti Model
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