import tkinter as tk
from tkinter import messagebox 
from tkinter import filedialog
import csv 
import matplotlib as mt
import datetime as dt
import pandas as pd 
from tkinter import ttk

MainWindow = tk.Tk()
MainWindow.title("Votaciones")
MainWindow.geometry("800x600") 
#Hecho por Santiago Sanchez Giraldo
#---------------Resultado estadisticos--------------------
def mostrar_estadisticas():
    jurados_df = pd.read_csv("jurados.csv")
    votantes_df = pd.read_csv("votantes.csv")
    asistencia_df = pd.read_csv("DatosAsistencia.csv")
    resultados_df = pd.read_csv("ArchivoResultados.csv")  
    
     # Normalizar columnas
    jurados_df.columns = jurados_df.columns.str.strip().str.lower()
    votantes_df.columns = votantes_df.columns.str.strip().str.lower()

    # Limpiar y convertir tipos
    jurados_df['salon'] = jurados_df['salon'].astype(str).str.strip()
    votantes_df['salon'] = votantes_df['salon'].astype(str).str.replace("salon", "").str.strip()

    # Total de jurados por salón
    jurados_por_salon = jurados_df.groupby("salon").size()

    # Total de votantes por salón
    votantes_por_salon = votantes_df.groupby("salon").size()

    # Porcentaje de mesas completas
    total_mesas = 21  # Puedes calcular esto dinámicamente si lo deseas
    mesas_con_jurados = jurados_df.drop_duplicates(subset=["salon", "mesa"]).shape[0]
    porcentaje_mesas = (mesas_con_jurados / total_mesas) * 100 if total_mesas > 0 else 0
    # Número de jurados por mesa
    jurados_por_mesa = jurados_df.groupby(["salon", "mesa"]).size()

    # Limpiar datos si es necesario
   

    # Asegurar que las columnas estén limpias
    # Limpiar nombres de columnas y datos
    asistencia_df.columns = asistencia_df.columns.str.strip().str.lower()
    asistencia_df["salon"] = asistencia_df["salon"].fillna("").astype(str).str.strip()
    asistencia_df["cedula"] = asistencia_df["cedula"].fillna("").astype(str).str.strip()

    # Eliminar duplicados (una asistencia por cedula y salón)
    asistencia_unicos = asistencia_df.drop_duplicates(subset=["cedula", "salon"])

    # Limpiar nombres de columnas y datos
    resultados_df.columns = resultados_df.columns.str.strip().str.lower()

# Convertir todas las respuestas a minúsculas y quitar espacios
    for col in resultados_df.columns:
        if col.startswith("p"):
            resultados_df[col] = resultados_df[col].astype(str).str.strip().str.lower()

# Contar "sí" y "no" por cada pregunta
    resumen_resultados = {}
    for col in resultados_df.columns:
     if col.startswith("p"):
        si_count = (resultados_df[col] == "si").sum()
        no_count = (resultados_df[col] == "no").sum()
        resumen_resultados[col.upper()] = {"Sí": si_count, "No": no_count}
# Contar asistentes únicos por salón
    votantes_por_salon = asistencia_unicos.groupby("salon")["cedula"].count()
    mensaje = "Resumen Estadístico:\n"

    mensaje += "\nTotal de Jurados por Salón:\n"
    for salon, total in jurados_por_salon.items():
        mensaje += f" - Salón {salon}: {total}\n"

    mensaje += "\nNúmero de Jurados por Mesa:\n"
    for (salon, mesa), total in jurados_por_mesa.items():
        mensaje += f" - Salón {salon}, Mesa {mesa}: {total} jurado(s)\n"

    mensaje += "\nTotal de Votantes por Salón:\n"
    for salon, total in votantes_por_salon.items():
        mensaje += f" - Salón {salon}: {total}\n"

    mensaje += "\nPorcentaje de Mesas Completas:\n"
    mensaje += f" - {porcentaje_mesas:.2f}% ({mesas_con_jurados}/{total_mesas} mesas)\n"

    mensaje += "\nAsistencia de Votantes por Salón:\n"
    for salon, total in votantes_por_salon.items():
        mensaje += f" - Salón {salon}: {total} asistidos\n"
    mensaje += "\nResumen de Resultados de Votación:\n"
    for pregunta, conteos in resumen_resultados.items():
        mensaje += f" - {pregunta}: Sí = {conteos['Sí']}, No = {conteos['No']}\n"

    # Mostrar en ventana emergente
    messagebox.showinfo("Resumen Estadístico", mensaje)


