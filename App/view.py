"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

from prettytable.prettytable import ALL, HEADER
import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf
from DISClib.ADT import map as mp
import time
from prettytable import PrettyTable
from datetime import datetime

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def obtener_nombres_artistas(obra):
    artistas = mp.get(obra,"Artistas")["value"]
    lista = []
    for artista in lt.iterator(artistas):
        lista.append(mp.get(artista,"Nombre")["value"])
    return lista



def print_artistas_cronologico(resultado,tiempo):
    print("Hay un total de " + str(lt.size(resultado)) + " artistas en el rango.")
    print("Se muestra a continuación los 3 primeros y los 3 últimos:")

    tabla = PrettyTable()
    tabla.field_names = ["Nombre","Año de nacimiento","Año de fallecimiento","Nacionaliad","Genero"]
    
    for i in range(1,4):
        artista = lt.getElement(resultado,i)
        tabla.add_row([mp.get(artista,"Nombre")["value"],mp.get(artista,"Año")["value"],mp.get(artista,"Fecha_falle")["value"],mp.get(artista,"Nacionalidad")["value"],mp.get(artista,"Genero")["value"]])
    
    for i in range(lt.size(resultado)-3,lt.size(resultado)):
        artista = lt.getElement(resultado,i)
        tabla.add_row([mp.get(artista,"Nombre")["value"],mp.get(artista,"Año")["value"],mp.get(artista,"Fecha_falle")["value"],mp.get(artista,"Nacionalidad")["value"],mp.get(artista,"Genero")["value"]])

    print(tabla)
    print("Tiempo requerido: " + str(tiempo) + " msg")


def print_numero_obras_nacionaliad(resultado,tiempo):

    tabla = PrettyTable()
    tabla.field_names=["Nacionalidad","Número de obras"]
    for i in range(1,10):
        nacionalidad = lt.getElement(resultado,i)
        tabla.add_row([mp.get(nacionalidad,"Nacionalidad")["value"],mp.get(nacionalidad,"Conteo")["value"]])

    print("El top 10 de nacionalidades con más obras es:")
    print(tabla)

    print("Muestra de las lista de la nacionalidad con mayor cantidad de obras:")
    tabla2 =PrettyTable(hrules = ALL)
    tabla2.field_names = ["Titulo","Artista(s)","Fecha","Medio","Dimensiones"]
    tabla2.max_width = 47
    
    lista = mp.get(lt.getElement(resultado,1),"Obras")["value"]
    for i in range(1,4):
        obra = lt.getElement(lista,i)
        nombre_artistas = obtener_nombres_artistas(obra)
        tabla2.add_row([mp.get(obra,"Titulo")["value"],nombre_artistas,mp.get(obra,"Fecha")["value"],mp.get(obra,"Medio")["value"],mp.get(obra,"Dimensiones")["value"]])

    for i in range(lt.size(lista)-3,lt.size(lista)):
        obra = lt.getElement(lista,i)
        nombre_artistas = obtener_nombres_artistas(obra)
        tabla2.add_row([mp.get(obra,"Titulo")["value"],nombre_artistas,mp.get(obra,"Fecha")["value"],mp.get(obra,"Medio")["value"],mp.get(obra,"Dimensiones")["value"]])
    
    print(tabla2)
    print("Tiempo requerido: " + str(tiempo) + " msg")

def initCatalog():
    return controller.initCatalog()

def loadData(catalog):
    return controller.loadData(catalog)

def printMenu():
    print("Bienvenido")
    print("0- Cargar información en el catálogo")
    print("1- Listar cronnológicamente artistas")
    print("2- Listar cronológicamente las adquisiciones")
    print("4- Clasificar obras por nacionalidad de sus creadores")


catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 0:
        print("Cargando información de los archivos ....")
        start_time = time.process_time()
        catalog = initCatalog()
        loadData(catalog)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print("Se han cargado los datos exitosamente.")
        print("Tiempo requerido: "+ str(elapsed_time_mseg) + " mseg")

    elif int(inputs[0]) == 1:
        anio_i = int(input("Ingrese el año inicial: "))
        anio_f = int(input("Ingrese el año final: "))
        print("Cargando información...")
        start_time = time.process_time()
        resultado = controller.artistas_cronologico(catalog,anio_i,anio_f)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print_artistas_cronologico(resultado,elapsed_time_mseg)

    
    elif int(inputs[0]) == 2:
        fecha_i = input("Ingrese la fecha inicial (YYYY-MM-DD): ")
        fecha_i = fecha_i.strip()
        fecha_i = datetime.strptime(fecha_i,"%Y-%m-%d")
        fecha_f = input("Ingrese la fecha final (YYYY-MM-DD): ")
        fecha_f = fecha_f.strip()
        fecha_f = datetime.strptime(fecha_f,"%Y-%m-%d")
        print("Cargando información de los archivos...")
        start_time = time.process_time()
        resultado = controller.adquisiciones_cronologico(fecha_i,fecha_f,catalog)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print(elapsed_time_mseg)
        #printAdquisicionesCronologicas(resultado[0],resultado[1],elapsed_time_mseg)

    elif int(inputs[0]) == 3:
        print("Ya que estoy solo en el grupo este requerimiento no fue implementado")

    elif int(inputs[0]) == 4:
        print("Cargando información...")
        start_time = time.process_time()
        resultado = controller.obras_por_nacionalidad(catalog)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print_numero_obras_nacionaliad(resultado,elapsed_time_mseg)

    else:
        sys.exit(0)
sys.exit(0)