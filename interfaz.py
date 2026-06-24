import flet as ft
import formulas

def main(page: ft.Page):
    page.title = "Parámetros del Sistema"
    #--------------------V_L-----------------------------
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
    fila_de_botones = ft.Row( controls=[B_estrella, B_Delta])
    
    page.add(texto_Banc_Cap,fila_de_botones)
    
    Geometria = ft.Text(value="Seleccionaste: " + verificacion())
    page.add(Geometria)
    #------------------------Variables Finales-----------------
    
    def calcular_sistema(e):
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
            
    #SUMA DE LAS PRIMERAS VARIABLES (PRUEBA)
            #resultado_final = formulas.SumaTotal(vl_input, f_input, fp_input)
            #page.add(ft.Text(value=f"Suma: {resultado_final}"))
            
            
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
    
ft.run(main)
    



    