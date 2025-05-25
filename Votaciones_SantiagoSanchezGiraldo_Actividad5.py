import tkinter as tk
from tkinter import messagebox 
from tkinter import filedialog
import csv 
import matplotlib as mt
import datetime as dt
MainWindow = tk.Tk()
MainWindow.title("Votaciones")
MainWindow.geometry("800x600") 
#Hecho por Santiago Sanchez Giraldo

#---------------Formulario de asistencia votantes------------------
def formulario_asistencia():
    Frame_Asistencia = tk.Toplevel(MainWindow)
    Frame_Asistencia.title("Formulario de Asistencia de los votantes")
    Frame_Asistencia.geometry("300x400")

    campos = ["Cedula", "Salon", "Mesa", "Hora de votacion"]
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
            # Abrimos el archivo en modo append para no sobrescribir
            #"utf-8" es para que el archivo se guarde en un formato que soporte caracteres especiales
            #newline es para que que los salts de linea no se guarden como caracteres especiales
            with open("DatosVotaciones.csv", "a", newline="", encoding="utf-8") as archivo:
                writer = csv.writer(archivo)
                #¨*datos es para que se guarde en una sola fila
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

        messagebox.showinfo("Guardado", "Los datos fueron guardados exitosamente en 'DatosVotaciones.csv'")

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


            

    
#---Abrir el archivo y guardar los datos de los jurados en el archivo csv---
#def Ingresar_Archivo():
    #el defaultextension es para que el sistema operativo sepa que el archivo es un csv y el filetypes es para que el usuario sepa que tipo de archivo en el buscador de archivos.
   # archivo_guardar = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")]) 
   # if not archivo_guardar:
       # messagebox.showerror("Error", "No se seleccionó ningún archivo.")
        #return
    
    
        
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

# ------ Buscar Jurado por cédula -------------------
LabelBuscarJurado = tk.Label(MainWindow, text="Buscar Jurado por Cédula:", font=("Arial", 10, "bold"))
LabelBuscarJurado.grid(row=8, column=0, sticky='e', padx=10, pady=5)    

EntryBuscarJurado = tk.Entry(MainWindow)
EntryBuscarJurado.grid(row=8, column=1, padx=5, pady=5)

BotonBuscarJurado = tk.Button(MainWindow, text="Buscar", font=("Arial", 10, "bold"), command=buscar_jurado, width=10)
BotonBuscarJurado.grid(row=8, column=2, padx=5, pady=5)

# ------ Buscar Votante por cédula -------------------
LabelBuscarVotante = tk.Label(MainWindow, text="Buscar Votante por Cédula:", font=("Arial", 10, "bold"))
LabelBuscarVotante.grid(row=9, column=0, sticky='e', padx=10, pady=5)

EntryBuscarVotante = tk.Entry(MainWindow)
EntryBuscarVotante.grid(row=9, column=1, padx=5, pady=5)

BotonBuscarVotante = tk.Button(MainWindow, text="Buscar", font=("Arial", 10, "bold"), command=buscar_votante, width=10)
BotonBuscarVotante.grid(row=9, column=2, padx=5, pady=5)

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