#---------------Resultados preguntas--------------------
def cargar_resultados_desde_csv():
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo CSV de resultados",
        filetypes=[("Archivos CSV", "*.csv")]
    )
    if not archivo:
        messagebox.showerror("Error", "No se seleccionó ningún archivo.")
        return  # El usuario canceló

    try:
        with open(archivo, "r", encoding="utf-8") as f:
            lector = csv.DictReader(f)
            encabezados_esperados = ["salon", "mesa", "tarjeton"] + [f"p{i}" for i in range(1, 10)]

            # Verifica que los encabezados del archivo sean los esperados
            if lector.fieldnames != encabezados_esperados:
                messagebox.showerror(
                    "Error",
                    f"Encabezados incorrectos.\nSe esperaban:\n{', '.join(encabezados_esperados)}\n"
                    f"Se encontraron:\n{', '.join(lector.fieldnames)}"
                )
                return
            ##########################   
            resultados = [fila for fila in lector]  # Lista con todos los resultados

            messagebox.showinfo("Éxito", f"Se cargaron {len(resultados)} resultados correctamente.")
            # Aquí puedes procesar o guardar los resultados en tu programa si es necesario

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo leer el archivo CSV: {e}")
    
#---------------Formulario de asistencia votantes------------------
def formulario_asistencia():
    Frame_Asistencia = tk.Toplevel(MainWindow)
    Frame_Asistencia.title("Formulario de Asistencia de los votantes")
    Frame_Asistencia.geometry("300x400")

    campos = ["Cedula del votante", "Salon", "Mesa", "Hora de votacion(HH:MM,24h)"]
    entradas = []

    for campo in campos:
        label = tk.Label(Frame_Asistencia, text=f"{campo}:")
        label.pack()
        entryF = tk.Entry(Frame_Asistencia)
        entryF.pack()
        entradas.append(entryF)

    def guardar_asistencia():
        datos = [entry.get() for entry in entradas]
        
        # Verificar que ningún campo esté vacío
        if any(dato.strip() == "" for dato in datos):
            messagebox.showerror("Error", "Todos los campos deben estar llenos.")
            return
        cedula_ingresada = datos[0].strip()
        mesa_ingresada = datos[2].strip()
        salon_ingresada = datos[1].strip()
        #Verificar que la cedula 
        existe_votante = any(v["cedula"]== cedula_ingresada for v in votantes)
        if not existe_votante:
            messagebox.showerror("Error", "La cédula ingresada no corresponde a un votante registrado.")
            return
        # Verificar que la cédula sea un número entero
        if not cedula_ingresada.isdigit():
            messagebox.showerror("Error", "La cédula debe ser un número entero.")
            return
        #verifica si el salon es un número entero
        if not salon_ingresada.replace(" ", "").isdigit():
            messagebox.showerror("Error", "El salón debe ser un número entero.")
            return
        #verifica si la mesa es un número entero
        if not mesa_ingresada.replace(" ", "").isdigit():
            messagebox.showerror("Error", "La mesa debe ser un número entero.")
            return
        

        hora_escrita= datos[3]
        # Verificar que la hora de votación sea válida
        try:
            hora_votacion = dt.datetime.strptime(hora_escrita, "%H:%M").time()
        #HH es para que la hora sea en formato de 24 horas y MM es para que los minutos sean en formato de 60 minutos
        except ValueError:
            messagebox.showerror("Error", "La hora de votación debe estar en formato HH:MM en formato de 24 horas.")
        hora_minima = dt.time(16,0) # 4:00 pm

        if hora_votacion > hora_minima:
            messagebox.showerror("Error", "La hora de votación no puede ser antes de las 4:00 PM.")
            return
        
        # si en el caso de que sea la hora correcta, se guardará en un archivos csv
        try:
            escribir_encabezado = True
    # Verificar si el archivo ya existe y tiene contenido
            try:
                with open("DatosAsistencia.csv", "r", encoding="utf-8") as archivo_lectura:
                    primera_linea = archivo_lectura.readline()
                    if primera_linea.strip():  # si hay algo escrito en la primera línea
                        escribir_encabezado = False
            except FileNotFoundError:
        # El archivo no existe aún, así que sí escribimos encabezado
                escribir_encabezado = True

    # Abrimos en modo append
            with open("DatosAsistencia.csv", "a", newline="", encoding="utf-8") as archivo:
                writer = csv.writer(archivo)
                if escribir_encabezado:
                    writer.writerow(["tipo", "cedula", "salón", "mesa", "hora"])
                writer.writerow(["Asistencia", *datos])

            messagebox.showinfo("Éxito", "Asistencia registrada correctamente.")
            Frame_Asistencia.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la asistencia: {e}")

    boton_guardar = tk.Button(Frame_Asistencia, text="Guardar Asistencia", command=guardar_asistencia)
    boton_guardar.pack(pady=10)
