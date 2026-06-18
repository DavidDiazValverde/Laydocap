import numpy as np


def SumaTotal(vl, f, fp):
    suma = vl + f + fp
    return suma


#Funciones para el sistema

#Necesitamos implementar las siguientes cosas
# Una función que validación, simplemente se encarga de validar si un dato es un numero o no
# a esa la llamaremos validación_flotante
#Seguidamente necesito una función para ingresar datos en ella se debe tener que el usuario ingrese:
#-Tensión de Línea, frecuencia en hertz, factor de potencia deseado,
#configuración del banco de capacitores.
#Después debemos crear una función pequeña que sea simplemente para ingresar una nueva carga:
# En ella se agrega un nombre que identifique a la carga, al menos dos de los siguientes datos:
#Potencia aparente (S), Potencia activa (P), Potencia Reactiva (Q), Factor de potencia (fp)
#Otra función debe ser simplemente comparar si el fp que nos dieron es menor, mayor o igual y devolver
#el booleano.
#Calcular el banco de capacitores

def ingresar_parametros_sistema():
    #Solicita y guarda los datos generales del sistema
    #(Tensión de línea,frecuencia,fp_deseado,
    #configuración estrella/ delta)
    return

def ingresar_carga():
    #ingresa el nombre y pide dos parámetros de la carga
    #devuelve un diccionario de la forma:
    # carga={"nombre": "nombre_carga", dos datos más}
    #ya sea P,S,Q o fp
    return

def calcular_datos_carga(datos):
    """Recibe un diccionario con:
    - nombre: identificador de la carga
    al menos dos de los siguientes datos: P,Q,S,fp
    reconstruye los valores faltantes"""

    nombre = datos.get("nombre", "Carga_sin_nombre")
    P = datos.get("P",None)
    Q = datos.get("Q",None)
    S = datos.get("S", None)
    fp = datos.get("fp", None)

    # Validación al menos dos datos
    
    #Caso 1: P y fp

    #Caso 2: P y Q

    #Caso 3: S y fp

    #Caso 4: S y Q

    #Retorna salida con el diccionario completo

    return 

def calcular_totales(lista_cargas):
    #Suma todas las cargas ingresadas y
    #retorna los valores totales
    return

def necesidad_compensacion(fp_act,fp_deseado):
    # Compara el factor de potencia actual con el deseado
    #devuelve Qc si es necesario calcular el banco de capacitores
    # si no devuelve un True
    return
def calcular_capacitancia(Qc, Vlinea,f,configuracion):
    """Convierte la potencia reactiva necesaria en capacitancia
    Calcula w=2 pi f
    si es estrella Vfase = Vlinea/raiz(3)
    Si es delta usar Vlinea
    Fórmula C = Qc/V^2*w
    retorna la capacitancia por fase"""
    
    return

def mostrar_resultados(fp_act,fp_deseado,QC,C):
    """Presenta los resultados finales
    Muestra el fp actual y el deseado
    Mostrar si necesita compensación
    si sí mostrar Qc y C"""
    return