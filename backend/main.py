from fastapi import FastAPI 

app = FastAPI(
    tile = "PlacekoV5",
    description = "This is my agentic AI application",
   
)
@app.get("/")
def home():
    return {"message":"Hello i am root"}

