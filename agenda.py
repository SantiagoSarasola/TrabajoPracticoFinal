from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem,QMessageBox, QInputDialog
from PyQt5 import uic
import sqlite3

class MiVentana(QMainWindow):    
    
    def __init__(self):
        super().__init__()
        
        #Cargar la interfaz de usuario
        uic.loadUi("./interfaz.ui", self)    
        
        #conectar a la base
        self.conexion = sqlite3.connect('interfaz.db')
        
        #Creación del cursor
        self.cursor = self.conexion.cursor()
        
        # Crear las columnas
        self.tabla.setColumnCount(9)

        # Nombrar las columnas
        self.tabla.setHorizontalHeaderLabels(('Nombre', 'Apellidos', 'Email','Teléfono','Dirección','Fecha Nac','Altura','Peso',"Id"))

        #Al hacer click sobre el botón cargar
        #self.cargar.clicked.connect(self.on_cargar)
        #Mostrar contactos precargados cuando se inicia el programa
        self.on_cargar()
        #Mensaje que surge al iniciar el programa. Dicho mensaje muestra que para editar o eliminar un contacto es necesario seleccionar una fila por su número
        self.mensajeDeAviso()
        
        
        self.nuevo.clicked.connect(self.on_nuevo)  
        self.nuevoOperacion = 0     #Para identificar si se hizo click en agregar nuevo contacto
        self.editar.clicked.connect(self.on_editar)
        self.editarOperacion = 0    #Para identificar si se hizo click en editar contacto
        self.eliminar.clicked.connect(self.on_eliminar)
        
        
    #Función para traer los contactos a la tabla       
    def on_cargar(self):
        
        self.cursor.execute("SELECT * FROM contactos")
        contactos = self.cursor.fetchall()
        self.tabla.setRowCount(0)
        
        for contacto in contactos:
            fila =contactos.index(contacto)
            self.tabla.insertRow(fila)
            self.tabla.setItem(fila,0,QTableWidgetItem(contacto[1]))  #Nombre
            self.tabla.setItem(fila,1,QTableWidgetItem(contacto[2]))  #Apellido 
            self.tabla.setItem(fila,2,QTableWidgetItem(contacto[3]))  #Email
            self.tabla.setItem(fila,3,QTableWidgetItem(contacto[4]))  #Teléfono
            self.tabla.setItem(fila,4,QTableWidgetItem(contacto[5]))  #Dirección
            self.tabla.setItem(fila,5,QTableWidgetItem(contacto[6]))  #FechaNac
            self.tabla.setItem(fila,6,QTableWidgetItem(str(contacto[7])))  #Altura
            self.tabla.setItem(fila,7,QTableWidgetItem(str(contacto[8])))  #Peso
            self.tabla.setItem(fila,8,QTableWidgetItem(str(contacto[0])))  #Id del contacto
            print(list(contacto))
      
    
    #Función para crear un nuevo contacto
    def on_nuevo(self):
        self.habilitarCampos()                          #Habilitamos los campos para poder ser modificados
        self.deshabilitarBotonesEnNuevoEditarEliminar() #Deshabilitamos botones 
        self.nuevoOperacion = 1                         #Esta variable será usada cuando se haga click sobre aceptar o eliminar
        self.cancelar.clicked.connect(self.on_cancelar)
        self.aceptar.clicked.connect(self.on_aceptar)
    
    #Función para editar un nuevo contacto        
    def on_editar(self):
        
        self.habilitarCampos() #Habilitamos los campos para poder ser modificados
        self.deshabilitarBotonesEnNuevoEditarEliminar() #Deshabilitamos botones
        
        #Obtener la fila seleccionada
        contacto = self.tabla.selectedItems()
        
        #Extraer los valores de la fila y colocarlos en variables
        nombre = contacto[0].text()
        apellido = contacto[1].text()
        email = contacto[2].text()
        telefono = contacto[3].text()
        direccion = contacto[4].text()
        fecha = contacto[5].text()
        altura = contacto[6].text()
        peso = contacto[7].text()
        
        #Colocar los valores en los campos, para ser editados
        self.nombre.setText(nombre)
        self.apellidos.setText(apellido)
        self.email.setText(email)
        self.telefono.setText(telefono)
        self.direccion.setText(direccion)
        self.fecha.setText(fecha)
        self.altura.setText(altura)
        self.peso.setText(peso)
        
        self.editarOperacion = 1 #Esta variable será usada cuando se haga click sobre aceptar o eliminar
        self.cancelar.clicked.connect(self.on_cancelar)
        self.aceptar.clicked.connect(self.on_aceptar)
        
    #Función para eliminar un contacto    
    def on_eliminar(self):
        
        self.habilitarCampos()
        self.deshabilitarBotonesEnNuevoEditarEliminar()
        
        #Obtener fila seleccionada
        contacto = self.tabla.selectedItems()
        id = contacto[8].text()
        nroFila = self.tabla.currentRow() + 1
        
        #Creación de mensaje
        mensaje = QMessageBox()
        mensaje.setWindowTitle('Eliminar')
        # "{self.combo.currentText()}
        mensaje.setText(f'¿Está seguro que desea eliminar el usuario con id "{id}", de la fila "{nroFila}" ?')
        
        #Icono mensaje
        mensaje.setIcon(QMessageBox.Question)
        
        #Boton
        mensaje.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        
        resultado = mensaje.exec_()
        if resultado == QMessageBox.Yes:
            self.cursor.execute("DELETE FROM contactos WHERE id ='"+id+"'")
            self.conexion.commit()
            print("Contacto eliminado!")
            self.deshabilitarBotonesAceptarCancelar()
            self.deshabilitarCampos()
            self.limpiarCampos()
            self.eliminarOperacion = 0
            
            #Segundo mensaje
            mensaje2 = QMessageBox()
            mensaje2.setWindowTitle('Eliminación')
            mensaje2.setText("Eliminación del contacto realizada con éxito!")            
            resultado2 = mensaje2.exec_()
        
        if resultado == QMessageBox.No:
            
            self.deshabilitarBotonesAceptarCancelar()
            self.deshabilitarCampos()
            self.limpiarCampos()
            self.eliminarOperacion = 0
            
            #Segundo mensaje
            mensaje2 = QMessageBox()
            mensaje2.setWindowTitle('Eliminación')
            mensaje2.setText("Eliminación del contacto cancelada!")            
            resultado2 = mensaje2.exec_()
        
        self.on_cargar()
        
        
    #Función para aceptar/confirmar una acción
    def on_aceptar(self):
        
        #Para crear contacto
        if self.nuevoOperacion == 1:
            nombres = self.nombre.text()
            apellidos = self.apellidos.text()
            email = self.email.text()
            telefono = self.telefono.text()
            direccion = self.direccion.text()
            fecha = self.fecha.text()
            altura = self.altura.text()
            peso = self.peso.text()
            self.cursor.execute("INSERT INTO contactos(nombres,apellidos,email,telefono,direccion,fecha_nac,altura,peso) VALUES ('"+nombres+"','"+apellidos+"','"+email+"','"+telefono+"','"+direccion+"','"+fecha+"','"+altura+"','"+peso+"')")
            self.conexion.commit()
            print("Creación del contacto realizada con éxito!")
            self.deshabilitarBotonesAceptarCancelar()
            self.deshabilitarCampos()
            self.limpiarCampos()
            self.on_cargar()
            self.nuevoOperacion = 0
            
            #Mensaje para confirmar la acción de cración
            mensaje = QMessageBox()
            mensaje.setWindowTitle('Nuevo contacto')
            mensaje.setText("Creación del contacto realizada con éxito!")            
            resultado = mensaje.exec_()
        
        #Para editar contacto
        if self.editarOperacion == 1:
            nombres = self.nombre.text()
            apellidos = self.apellidos.text()
            email = self.email.text()
            telefono = self.telefono.text()
            direccion = self.direccion.text()
            fecha = self.fecha.text()
            altura = self.altura.text()
            peso = self.peso.text()
            id = self.tabla.selectedItems()[8].text()
            self.cursor.execute("UPDATE contactos SET nombres='"+nombres+"',apellidos='"+apellidos+"',email='"+email+"',telefono='"+telefono+"',direccion='"+direccion+"',fecha_nac='"+fecha+"',altura='"+altura+"',peso='"+peso+"' WHERE id='"+id+"'")
            self.conexion.commit()
            print("Modificación del contacto realizada con éxito!")
            self.deshabilitarBotonesAceptarCancelar()
            self.deshabilitarCampos()
            self.limpiarCampos()
            self.on_cargar()
            self.editarOperacion = 0
            
            #Mensaje para confirmar modificación de usuario
            mensaje = QMessageBox()
            mensaje.setWindowTitle('Modificación')
            mensaje.setText("Modificación del contacto realizada con éxito!")            
            resultado = mensaje.exec_()

        
    #Función para cancelar una acción
    def on_cancelar(self):
        
        #En caso de creación de contacto
        if self.nuevoOperacion == 1:
            print("Se canceló crear nuevo contacto")
            self.deshabilitarBotonesAceptarCancelar()
            self.deshabilitarCampos()
            self.limpiarCampos()
            self.nuevoOperacion = 0 
            
            mensaje = QMessageBox()
            mensaje.setWindowTitle('Creación de contacto')
            mensaje.setText("Creación de contacto cancelada!")            
            resultado = mensaje.exec_()
        
        #En caso de modificación de contacto
        if self.editarOperacion==1:
            print("Se canceló editar contacto")
            self.deshabilitarBotonesAceptarCancelar()
            self.deshabilitarCampos()
            self.limpiarCampos()
            self.editarOperacion = 0
            
            mensaje = QMessageBox()
            mensaje.setWindowTitle('Modificación de contacto')
            mensaje.setText("Modificación de contacto cancelada!")            
            resultado = mensaje.exec_()
        
    #Función para habilitar los campos                 
    def habilitarCampos(self):
        self.nombre.setEnabled(True)
        self.apellidos.setEnabled(True)
        self.email.setEnabled(True)
        self.telefono.setEnabled(True)
        self.direccion.setEnabled(True)
        self.fecha.setEnabled(True)
        self.altura.setEnabled(True)
        self.peso.setEnabled(True)
    
    #Función para deshabilitar los campos
    def deshabilitarCampos(self):
        self.nombre.setEnabled(False)
        self.apellidos.setEnabled(False)
        self.email.setEnabled(False)
        self.telefono.setEnabled(False)
        self.direccion.setEnabled(False)
        self.fecha.setEnabled(False)
        self.altura.setEnabled(False)
        self.peso.setEnabled(False)                           
    
    #Función para limpiar los campos
    def limpiarCampos(self):
        self.nombre.setText("")
        self.apellidos.setText("")
        self.email.setText("")
        self.telefono.setText("")
        self.direccion.setText("")
        self.fecha.setText("")
        self.altura.setText("")
        self.peso.setText("")
            
    #Función para deshabilitar botones cuando se realice una acción de creación, modificación o eliminación de contacto            
    def deshabilitarBotonesEnNuevoEditarEliminar(self):
        self.editar.setEnabled(False)
        self.eliminar.setEnabled(False)
        self.nuevo.setEnabled(False)
        self.aceptar.setEnabled(True)
        self.cancelar.setEnabled(True)
    
    #Función para deshabilitar los botones de aceptar y cancelar
    def deshabilitarBotonesAceptarCancelar(self):
        self.editar.setEnabled(True)
        self.eliminar.setEnabled(True)
        self.nuevo.setEnabled(True)
        self.aceptar.setEnabled(False)
        self.cancelar.setEnabled(False)
              
    def closeEvent(self,event):
        self.conexion.close()    
    
    #Función para mostrar mensaje de aviso al iniciar el programa. El mensaje pide seleccionar 
    # una fila por su número cuando se quiera modificar o eliminar un contacto
    def mensajeDeAviso(self):
        mensaje = QMessageBox()
        mensaje.setWindowTitle('Aviso')
        # "{self.combo.currentText()}
        mensaje.setText("Para realizar operaciones de modificación o eliminación de un contacto es necesario seleccionar una fila haciendo click en su número, de lo contrario el programa provocará un error.")
        resultado = mensaje.exec_()
    

app = QApplication([])

win = MiVentana()
win.show()

app.exec_()

