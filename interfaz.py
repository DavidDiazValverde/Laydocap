import flet as ft
import formulas
import os
import asyncio
from  tabla_cargas import crear_seccion_cargas

async def logo(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    logo_img = ft.Image(src="logo.png", height=page.height)
    page.add(logo_img)
    page.update()                                                                                                                              
    await asyncio.sleep(1)                                                    
    page.controls.clear()   
    await main(page)  # Llama a la función main para mostrar la interfaz principal                                                  
    page.update()
   
    
async def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.title = "Parámetros del Sistema"
    #--------------------V_L----------------------------

    def validar_tension(e):
        try:
            valor = float(e.control.value)

            if valor <= 0:
                error_VL.value = "La tensión debe ser mayor a 0V."
                error_VL.color = "red"

            else:
                error_VL.value = "Tensión válida."
                error_VL.color = "green"
                e.control.data = valor

        except ValueError:
            error_VL.value = "Ingrese un valor numérico válido."
            error_VL.color = "red"

        error_VL.update()

    texto_VL = ft.Text(value="Tensión de línea (V)")
    error_VL = ft.Text(value="")
    VL = ft.TextField(label="Escribe algo aquí",on_blur=validar_tension, data=0)

    page.add(texto_VL, VL, error_VL)

    #---------------------F------------------------------
    
    def validar_frecuencia(e):
        try:
            valor = float(e.control.value)
        
            if valor <= 0:
                error_F.value = "La frecuencia debe ser mayor a 0Hz."
                error_F.color = "red"
                
            else:
                error_F.value = "Frecuencia válida." 
                error_F.color = "green"
                e.control.data = valor  # Guardamos el valor validado en el campo de datos
    
            
        except ValueError:
            error_F.value = "Ingrese un valor numérico válido."
            error_F.color = "red"

        error_F.update()

    texto_F = ft.Text(value="Frecuencia del sistema (Hz)")
    F = ft.TextField(label="Escribe algo aquí",on_blur=validar_frecuencia, data=0)
    error_F = ft.Text(value="")

    page.add(texto_F, F, error_F)
    
    #---------------------F_p-----------------------------
        
    def validar_fp(e):
        try:
            valor = float(e.control.value)
        
            if valor <= 0 or valor > 1:
                error_fp.value = "El factor de potencia debe ser un valor entre 0 y 1."
                error_fp.color = "red"
                
            else:
                error_fp.value = "Factor de potencia válido." 
                error_fp.color = "green"
                e.control.data = valor  # Guardamos el valor validado en el campo de datos
    
            
        except ValueError:
            error_fp.value = "Ingrese un valor numérico válido."
            error_fp.color = "red"

        error_fp.update()

    texto_fp = ft.Text(value="Factor de potencia deseado")
    fp = ft.TextField(label="Escribe algo aquí",on_blur=validar_fp, data=0)
    error_fp = ft.Text(value="")

    page.add(texto_fp, fp, error_fp)

    #---------------------Banc_Cap-----------------------------
    
    texto_Banc_Cap = ft.Text(value="Que geometria de banco de capacitores deseas")
    
    def click_estrella(e):
        B_estrella.disabled = True
        B_Delta.disabled = False
        Geometria.value = "Seleccionaste: " + verificacion_geometria()
        page.update()
    
    def click_delta(e):
        B_Delta.disabled = True
        B_estrella.disabled = False
        Geometria.value = "Seleccionaste: " + verificacion_geometria()
        page.update()

    def verificacion_geometria():
        if B_estrella.disabled == True:
            Estado = "estrella"
           
        elif B_Delta.disabled == True:
            Estado = "delta"
            
        else:
            Estado = "No seleccionado"
            
        return Estado
        
    B_estrella = ft.Button(content=ft.Text("Estrella"), on_click=click_estrella, width=100)
    B_Delta = ft.Button(content=ft.Text("Delta"), on_click=click_delta, width=100)
    fila_de_botones = ft.Row(controls=[B_estrella, B_Delta], alignment=ft.MainAxisAlignment.CENTER)
    
    page.add(texto_Banc_Cap, fila_de_botones)
    
    Geometria = ft.Text(value="Seleccionaste: " + verificacion_geometria())
    page.add(Geometria)

#--------------------------Cargas-----------------------------
    lista_cargas_datos = []
    await crear_seccion_cargas(page, lista_cargas_datos)
    page.update()


#-----------------------Boton calcular-----------------

    def verificar(e):
        # 1. Validar que los campos estén correctos
        if (error_VL.value == "Tensión válida." and 
            error_F.value == "Frecuencia válida." and 
            error_fp.value == "Factor de potencia válido."):
        
            # 2. Validar geometría seleccionada
            geometria = verificacion_geometria()
            if geometria == "No seleccionado":
                texto_variables_listas.value = "Por favor, selecciona una geometría (Estrella o Delta)."
                texto_variables_listas.color = "red"
                page.update()
                return

            texto_variables_listas.value = "Todos los parámetros son válidos. Calculando..."
            texto_variables_listas.color = "green"
            page.update()
        
        # 3. Llamar a la función correcta con manejo de excepciones
            try:
                datos_sistema = formulas.procesar_sistema_completo(
                    VL.data,           # tensión de línea
                    F.data,            # frecuencia
                    fp.data,           # fp deseado
                    geometria,         # "estrella" o "delta"
                    lista_cargas_datos # lista de cargas ingresadas
                )
                resultados(page, datos_sistema)
            except Exception as ex:
                texto_variables_listas.value = f"Error en el cálculo: {str(ex)}"
                texto_variables_listas.color = "red"
                page.update()
        else:
            texto_variables_listas.value = "Por favor, corrige los errores antes de calcular."
            texto_variables_listas.color = "red"
            page.update()

    # Botón que usa tu lógica de verificación
    texto_variables_listas = ft.Text(value="")
    boton_calcular = ft.Button(content="Calcular", on_click=verificar)
    page.add(boton_calcular, texto_variables_listas)

#-----------------------Resultados-----------------------------

def resultados(page: ft.Page, datos_sistema: dict):
    page.title = "Resultados del Sistema"
    page.vertical_alignment = ft.MainAxisAlignment.START
    
    totales = datos_sistema["totales"]
    
    # Tarjeta de potencias totales
    tarjeta_totales = ft.Card(
        content=ft.Container(
            padding=20,
            content=ft.Column([
                ft.Text("Potencias Totales del Sistema", size=20, weight=ft.FontWeight.BOLD, color="#005088"),
                ft.Text(f"Potencia Activa (P): {totales['Ptot']:.2f} W"),
                ft.Text(f"Potencia Reactiva (Q): {totales['Qtot']:.2f} VAR"),
                ft.Text(f"Potencia Aparente (S): {totales['Stot']:.2f} VA"),
                ft.Text(f"Factor de Potencia Actual: {totales['fp_act']:.4f}", weight=ft.FontWeight.W_500),
            ])
        )
    )
    
    # Tarjeta de Compensación
    contenido_compensacion = [ft.Text("Análisis de Compensación", size=20, weight=ft.FontWeight.BOLD, color="#005088")]
    
    if datos_sistema["necesita_compensacion"]:
        contenido_compensacion.extend([
            ft.Text("⚠️ El sistema requiere corrección de factor de potencia.", color="red", weight=ft.FontWeight.BOLD),
            ft.Text(f"FP Deseado: {datos_sistema['fp_deseado']}"),
            ft.Text(f"Potencia Reactiva a Inyectar (Qc): {datos_sistema['Qc']:.2f} VAR"),
            ft.Text(f"Capacitancia Requerida por fase: {datos_sistema['capacitancia_fase'] * 1e6:.2f} µF")
        ])
    else:
        contenido_compensacion.append(
            ft.Text("✅ El sistema cumple con el Factor de Potencia deseado. No requiere banco.", color="green", weight=ft.FontWeight.BOLD)
        )

    tarjeta_compensacion = ft.Card(content=ft.Container(padding=20, content=ft.Column(contenido_compensacion)))
    
    # Botón para regresar
    async def volver_inicio(e):
        page.controls.clear()
        await main(page)
        page.update()

    btn_volver = ft.Button(content="Volver", on_click=volver_inicio)

    page.add(
        ft.Row([ft.Text("Reporte Final", size=28, weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(height=20, color="transparent"),
        tarjeta_totales,
        tarjeta_compensacion,
        ft.Divider(height=20, color="transparent"),
        ft.Row([btn_volver], alignment=ft.MainAxisAlignment.CENTER)
    )


if __name__ == "__main__":
    carpeta_recursos = os.path.dirname(__file__)
    # Al usar app=ft.app dentro de run, se mapea correctamente en las nuevas versiones
    ft.run(main=logo, assets_dir=carpeta_recursos)