#---------------Guarda en un archivo los datos de los jurados en csv------------------
def guardaDatosVotaciones():
    try:
        with open("DatosVotaciones.csv", "w", newline="", encoding="utf-8") as archivo:
            writer = csv.writer(archivo)

            # Datos generales sobre el centro de votación
            writer.writerow(["------------Centro de Votación-----------\n"])
            writer.writerow(["Cantidad de Salones", entry_salon.get()])
            writer.writerow(["Cantidad de Mesas por Salón", entry_mesas.get()])
            writer.writerow(["Cantidad de Jurados por Mesa", entry_jurados.get()])
            writer.writerow([])
            
            # Datos de jurados por mesa
            writer.writerow(["---------Jurados por Mesa--------\n"])
            writer.writerow(["---------Mesa,Nombre,Cedula,Telefono,Direccion--------\n"])
            for i, jurados in enumerate(jurados_por_mesa):
                for jurado in jurados:
                    writer.writerow([f"Mesa {i+1}", jurado[0], jurado[1], jurado[2], jurado[3]])
            writer.writerow([])

            # Datos de votantes
            writer.writerow(["-----------Votantes---------\n"])
            
            for v in votantes:
                writer.writerow([v["nombre"], v["cedula"], v["salon"], v["mesa"]])

       # Archivos separados y tabulares para pandas:

        # Guardar jurados.csv
        with open("jurados.csv", "w", newline="", encoding="utf-8") as jurado_file:
            jurado_writer = csv.writer(jurado_file)
            jurado_writer.writerow(["salon", "mesa", "nombre", "cedula", "telefono", "direccion"])
            for mesa_index, jurados in enumerate(jurados_por_mesa):
                salon = mesa_index // int(entry_mesas.get()) + 1  # Calcula salón según index
                mesa = mesa_index % int(entry_mesas.get()) + 1
                for jurado in jurados:
                    jurado_writer.writerow([salon, mesa, jurado[0], jurado[1], jurado[2], jurado[3]])

        # Guardar votantes.csv
        with open("votantes.csv", "w", newline="", encoding="utf-8") as votantes_file:
            votante_writer = csv.writer(votantes_file)
            votante_writer.writerow(["nombre", "cedula", "salon", "mesa"])
            for v in votantes:
                votante_writer.writerow([v["nombre"], v["cedula"], v["salon"], v["mesa"]])

        

        messagebox.showinfo("Guardado", "Los datos fueron guardados exitosamente en múltiples archivos CSV.")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")

##---Abrir el archivo y guardar los datos de los votantes en el archivo csv---
votantes = []  # Lista global para guardar los votantes

def cargar_votantes():
    archivo = filedialog.askopenfilename(title="Seleccionar archivo de votantes", filetypes=[("CSV files", "*.csv")])
    if not archivo:
        messagebox.showerror("Error", "No se seleccionó ningún archivo.")
        return
    try:
        #utf-8 es para que el archivo se guarde en un formato que soporte caracteres especiales
        with open(archivo, newline='', encoding='utf-8') as f: #newline es para que que los salts de linea no se guarden como caracteres especiales
            #La f es para que el archivo se cierre automaticamente al terminar de usarlo y tambien para que no se guarde en la memoria, solo sea temporal
            lector = csv.reader(f)
            next(lector, None)
            votantes.clear()
            for fila in lector:
                if len(fila) >= 4:
                    votantes.append({
                        "nombre": fila[0],
                        "cedula": fila[1], 
                        "salon":fila[2],  
                        "mesa":  fila[3]  # Se asume que columna 4 indica número de mesa
                    })
        messagebox.showinfo("Carga exitosa", "Votantes cargados correctamente.")

    #except es para capturar errores si el usuario no ingresa un valor no deseado.
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el archivo: {e}")
#######################
def buscar_votante():
    
    cedula=EntryBuscarVotante.get()

    for votante in votantes:
        if votante["cedula"] == cedula:
            messagebox.showinfo("Votante encontrado", f"Nombre: {votante['nombre']}\nCédula: {votante['cedula']}\nSalon: {votante['salon']}\nMesa: {votante['mesa']}")
            return
      
    if cedula =="":
        messagebox.showerror("Error", "Por favor, ingrese una cédula o valor numerico.")

    if not votante in votantes:
        # Si la cédula no se encuentra en la lista de votantes
        messagebox.showerror("Error", "No existe ningún votante con la cédula ingresada.")
        return    
    messagebox.showerror("Error", "No existe ningún jurado con la cédula ingresada.")

