import numpy as np

PARAMETROS_SISTEMA = {}
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
def validar_parametros_sistema(Vlinea, f, fp_deseado, config):
    """
    Valida los parámetros del sistema:
    - Vlinea: tensión de línea (V), debe ser > 0
    - f: frecuencia (Hz), debe ser > 0
    - fp_deseado: factor de potencia deseado, entre 0 y 1
    - config: configuración del banco, 'estrella' o 'delta'
    """
    if Vlinea <= 0:
        raise ValueError("La tensión de línea debe ser mayor que cero.")
    if f <= 0:
        raise ValueError("La frecuencia debe ser mayor que cero.")
    if not (0 < fp_deseado <= 1):
        raise ValueError("El factor de potencia deseado debe estar entre 0 y 1.")
    if config.lower() not in ["estrella", "delta"]:
        raise ValueError("La configuración debe ser 'estrella' o 'delta'.")
    return True

def ingresar_parametros_sistema():
    #Solicita y guarda los datos generales del sistema
    #(Tensión de línea,frecuencia,fp_deseado,
    #configuración estrella/ delta)
    try:
        Vlinea = float(input("Ingrese la tensión de línea [V]: "))
        f = float(input("Ingrese la frecuencia [Hz]: "))
        fp_deseado = float(input("Ingrese el factor de potencia deseado (0-1): "))
        config = input("Ingrese la condiguración (estrella/delta): ").strip().lower()

        #Validar
        validar_parametros_sistema(Vlinea,f,fp_deseado,config)

        #Guardar en diccionario global
        global PARAMETROS_SISTEMA
        PARAMETROS_SISTEMA = {
            "Vlinea": Vlinea,
            "f": f,
            "fp_deseado":fp_deseado,
            "config":config
        }
        print("\n✅ Parámetros del sistema guardados correctamente.")
        return PARAMETROS_SISTEMA

    except ValueError as e:
        print(f"❌ Error: {e}")
        return None


def ingresar_carga():
    #ingresa el nombre y pide dos parámetros de la carga
    #devuelve un diccionario de la forma:
    # carga={"nombre": "nombre_carga", dos datos más}
    #ya sea P,S,Q o fp
    carga = {}
    nombre = input("Ingrese el nombre de la carga: ").strip()
    carga["nombre"] = nombre

    # Variables permitidas
    opciones = ["P", "Q", "S", "fp"]

    print("\nDebe ingresar al menos dos variables entre P, Q, S, fp.")
    print("Opciones disponibles:", opciones)

    # Loop de ingreso
    while True:
        var = input("\nSeleccione la variable a ingresar (P/Q/S/fp): ").strip()
        if var not in opciones:
            print("❌ Opción inválida. Intente de nuevo.")
            continue

        try:
            valor = float(input(f"Ingrese el valor de {var}: "))
            carga[var] = valor
        except ValueError:
            print("❌ Valor inválido. Debe ser numérico.")
            continue

        # Condición de salida: al menos dos variables
        variables_ingresadas = [k for k in carga.keys() if k in opciones]

        if len(variables_ingresadas) >= 2:
            salir = input("¿Desea terminar el ingreso? (s/n): ").strip().lower()
            if salir == "s":
                break

    print("\n✅ Datos de la carga ingresados correctamente.")
    return carga

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
    datos_presentes = [x for x in [P, Q, S, fp] if x is not None]
    if len(datos_presentes)<2:
        raise ValueError("Debes ingresar al menos dos parámetros entre P,Q,S,fp")
    #Caso 1: P y fp
    if P is not None and fp is not None:
        S = P /fp
        Q= np.sqrt(S**2-P**2)
    #Caso 2: P y Q
    elif P is not None and Q is not None:
        S = np.sqrt(P**2+Q**2)
        fp = P/S
    #Caso 3: P y S
    elif P is not None and S is not None:
        Q = np.sqrt(S**2-P**2)
        fp = P/S
    #Caso 4: S y fp
    elif S is not None and fp is not None:
        P = S * fp
        Q = np.sqrt(S**2-P**2)
    #Caso 5: S y Q
    elif S is not None and Q is not None:
        P = np.sqrt(S**2-Q**2)
        fp = P/S
    #Caso 6 Q y fp:
    elif Q is not None and fp is not None:
        denom = np.sqrt(1-fp**2)
        P = (fp*abs(Q))/denom
        S = np.sqrt(P**2+Q**2)

    #Retorna salida con el diccionario completo
    resultado = {
        "nombre": nombre,
        "P":P,
        "Q": Q,
        "S":S,
        "fp":fp
    }
    return resultado

