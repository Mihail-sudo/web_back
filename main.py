from fastapi import FastAPI
from routes import auth, messages

app = FastAPI()
app.include_router(auth.router)
app.include_router(messages.router)

@app.get("/")
def read_root():
    return {"message": "Messenger API"}
