from typing import List
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import yaml

app = FastAPI(title = "FastAPI con Jinja2")
app.mount("/rutarecursos", StaticFiles(directory="recursos"), name="mirecurso")
miPlantilla = Jinja2Templates(directory="plantillas")

async def cargarYAML():
    with open('lista_alumnos.yml', "r",  encoding='utf-8-sig') as archivo_yml:
        diccionario = yaml.load(archivo_yml, Loader=yaml.FullLoader)
        #print(diccionario)
        #datos = yaml.load(archivo_yml)
        miLista = diccionario['alumnos']
        #print(miLista)
    return miLista

async def guardarYAML(datosAgregar:List):
    nuevo_dicc = {}
    nuevo_dicc["alumnos"] = datosAgregar
    #print("lista a guardar:")
    #print(nuevo_dicc)
    with open('lista_alumnos.yml',"w") as archivo_yml:
        #yaml.dump(nuevo_dicc, archivo_yml)
        #yaml.dump(nuevo_dicc, archivo_yml, sort_keys=False, indent=4)
        yaml.dump(nuevo_dicc, archivo_yml, default_flow_style=False, sort_keys=False)


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    datos = await cargarYAML()
    return miPlantilla.TemplateResponse("index.html",{"request":request, "lista":datos})
    

@app.get("/lista", response_class=HTMLResponse)
async def iniciar(request: Request):
    datos = await cargarYAML()
    return miPlantilla.TemplateResponse("listaIntegrantes.html",{"request":request,"lista":datos})


@app.post("/agregar")
async def agregar(request:Request):
    datos = await cargarYAML()
    nuevos_datos = {}
    datos_formulario = await request.form()
    #print(datos_formulario)
    ultimo_id = datos[-1].get("item_id")  #valor del id del ultimo elemento de la lista
    nuevos_datos["item_id"] = ultimo_id+1
    nuevos_datos["Matricula"] = int(datos_formulario["f_matricula"])
    nuevos_datos["Nombre"] = datos_formulario["f_nombre"]
    nuevos_datos["APaterno"] = datos_formulario["f_apaterno"]
    nuevos_datos["AMaterno"] = datos_formulario["f_amaterno"]
    nuevos_datos["Edad"] = int(datos_formulario["f_edad"])
    nuevos_datos["Telefono"] = int(datos_formulario["f_telefono"])
    nuevos_datos["Correo"] = datos_formulario["f_correo"]
    nuevos_datos["Carrera"] = datos_formulario["f_carrera"]
    #print(nuevos_datos)
    datos.append(nuevos_datos)

    await guardarYAML(datos)

    return RedirectResponse("/lista",303)

@app.get("/eliminar/{id}")
async def eliminar(request:Request,id:int):
    datos = await cargarYAML()
    del datos[id]
    #print("Item eliminado")
    #print(datos)
    await guardarYAML(datos)

    return RedirectResponse("/lista",303)

@app.get("/modificar/{id}")
async def modificar(request:Request,id:int):
    datos = await cargarYAML()
    id1 = datos[id]
    id2 = id1['item_id']
    print (id2)
    return miPlantilla.TemplateResponse("modificar.html",{"request":request,"lista":datos,"id":id2})

@app.post("/modificarJSON/{id}")
async def modificar(request:Request,id:int):
    datos = await cargarYAML()
    datos[id]
    nuevos_datos = datos[id]
    datos_formulario = await request.form()
    nuevos_datos["Matricula"] = int(datos_formulario["f_matricula"])
    nuevos_datos["Nombre"] = datos_formulario["f_nombre"]
    nuevos_datos["APaterno"] = (datos_formulario["f_apaterno"])
    nuevos_datos["AMaterno"] = (datos_formulario["f_amaterno"])
    nuevos_datos["Edad"] = int(datos_formulario["f_edad"])
    nuevos_datos["Correo"] = (datos_formulario["f_correo"])
    nuevos_datos["Telefono"] = int(datos_formulario["f_telefono"])
    nuevos_datos["Carrera"] = (datos_formulario["f_carrera"])
    datos[id] = nuevos_datos
    await guardarYAML(datos)
    return RedirectResponse("/lista",303)
    

@app.get("/colaborador/{id}")
async def modificar(request:Request,id:int):
    datos = await cargarYAML()
    id1 = datos[id]
    id2 = id1['item_id']
    print (id2)
    return miPlantilla.TemplateResponse("integrantes.html",{"request":request,"lista":datos,"id":id2})
