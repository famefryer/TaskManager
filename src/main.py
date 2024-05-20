from fastapi import FastAPI
import uvicorn

from routes.router import router

app = FastAPI()
app.include_router(router)

@app.get("/")
def root():
    return {"message" : "Hello, It's me"}

if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
