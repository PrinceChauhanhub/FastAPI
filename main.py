from fastapi import FastAPI

app = FastAPI()

@app.get("/")   ## "/" it is the route means when user hit it it runs the hello function 
def hello():
    return {'message':'Hello World'}

@app.get("/about")
def about():
    return {'print':'it is a command to print the message'}