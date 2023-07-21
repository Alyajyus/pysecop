import requests
import pandas as pd
import tkinter as tk
from tkcalendar import DateEntry
import webbrowser

def copiar(event):
    widget = event.widget
    root.clipboard_clear()
    root.clipboard_append(widget.get())

def abrir_url(event, url):
    webbrowser.open(url)

def actualizar_tabla():
    fecha_inicio = cal_inicio.get_date().strftime('%Y-%m-%dT00:00:00.000')
    fecha_fin = cal_fin.get_date().strftime('%Y-%m-%dT23:59:59.999')
    
    # Extraer de departamentos.txt los departamentos
    with open("departamentos.txt") as f:
        departamentos = f.read().splitlines()
    
    # Crear condiciones de departamentos for params1. Un bucle que lee la lista de departamentos para la solicitud SoQL
    departamento_condiciones1 = " OR ".join([f"upper(departamento) like '%{d}%'" for d in departamentos])
    
    # Obtener datos de la 1ra URL
    params1["$where"] = f"({departamento_condiciones1}) AND upper(descripcion_del_proceso) like '%EMPR_STITO%' AND fecha_de_firma between '{fecha_inicio}' and '{fecha_fin}'"
    llamada_api1 = requests.get(url1, params=params1, timeout=None)
    datos1 = llamada_api1.json()
    df1 = pd.DataFrame(datos1)
    
    # Agregar "origen" a df1
    df1['origen'] = 'SECOP II'
    
    # Crear condiciones de departamentos for params2. Un bucle que lee la lista de departamentos para la solicitud SoQL
    departamento_conditions2 = " OR ".join([f"upper(departamento_entidad) like '%{d}%'" for d in departamentos])
    
    # Obtener datos de la 2da URL
    params2["$where"] = f"({departamento_conditions2}) AND upper(detalle_del_objeto_a_contratar) like '%EMPR_STITO%' AND fecha_de_firma_del_contrato between '{fecha_inicio}' and '{fecha_fin}'"
    llamada_api2 = requests.get(url2, params=params2, timeout=None)
    datos2 = llamada_api2.json()
    df2 = pd.DataFrame(datos2)
    
    # Renombrar columnas de df2
    df2 = df2.rename(columns={
        "nit_de_la_entidad": "nit_entidad",
        "departamento_entidad": "departamento",
        "municipio_entidad": "ciudad",
        "detalle_del_objeto_a_contratar": "descripcion_del_proceso",
        "fecha_de_firma_del_contrato": "fecha_de_firma",
        "cuantia_contrato": "valor_del_contrato",
        "ruta_proceso_en_secop_i": "urlproceso"
    })
    
    # Agregar "origen" a df2
    df2['origen'] = 'SECOP I'
    
    # Unir las dos bases
    df_unido = pd.concat([df1, df2], axis=0, ignore_index=True)
    
    for widget in table_frame.winfo_children():
        widget.destroy()
    
    for c, column in enumerate(columnas):
        label = tk.Label(table_frame, text=column)
        label.grid(row=0, column=c)

    for r, row in df_unido.iterrows():
        for c, column in enumerate(columnas):
            value = row[column]
            entry = tk.Entry(table_frame, width=20)
            entry.insert(0, value)
            entry.grid(row=r+1, column=c)
            entry.bind('<Control-c>', copiar)
            if column == 'urlproceso':
                url_dict = value
                url = url_dict['url']
                entry.bind('<Button-1>', lambda event, url=url: abrir_url(event, url))
                entry.config(fg='blue')
root = tk.Tk()
root.title("Filtrador de Contratos SECOP")

table_frame = tk.Frame(root)
table_frame.pack()

cal_label_inicio = tk.Label(root, text="Fecha de inicio:")
cal_label_inicio.pack()
cal_inicio = DateEntry(root)
cal_inicio.pack()

cal_label_fin = tk.Label(root, text="Fecha de fin:")
cal_label_fin.pack()
cal_fin = DateEntry(root)
cal_fin.pack()

update_button = tk.Button(root, text="Actualizar", command=actualizar_tabla)
update_button.pack()

url1 = 'http://www.datos.gov.co/resource/jbjy-vk9h.json'
params1 = {}
columnas1 = ["nombre_entidad", "nit_entidad", "departamento", "ciudad", "descripcion_del_proceso", "fecha_de_firma", "valor_del_contrato", "urlproceso", "origen"]

url2 = 'http://www.datos.gov.co/resource/f789-7hwg.json'
params2 = {}
columnas2 = ["nombre_entidad", "nit_de_la_entidad", "departamento_entidad", "municipio_entidad", "detalle_del_objeto_a_contratar", "fecha_de_firma_del_contrato", "cuantia_contrato", "ruta_proceso_en_secop_i", "origen"]

# Define common column names for the merged dataset
columnas = ["nombre_entidad", "nit_entidad", "departamento", "ciudad", "descripcion_del_proceso", "fecha_de_firma", "valor_del_contrato", "urlproceso", "origen"]

actualizar_tabla()

root.mainloop()