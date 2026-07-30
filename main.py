from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import routers.routerUsuario as routerUsuario
import MODELS.etlexceptions as etlException

app = FastAPI(title="Mantenimiento de usuarios")

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(etlException.BusinessError)
def business_error_handler(request:Request, exc: etlException.BusinessError):
    return JSONResponse(
        status_code = exc.status_code,
        content={
            "codigo": exc.codigo, 
            "mensaje" :exc.mensaje
        }
    )

app.include_router(routerUsuario.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)