def buscar_jurado():
    cedulajurado = EntryBuscarJurado.get().strip()
    
    if cedulajurado == "":
        messagebox.showerror("Error", "Por favor, ingrese la cédula del jurado.")
        return  # Para que no siga ejecutándose
    
    # Buscar jurado con esa cédula
    for jurado in Datos_Jurado:
        if jurado[1] == cedulajurado:
            messagebox.showinfo(
                "Jurado encontrado", 
                f"Nombre: {jurado[0]}\nCédula: {jurado[1]}\nSalón: {jurado[4]}\nMesa: {jurado[5]}"
            )
            return
    if not jurado in Datos_Jurado:
        # Si la cédula no se encuentra en la lista de jurados
        messagebox.showerror("Error", "No existe ningún jurado con la cédula ingresada.")
        return
    # Si no se encontró, mostrar error
    messagebox.showerror("Error", "No existe ningún jurado con la cédula ingresada.")      
     
        
# ------ Guardar centro de votación -------------------
BotonGuardarCentro = tk.Button(MainWindow, text="Guardar centro de votacion", font=("Arial", 10, "bold"), command=guardaDatosVotaciones, width=25)
BotonGuardarCentro.grid(row=4, column=0, columnspan=2, pady=10)

# ------ Cargar Centro de votación -------------------
BotonCargarVotacion = tk.Button(MainWindow, text="Cargar Centro de votacion", font=("Arial", 10, "bold"), width=25)
BotonCargarVotacion.grid(row=5, column=0, columnspan=2, pady=10)

# ------ Cargar los datos de los votantes -------------------
BotonCargarVotantes = tk.Button(MainWindow, text="Cargar Datos votantes", font=("Arial", 10, "bold"), command=cargar_votantes, width=25)
BotonCargarVotantes.grid(row=6, column=0, columnspan=2, pady=10)

# ------ Botón del formulario de asistencia -------------------
BotonAsistencia = tk.Button(MainWindow, text="Formulario de Asistencia", font=("Arial", 10, "bold"), width=25, command=formulario_asistencia)
BotonAsistencia.grid(row=7, column=0, columnspan=2, pady=10)

# ------ Botón para mostrar resultados de las preguntas -------------------
BotonResultadosPreguntas = tk.Button(MainWindow, text="Cargar resultados desde CSV", font=("Arial", 10, "bold"), command=cargar_resultados_desde_csv, width=25)
BotonResultadosPreguntas.grid(row=8, column=0, columnspan=2, pady=10)

# ------ Botón para mostrar estadísticas -------------------
BotonResultadoEstadisticos = tk.Button(MainWindow, text="Mostrar Estadísticas",command=mostrar_estadisticas, font=("Arial", 10, "bold"), width=25)
BotonResultadoEstadisticos.grid(row=9, column=0, columnspan=2, pady=10)

# ------ Buscar Jurado por cédula -------------------eeeeeee
LabelBuscarJurado = tk.Label(MainWindow, text="Buscar Jurado por Cédula:", font=("Arial", 10, "bold"))
LabelBuscarJurado.grid(row=10, column=0, sticky='e', padx=10, pady=5)    

EntryBuscarJurado = tk.Entry(MainWindow)
EntryBuscarJurado.grid(row=10, column=1, padx=5, pady=5)

BotonBuscarJurado = tk.Button(MainWindow, text="Buscar", font=("Arial", 10, "bold"), command=buscar_jurado, width=10)
BotonBuscarJurado.grid(row=10, column=2, padx=5, pady=5)

# ------ Buscar Votante por cédula -------------------
LabelBuscarVotante = tk.Label(MainWindow, text="Buscar Votante por Cédula:", font=("Arial", 10, "bold"))
LabelBuscarVotante.grid(row=11, column=0, sticky='e', padx=10, pady=5)

EntryBuscarVotante = tk.Entry(MainWindow)
EntryBuscarVotante.grid(row=11, column=1, padx=5, pady=5)

