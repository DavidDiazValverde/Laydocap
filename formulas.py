import numpy as np


def validar_parametros_sistema(Vlinea, f, fp_deseado, config):
    """Lanza un error si algún parámetro del sistema no es válido."""
    if Vlinea <= 0:
        raise ValueError("La tensión de línea debe ser mayor que cero.")
    if f <= 0:
        raise ValueError("La frecuencia debe ser mayor que cero.")
    if not (0 < fp_deseado <= 1):
        raise ValueError("El factor de potencia deseado debe estar entre 0 y 1.")
    if config.lower() not in ["estrella", "delta"]:
        raise ValueError("La configuración debe ser 'estrella' o 'delta'.")
    return True

def calcular_datos_carga(datos):
    """Reconstruye los valores faltantes de una carga."""
    nombre = datos.get("nombre", "Carga_sin_nombre")
    
    # Extraemos considerando que la interfaz envía claves en minúscula ("p", "q") o mayúscula ("P", "Q")
    P = datos.get("p") if "p" in datos else datos.get("P")
    Q = datos.get("q") if "q" in datos else datos.get("Q")
    S = datos.get("s") if "s" in datos else datos.get("S")
    fp = datos.get("fp") if "fp" in datos else datos.get("FP")

    # Validación: al menos dos datos
    datos_presentes = [x for x in [P, Q, S, fp] if x is not None]
    if len(datos_presentes) < 2:
        raise ValueError(f"Faltan datos suficientes en la carga: {nombre}")

    # Cálculos trigonométricos
    if P is not None and fp is not None:
        S = P / fp
        Q = np.sqrt(S**2 - P**2)
    elif P is not None and Q is not None:
        S = np.sqrt(P**2 + Q**2)
        fp = P / S
    elif P is not None and S is not None:
        Q = np.sqrt(S**2 - P**2)
        fp = P / S
    elif S is not None and fp is not None:
        P = S * fp
        Q = np.sqrt(S**2 - P**2)
    elif S is not None and Q is not None:
        P = np.sqrt(S**2 - Q**2)
        fp = P / S
    elif Q is not None and fp is not None:
        denom = np.sqrt(1 - fp**2)
        P = (fp * abs(Q)) / denom
        S = np.sqrt(P**2 + Q**2)

    return {"nombre": nombre, "P": P, "Q": Q, "S": S, "fp": fp}

def calcular_totales(lista_cargas_calculadas):
    """Suma todas las cargas y retorna los valores totales del sistema."""
    Ptot = sum(carga.get("P", 0.0) for carga in lista_cargas_calculadas)
    Qtot = sum(carga.get("Q", 0.0) for carga in lista_cargas_calculadas)
    
    Stot = np.sqrt(Ptot**2 + Qtot**2)
    fp_act = Ptot / Stot if Stot > 0 else 0.0
    
    return {"Ptot": Ptot, "Qtot": Qtot, "Stot": Stot, "fp_act": fp_act}

def necesidad_compensacion(totales, fp_deseado):
    """Verifica si el sistema requiere banco de capacitores."""
    Ptot = totales.get("Ptot", 0.0)
    fp_act = totales.get("fp_act", 0.0)
    
    if fp_act >= fp_deseado:
        return {"necesita_compensacion": False, "Qc": 0.0}
    else:
        Qc = Ptot * (np.tan(np.arccos(fp_act)) - np.tan(np.arccos(fp_deseado)))
        return {"necesita_compensacion": True, "Qc": Qc}

def calcular_capacitancia(Qc, Vlinea, f, configuracion):
    """Calcula la capacitancia por fase requerida."""
    w = 2 * np.pi * f
    Qc_fase = QC /3
    if configuracion.lower() == "estrella":
        V = Vlinea / np.sqrt(3)
        C = Qc_fase / (V**2 * w)
    else: # Delta
        V = Vlinea
        C = Qc_fase / (V**2 * w)
    return C

def procesar_sistema_completo(Vlinea, f, fp_deseado, config, lista_cargas_brutas):
    """
    Función maestra que conecta la interfaz con la matemática.
    Valida, calcula todo y devuelve un diccionario completo con los resultados.
    """
    # 1. Validar parámetros iniciales
    validar_parametros_sistema(Vlinea, f, fp_deseado, config)
    
    if not lista_cargas_brutas:
        raise ValueError("Debe añadir al menos una carga en la tabla antes de calcular.")

    # 2. Reconstruir valores de todas las cargas ingresadas
    cargas_calculadas = [calcular_datos_carga(carga) for carga in lista_cargas_brutas]

    # 3. Calcular totales de potencia del sistema
    totales = calcular_totales(cargas_calculadas)

    # 4. Calcular necesidad de compensación
    comp = necesidad_compensacion(totales, fp_deseado)

    # 5. Calcular capacitador (si se necesita)
    C = 0.0
    if comp["necesita_compensacion"]:
        C = calcular_capacitancia(comp["Qc"], Vlinea, f, config)

    # 6. Retornar el paquete completo a la interfaz
    return {
        "cargas_individuales": cargas_calculadas,
        "totales": totales,
        "Qc": comp["Qc"],
        "necesita_compensacion": comp["necesita_compensacion"],
        "capacitancia_fase": C,
        "fp_deseado": fp_deseado
    }