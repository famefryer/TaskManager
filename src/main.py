from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn

from routes.router import router
from exceptions import custom_exception

app = FastAPI()
app.include_router(router)

@app.exception_handler(custom_exception.EntityNotFoundException)
async def entity_not_found_exception_handler(
    request: Request, exc: custom_exception.EntityNotFoundException
):
    return JSONResponse(status_code=404, content={"message": exc.message})


@app.exception_handler(custom_exception.EntityAlreadyExistException)
async def entity_not_found_exception_handler(
    request: Request, exc: custom_exception.EntityAlreadyExistException
):
    return JSONResponse(status_code=400, content={"message": exc.message})


@app.exception_handler(custom_exception.BadRequestException)
async def entity_not_found_exception_handler(
    request: Request, exc: custom_exception.BadRequestException
):
    return JSONResponse(status_code=400, content={"message": exc.message})


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
