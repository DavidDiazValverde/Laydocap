import flet as ft
import formulas
import os
import asyncio

async def logo(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    logo_img = ft.Image(src="logo.png", height=page.height)
    page.add(logo_img)
    page.update()                                                                                                                              
    await asyncio.sleep(1)                                                    
    page.controls.clear()   
    main(page)  # Llama a la función main para mostrar la interfaz principal                                                  
    page.update()
   
    
def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.title = "Parámetros del Sistema"
    #--------------------V_L--------pod---------------------
    texto_V_L = ft.Text(value="Nivel de tensión del sistema (tensión de línea)")
    V_L = ft.TextField(label="Escribe algo aquí")
    
    page.add(texto_V_L, V_L)

    #---------------------F------------------------------
    texto_F = ft.Text(value="Frecuencia del sistema (Hz)")
    F = ft.TextField(label="Escribe algo aquí")
    
    page.add(texto_F, F)
    
    #---------------------F_p-----------------------------
    texto_F_p= ft.Text(value="Factor de potencia deseado")
    F_p = ft.TextField(label="Escribe algo aquí")

    page.add(texto_F_p, F_p)

    #---------------------Banc_Cap-----------------------------
    texto_Banc_Cap = ft.Text(value="Que geometria de banco de capacitores deseas")
    
    def click_estrella(e):
        B_estrella.disabled = True
        B_Delta.disabled = False
        Geometria.value = "Seleccionaste: " + verificacion()
        page.update()
    
    def click_delta(e):
        B_Delta.disabled = True
        B_estrella.disabled = False
        Geometria.value = "Seleccionaste: " + verificacion()
        page.update()

    def verificacion():
        if B_estrella.disabled == True:
            Estado = "Estrella"
           
        elif B_Delta.disabled == True:
            Estado = "Delta"
            
        else:
            Estado = "No seleccionado"
            
        return Estado
        

    B_estrella = ft.Button(content="Estrella", on_click=click_estrella, width=100)
    B_Delta = ft.Button(content="Delta", on_click=click_delta, width=100)
    fila_de_botones = ft.Row( controls=[B_estrella, B_Delta],alignment=ft.MainAxisAlignment.CENTER)
    
    page.add(texto_Banc_Cap,fila_de_botones)
    
    Geometria = ft.Text(value="Seleccionaste: " + verificacion())
    page.add(Geometria)
    #------------------------Variables Finales-----------------
    
    async def calcular_sistema(e):
        try:
            # EXTRAEMOS Y CONVERTIMOS A LAS VARIABLES QUE USARÁS EN TUS FÓRMULAS:
            vl_input = float(V_L.value)
            f_input = float(F.value)
            fp_input = float(F_p.value)
            geometria_input = verificacion()

            if geometria_input == "No seleccionado":
                texto_variables_listas.value = "Selecciones una geometría para el banco de capacitores."
                texto_variables_listas.color = "red"
                page.update()
                return

            if fp_input <= 0 or fp_input > 1:
                texto_variables_listas.value = "El factor de potencia debe estar entre 0 y 1."
                texto_variables_listas.color = "red"
                page.update()
                return
            
            texto_variables_listas.color = "green"
            texto_variables_listas.value = f"Valores ingresados correctamente"
            
            page.update()
            await asyncio.sleep(1)                                                    
            page.controls.clear()   
            resultados(page)  # Llama a la función main para mostrar la interfaz principal                                                  
            page.update()
            
            
        except ValueError:
            # Atrapa errores si el usuario mete letras en los TextField numéricos
            texto_variables_listas.value = "Ingrese valores numéricos válidos para el Voltaje de línea, Frecuencia y Factor de potencia."
            texto_variables_listas.color = "red"
            page.update()

    texto_variables_listas = ft.Text(value="Esperando cálculo...", size=14)
    page.add(texto_variables_listas)

    boton_calcular = ft.Button(content="Calcular", on_click=calcular_sistema, width=120)
    page.add(boton_calcular)

def resultados (page: ft.Page):
    page.title = "Resultados del Sistema"
    #SUMA DE LAS PRIMERAS VARIABLES (PRUEBA)
    #resultado_final = formulas.SumaTotal(vl_input, f_input, fp_input)
    #page.add(ft.Text(value=f"Suma: {resultado_final}"))
    page.add(ft.Text(value="Resultados del sistema calculados aquí."))


if __name__ == "__main__":
    carpeta_recursos = os.path.dirname(__file__)
    ft.app(target=logo, assets_dir=carpeta_recursos)
    
