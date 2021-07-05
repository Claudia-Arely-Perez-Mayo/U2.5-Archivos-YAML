from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title = "FastAPI con Jinja2")

app.mount("/rutarecursos", StaticFiles(directory="recursos"), name="mirecurso")

miPlantilla = Jinja2Templates(directory="plantillas")

@app.get("/inicio/", response_class=HTMLResponse)
async def read_item(request: Request):
	datos = await cargarYAML()
    return miPlantilla.TemplateResponse("index.html",{"request":request, "lista":datos})

@app.get("/integrantes/", response_class=HTMLResponse)
async def leer_integrante(request: Request, Matricula: int, Nombre: str, APaterno: str, AMaterno: str, Edad: int, Telefono: int, 
                            Correo: str, Carrera: str):
    return miPlantilla.TemplateResponse("integrantes.html",{"request":request, "matri": Matricula, "nom":Nombre, "apellidopaterno":APaterno, 
                                                            "apellidomaterno": AMaterno, "edad":Edad,
                                                            "telefono": Telefono, "correo": Correo, "carrera": Carrera})