def calcular_totales(lista_cargas):
    Ptot = 0.0
    Qtot = 0.0
    #Suma todas las cargas ingresadas y
    #retorna los valores totales

    #Sumar cargas
    for carga in lista_cargas:
        Ptot += carga.get("P",0.0)
        Qtot += carga.get("Q",0.0)


    
    Stot = np.sqrt(Ptot**2 + Qtot**2)
    fp_act = Ptot/Stot if Stot> 0 else 0.0
    return {
        "Ptot": Ptot,
        "Qtot": Qtot,
        "Stot": Stot,
        "fp_act": fp_act
    }

def necesidad_compensacion(totales,fp_act,fp_deseado):
    # Compara el factor de potencia actual con el deseado
    #devuelve Qc si es necesario calcular el banco de capacitores
    # si no devuelve un True
    Ptot = totales.get("Ptot", 0.0)
    if fp_act >= fp_deseado:
        return {
            "fp_act": fp_act,
            "fp_deseado": fp_deseado,
            "necesita_compensacion": False,
            "Qc": 0.0}
    else:
        Qc = Ptot *(np.tan(np.arccos(fp_act))- np.tan(np.arccos(fp_deseado)))
        return {"fp_act": fp_act,
            "fp_deseado": fp_deseado,
            "necesita_compensacion": True,
            "Qc": Qc}
def calcular_capacitancia(Qc, Vlinea,f,configuracion):
    """Convierte la potencia reactiva necesaria en capacitancia
    Calcula w=2 pi f
    si es estrella Vfase = Vlinea/raiz(3)
    Si es delta usar Vlinea
    Fórmula C = Qc/V^2*w
    retorna la capacitancia por fase"""
    w = 2 * np.pi * f
    if configuracion.lower() == "estrella":
        V = Vlinea/ np.sqrt(3)
        C = Qc/ (V**2 *w)
    else:
        V = Vlinea
        C = Qc/ (V**2 *w)
    return C

def mostrar_resultados(fp_act,fp_deseado,Qc,C):
    """Presenta los resultados finales
    Muestra el fp actual y el deseado
    Mostrar si necesita compensación
    si sí mostrar Qc y C
    Presenta los resultados finales:
    - Muestra el fp actual y el deseado
    - Indica si se necesita compensación
    - Si sí, muestra Qc y C por fase
    """
    print("\n📊 RESULTADOS DEL SISTEMA")
    print(f"Factor de potencia actual:   {fp_act:.3f}")
    print(f"Factor de potencia deseado:  {fp_deseado:.3f}")

    if fp_act >= fp_deseado:
        print("✅ No se requiere compensación. El sistema ya cumple con el FP deseado.")
    else:
        print("⚠️ Se requiere compensación.")
        print(f"Potencia reactiva a compensar (Qc): {Qc:.2f} var")
        print(f"Capacitancia por fase: {C*1e6:.2f} µF")
    return

def main():
    print("=== PROGRAMA DE COMPENSACIÓN DE FACTOR DE POTENCIA ===")

    # 1. Ingresar parámetros del sistema
    sistema = ingresar_parametros_sistema()
    if sistema is None:
        return

    # 2. Ingresar cargas
    lista_cargas = []
    while True:
        carga = ingresar_carga()
        carga_completa = calcular_datos_carga(carga)
        lista_cargas.append(carga_completa)

        otra = input("¿Desea ingresar otra carga? (s/n): ").strip().lower()
        if otra != "s":
            break

    # 3. Calcular totales
    totales = calcular_totales(lista_cargas)

    # 4. Determinar necesidad de compensación
    resultado = necesidad_compensacion(totales, totales["fp_act"], sistema["fp_deseado"])

    # 5. Si necesita compensación, calcular capacitancia
    C = 0.0
    if resultado["necesita_compensacion"]:
        C = calcular_capacitancia(resultado["Qc"], sistema["Vlinea"], sistema["f"], sistema["config"])

    # 6. Mostrar resultados finales
    mostrar_resultados(resultado["fp_act"], resultado["fp_deseado"], resultado["Qc"], C)
    return 



if __name__ == "__main__":
    main()