BotonBuscarVotante = tk.Button(MainWindow, text="Buscar", font=("Arial", 10, "bold"), command=buscar_votante, width=10)
BotonBuscarVotante.grid(row=11, column=2, padx=5, pady=5)


# ------------------ Lista de listas para guardar jurados por mesa ------------------
# Cada sublista representa una mesa, y contiene listas con los datos de los jurados
jurados_por_mesa = []  

# ------------------ Contenedor donde se mostrarán los salones ------------------
ContenedorSalon = tk.Frame(MainWindow)
ContenedorSalon.grid(row=14, column=0, columnspan=2, pady=20)

# ------------------ Función para mostrar jurados de una mesa específica ------------------

def mostrar_datos_jurados(indice_mesa):
    jurados = jurados_por_mesa[indice_mesa]

    if not jurados:
        messagebox.showerror("Error", "No hay jurados registrados para esta mesa.")
        return

    # Calcular el salón y número de mesa real
    total_mesas = int(entry_mesas.get())
    #salon_num es el número del salón y mesa_num es el número de la mesa
    #indice_mesa es el índice de la mesa en la lista jurados_por_mesa
   
    salon_num = (indice_mesa // total_mesas) + 1
    mesa_num = (indice_mesa % total_mesas) + 1  #total_mesas es el número total de mesas por salón

    SalidaTexto = ""

    for i, jurado in enumerate(jurados):
        SalidaTexto += f"Jurado #{i+1}:\nNombre: {jurado[0]}\nCédula: {jurado[1]}\nTeléfono: {jurado[2]}\nDirección: {jurado[3]}\n\n"

    nombre_mesa = f"mesa {mesa_num}"
    # Filtrar votantes por mesa Y salón
    votantes_en_mesa = [v for v in votantes 
                        if v["mesa"].strip().lower() == nombre_mesa 
                        and v["salon"].strip().lower() == f"salon {salon_num}"]

    if not votantes_en_mesa:
        SalidaTexto += "--- No hay votantes asignados a esta mesa ---"
    else:
        SalidaTexto += "--- Votantes ---\n"
        for v in votantes_en_mesa:
            SalidaTexto += f"Nombre: {v['nombre']}\nCédula: {v['cedula']}\n\n"

    messagebox.showinfo(f"Datos del Salón {salon_num} - Mesa {mesa_num}", SalidaTexto)

# ------------------ Función para guardar datos del jurado ------------------
Datos_Jurado = []  # Lista para guardar los datos del jurado

def guardar_datos(entradas, Frame_Formulario, indice_mesa): #Se añade el indice de la mesa para guardar los datos de la mesa correcta
    Datos_Guardados = []
    total_mesas = int(entry_mesas.get())
    salon_num = (indice_mesa // total_mesas) + 1
    mesa_num = (indice_mesa % total_mesas) + 1
    direccion = entradas[3].get()

    # Verifica si los campos están vacíos
    for entry in entradas:
        if entry.get() == "":
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
            return 
    #.replace(" ", "") es para eliminar los espacios en blanco y hace que .isalnum() solo verifique letras y números  
    if not direccion.replace(" ", "").isalnum():
        messagebox.showerror("Error", "La dirección no puede contener caracteres especiales, solo letras, números y espacios.")
        return
    #.isdigit() verifica si la cadena contiene solo dígitos, si no es así, se muestra un mensaje de error
    if direccion.isdigit():
        messagebox.showerror("Error", "La dirección no puede ser solo números.")
        return
    #.isalpha() verifica si la cadena contiene solo letras, si no es así, se muestra un mensaje de error
    if not entradas[0].get().isalpha():
        messagebox.showerror("Error", "Por favor, ingrese solo letras en el nombre.")
        return
    #.isdigit() verifica si la cadena contiene solo dígitos, si no es así, se muestra un mensaje de error
    if not entradas[1].get().isdigit():
        messagebox.showerror("Error", f"Por favor, ingrese solo números enteros válidos en la cédula.")
        return
    if not entradas[2].get().isdigit():
        messagebox.showerror("Error", "Por favor, ingrese solo números enteros válidos en el telefono.")
        return
           

    for entry in entradas:
        Datos_Guardados.append(entry.get()) 

    jurados_por_mesa[indice_mesa].append(Datos_Guardados)  #Se guarda en la lista correspondiente 

    Datos_Jurado.append(Datos_Guardados + [f"salon {salon_num}", f"mesa {mesa_num}"])  # Se guarda en la lista de jurados

    label = tk.Label(Frame_Formulario, text="Los datos han sido guardados correctamente")
    label.pack(pady=10)

# ------------------ Formulario de jurado ------------------
def formulario_Jurado(indice_mesa):  #recibe el índice de la mesa
    Frame_Formulario = tk.Toplevel(MainWindow)
    Frame_Formulario.title(f"Formulario Jurado - Mesa {indice_mesa + 1}")
    Frame_Formulario.geometry("300x400")

    campos = ["Nombre", "Cédula", "Teléfono", "Dirección"]
    entradas = [] 

    for campo in campos:
        #Escoge cada campo para poder que aparezca en el formulario
        #label es el texto que aparece en el formulario
        label = tk.Label(Frame_Formulario, text=f"{campo}:")
        label.pack()
        entryF = tk.Entry(Frame_Formulario)
        entryF.pack()
        entradas.append(entryF)

    boton_guardar = tk.Button(Frame_Formulario, text="Guardar", command=lambda: guardar_datos(entradas, Frame_Formulario, indice_mesa))
    boton_guardar.pack(pady=10)

# ------------------ Genera los salones, mesas y jurados ------------------
def generar_votacion():
    #winfo_children() elimina todos los widgets dentro del contenedor
    # Esto es útil para limpiar el contenedor antes de crear nuevos salones y mesas
    for Eliminar in ContenedorSalon.winfo_children():
        Eliminar.destroy()
    #try sirve para evitar errores si el usuario no ingresa un valor
    try:
        total_salones = int(entry_salon.get())
        total_mesas = int(entry_mesas.get())
        total_jurados = int(entry_jurados.get())
    #except sirve para capturar errores si el usuario no ingresa un valor no deseado.
    except ValueError:
        messagebox.showerror("Error", "Por favor ingrese solo números enteros válidos.")
        return  # Termina la función si ocurre error

    jurados_por_mesa.clear()  #limpiamos jurados por mesa
    total_mesas_totales = total_salones * total_mesas
    for _ in range(total_mesas_totales):
        jurados_por_mesa.append([])  #una lista vacia por mesa

    indice_mesa_global = 0  #variable global para guardar el indice de la mesa

    for i in range(total_salones):
        frame_salon = tk.LabelFrame(ContenedorSalon, text=f"Salón {i+1}", padx=10, pady=10)
        frame_salon.grid(padx=10, pady=10, column="2", row=i) 
#
        for m in range(total_mesas):
            frame_mesa = tk.Frame(frame_salon)
            frame_mesa.pack(pady=2)

            #mesa muestra solos sus jurados
            #index es para guardar el indice de la mesa
            btn_mesa = tk.Button(frame_mesa, text=f"Mesa {m+1}", width=10, command=lambda index=indice_mesa_global: mostrar_datos_jurados(index))
            btn_mesa.pack(side="left", padx=5)

            for j in range(total_jurados):
                # boton para abrir el formulario del jurado cuando le de a la mesa
                btn_jurado = tk.Button(frame_mesa, text=f"Jurado {j+1}", width=10, command=lambda index=indice_mesa_global: formulario_Jurado(index))
                btn_jurado.pack(side="left", padx=2)

            indice_mesa_global += 1  # aumentamos el indice de la mesa
# ------------------ Widgets de Entrada Principal ------------------

# ------------------ Salón --------------------
tk.Label(MainWindow, text="Numero de salones:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky='e', padx=10, pady=5)
entry_salon = tk.Entry(MainWindow)
entry_salon.grid(row=0, column=1, padx=10, pady=5)

# ------------------ Mesas --------------------
tk.Label(MainWindow, text="Numero de Mesas por Salón:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky='e', padx=10, pady=5)
entry_mesas = tk.Entry(MainWindow)
entry_mesas.grid(row=1, column=1, padx=10, pady=5)

# ------------------ Jurados --------------------

tk.Label(MainWindow, text="Numero de Jurados por Mesa:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky='e', padx=10, pady=5)
entry_jurados = tk.Entry(MainWindow)
entry_jurados.grid(row=2, column=1, padx=10, pady=5)

# # ------------------ Botón --------------------

boton = tk.Button(MainWindow, text="Generar Centro de Votación", command=generar_votacion, font=("Arial", 10, "bold"), width=25)
boton.grid(row=3, column=0, columnspan=2, pady=20)

MainWindow.mainloop()

#Hecho por Santiago Sanchez Giraldo


