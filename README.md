# Compensación de Factor de Potencia

Aplicación de escritorio desarrollada con Python y Flet para calcular compensación de factor de potencia y dimensionar bancos de capacitores en configuración estrella o delta. Pensada para proyectos de ingeniería eléctrica donde se necesita dimensionar la corrección sin tener que hacer los cálculos manualmente cada vez.

---

## 📁 Estructura del proyecto

```
├── main.py               # Punto de entrada principal
├── interfaz.py           # Interfaz gráfica completa
├── formulas.py           # Cálculos eléctricos
├── tabla_cargas.py       # Componente para agregar cargas
├── logo.png              # Imagen de bienvenida
├── README.md             # Este archivo
```

---

## 🖥️ Requisitos

- Python 3.8 o superior
- Flet 0.85.3 o superior
- NumPy 1.24.0 o superior


## 🚀 Instalación y ejecución

## Forma 1 (mas sencilla)
1. Entra al repositorio https://github.com/DavidDiazValverde/Proyecto-Circuitos
2. Ve a la seccion de releases y selecciona la version mas nueva
3. Selecciona el archivo Laydocap.exe y descargalo
4. Disfruta de la aplicación

## Forma 2 (más extensa, en caso de que la forma 1 falle)

```bash
# Clonar el repositorio
git clone git@github.com:DavidDiazValverde/Proyecto-Circuitos.git
cd Proyecto-Circuitos

# Crear y activar entorno virtual (recomendado)
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependencias
pip install flet numpy

# Ejecutar
python main.py

#o si quieres creer el .exe
pip install pyinstaller
pyinstaller --onefile --noconsole --name="Leydocap" --add-data "logo.png;." main.py
```

---

## 🧮 Cómo usar la aplicación

### 1. Pantalla de bienvenida
Al abrir la aplicación, se muestra el logo durante unos segundos y luego pasa automáticamente a la interfaz principal.

### 2. Parámetros del sistema
Complete los datos básicos:
- **Tensión de línea** (en voltios, mayor a 0)
- **Frecuencia del sistema** (en hercios, mayor a 0)
- **Factor de potencia deseado** (entre 0 y 1)
- **Tipo de conexión** del banco de capacitores (Estrella o Delta)

Cada campo valida la entrada: si el valor es incorrecto muestra un mensaje en rojo; si es válido, en verde.

### 3. Agregar cargas
Cada carga requiere:
- Un nombre (ej: "Motor 1", "Alumbrado")
- Dos parámetros de los cuatro posibles: **P** (potencia activa), **Q** (reactiva), **S** (aparente) o **FP** (factor de potencia)

Con esos datos el programa calcula los valores restantes automáticamente. Puede agregar todas las cargas que necesite y se irán listando en una tabla.

### 4. Calcular
Presione el botón **Calcular**. Si los parámetros son válidos y hay al menos una carga, se realizan los cálculos. En caso contrario, se muestra un mensaje indicando el problema.

### 5. Resultados
La pantalla de resultados muestra:
- Potencias totales del sistema (P, Q, S y factor de potencia actual)
- Compensación necesaria: potencia reactiva (Qc) y capacitancia por fase (en µF) requerida para el banco de capacitores
- Si el sistema ya cumple con el factor de potencia deseado, se informa que no se requiere compensación

Desde esta pantalla puede volver a la vista principal para realizar una nueva simulación.

---

## 📝 Notas

- Los valores de P, Q y S deben ser positivos. El FP debe estar entre 0 y 1.
- Probado en Linux, Windows y macOS.
- Los cálculos utilizan NumPy, por lo que el rendimiento se mantiene incluso con muchas cargas.
- Para cambiar el logo, reemplace el archivo `logo.png` por otro con el mismo nombre y formato.

---

## Acerca del proyecto

Esta aplicación surgió como una herramienta para agilizar los cálculos de compensación de factor de potencia. En lugar de hacer las operaciones a mano cada vez, se ingresan los datos y se obtienen los resultados al instante.

---

Desarrollado por **Santiago Gómez Ramírez, David Díaz Valverde y Luca Fernández Diaz** como parte de un proyecto de Ingeniería Eléctrica en la Universidad de Costa Rica.
