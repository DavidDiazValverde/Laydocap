import flet as ft

async def crear_seccion_cargas(page: ft.Page, lista_cargas_datos: list):
    page.add(ft.Divider(height=20, color="transparent"))

    page.add(
        ft.Container(
            content=ft.Text(
                "Configuración de Cargas Individuales",
                size=18,
                weight=ft.FontWeight.BOLD,
                color="#005088",
            )
        )
    )

    input_nombre = ft.TextField(
        label="Identificador de Carga (Ej: Motor 1)", width=220, hint_text="Nombre"
    )

    dropdown_param1 = ft.Dropdown(
        label="Parámetro 1", width=160,
        options=[
            ft.dropdown.Option("P", "Activa (P)"),
            ft.dropdown.Option("Q", "Reactiva (Q)"),
            ft.dropdown.Option("S", "Aparente (S)"),
            ft.dropdown.Option("FP", "Factor de Potencia"),
        ],
    )
    input_val1 = ft.TextField(label="Valor 1", width=110)

    dropdown_param2 = ft.Dropdown(
        label="Parámetro 2", width=160,
        options=[
            ft.dropdown.Option("P", "Activa (P)"),
            ft.dropdown.Option("Q", "Reactiva (Q)"),
            ft.dropdown.Option("S", "Aparente (S)"),
            ft.dropdown.Option("FP", "Factor de Potencia"),
        ],
    )
    input_val2 = ft.TextField(label="Valor 2", width=110)

    error_carga = ft.Text(value="", color="red", size=13, weight=ft.FontWeight.W_500)

    tabla_cargas = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID Carga", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Parámetros Ingresados", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Acción", weight=ft.FontWeight.BOLD))
        ],
        rows=[],
    )

    async def agregar_carga_a_tabla(e):
        try:
            nombre = (input_nombre.value or "").strip()
            p1 = dropdown_param1.value
            p2 = dropdown_param2.value
            
            if not nombre or not p1 or not p2 or not input_val1.value or not input_val2.value:
                error_carga.value = "Completa todos los campos."
                page.update() 
                return
            
            if p1 == p2:
                error_carga.value = "Los parámetros deben ser diferentes."
                page.update()
                return

            val1 = float(input_val1.value)
            val2 = float(input_val2.value)

            error_carga.value = "" 

            nombre_carga = nombre  # Guardamos el nombre en una variable separada
            lista_cargas_datos.append({"nombre": nombre, p1.lower(): val1, p2.lower(): val2})


            def eliminar_carga(e, nombre_carga=nombre_carga):
                # Eliminar de la lista de datos por nombre
                for i, carga in enumerate(lista_cargas_datos):
                    if carga.get("nombre") == nombre_carga:
                        lista_cargas_datos.pop(i)
                        break
    
                # Eliminar la fila de la tabla por nombre
                for i, row in enumerate(tabla_cargas.rows):
                    if row.cells[0].content.value == nombre_carga:
                        tabla_cargas.rows.pop(i)
                        break
    
                page.update()

            btn_eliminar = ft.Button(
                content=ft.Text("✕", color="red", size=20, weight=ft.FontWeight.BOLD),
                tooltip="Eliminar carga",
                on_click=eliminar_carga,
                width=100,
                height=40,
            )

            tabla_cargas.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(nombre, weight=ft.FontWeight.W_500)),
                    ft.DataCell(ft.Text(f"{p1}={val1} | {p2}={val2}")),
                    ft.DataCell(btn_eliminar),
                ])
            )

            input_nombre.value = ""
            dropdown_param1.value = None
            dropdown_param2.value = None
            input_val1.value = ""
            input_val2.value = ""
            page.update()

        except ValueError:
            error_carga.value = "Valores numéricos inválidos."
            page.update()

    
    btn_agregar_carga = ft.Button(
        content=ft.Text("Añadir Carga"), 
        on_click=agregar_carga_a_tabla, 
        width=140
    )

    fila_inputs = ft.Row(
        controls=[input_nombre, dropdown_param1, input_val1, dropdown_param2, input_val2, btn_agregar_carga],
        alignment=ft.MainAxisAlignment.START,
        wrap=True,
    )

    page.add(
        ft.Card(
            content=ft.Container(
                content=ft.Column(controls=[fila_inputs, error_carga, tabla_cargas]),
                padding=15
            )
        )
    )