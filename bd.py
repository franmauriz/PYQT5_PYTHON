import sys
import shutil,os
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QFileDialog
from PyQt5 import uic
from PyQt5.QtCore import QDir
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

class Dialogo(QDialog):
		def __init__(self):
			QDialog.__init__(self)
			uic.loadUi('bd.ui',self)
			self.btnconectar.clicked.connect(self.conectar)
			self.btnabrir.clicked.connect(self.abrirFichero)
			self.btncrear.clicked.connect(self.crearTabla)
			self.btnBorrar.clicked.connect(self.borrarTabla)
			self.btnTruncar.clicked.connect(self.truncarTabla)
			self.btncargar.clicked.connect(self.cargarTabla)
			self.btndesconectar.clicked.connect(self.desconectar)

		def conexion(self):
			base=self.combobd.currentText()
			self.db = QSqlDatabase.addDatabase('QMYSQL')
			self.db.setHostName("localhost")
			self.db.setDatabaseName(str(base).lower())
			self.db.setUserName("root")
			self.db.setPassword("frandaniel10")
			estado = self.db.open()
			if estado == True:
				return True
			else:
				return False

		def desconectar(self):
			if self.conexion():
				QMessageBox.information(self,"Conexión","Se ha desconectado de " + self.combobd.currentText(),QMessageBox.Ok)
				self.db.close()
				self.cajaTabla.setEnabled(False)
				self.btncrear.setEnabled(False)
				self.btnBorrar.setEnabled(False)
				self.btnTruncar.setEnabled(False)
				self.btnabrir.setEnabled(False)
				self.btncargar.setEnabled(False)
				self.comboTabla.clear()

		def conectar(self):
			if self.conexion() :
				QMessageBox.information(self,"Conexión","Se ha conectado a " + self.combobd.currentText(),QMessageBox.Ok)
				self.rellenarComboTabla()
				if self.combobd.currentText() != "Lote6_ri":
					self.cajaTabla.setEnabled(True)
					self.btncrear.setEnabled(True)
					self.btnBorrar.setEnabled(True)
					self.btnTruncar.setEnabled(True)
					self.btnabrir.setEnabled(True)
					self.btncargar.setEnabled(True)
				else:
					self.cajaTabla.setEnabled(False)
					self.btncrear.setEnabled(False)
					self.btnBorrar.setEnabled(True)
					self.btnTruncar.setEnabled(True)
					self.btnabrir.setEnabled(True)
					self.btncargar.setEnabled(True)
			else:
				QMessageBox.information(self,"Error","No se puede conectar con la base de datos.",QMessageBox.Cancel)
				self.db.close()

		def abrirFichero(self):
			file, _ = QFileDialog.getOpenFileName(self, 'Buscar Archivo', QDir.homePath(), "All Files (*);;Text Files (*.txt)")
			if file:
				self.nombreFichero.setText(file)
				origen=self.nombreFichero.text()
				fich=self.nombreFichero.text().split('/')
				fichero = fich[len(fich)-1]
				destino='/var/lib/mysql/'+self.combobd.currentText().lower()+'/'+fichero
				if os.path.exists(origen):
					with open(origen, 'rb') as forigen:
						with open(destino, 'wb') as fdestino:
							shutil.copyfileobj(forigen, fdestino)
							QMessageBox.information(self, "Correcto", "Fichero preparado para ser Cargado.", QMessageBox.Ok)

		def rellenarComboTabla(self):
			self.comboTabla.clear()		
			#SHOW FULL TABLES FROM mi_base_de_datos
			sql = "SHOW FULL TABLES FROM " + self.combobd.currentText().lower() + " WHERE Table_type='BASE TABLE'"
			#print(sql)
			query = QSqlQuery(sql)
			while query.next():
				self.comboTabla.addItem(str(query.value(0)))

		def closeEvent(self,event):
			resultado = QMessageBox.question(self,"Salir","¿Seguro que quieres salir de la aplicación?",QMessageBox.Yes|QMessageBox.No)
			if resultado == QMessageBox.Yes:
				event.accept()
				self.db.close()
			else:
				event.ignore()

		def crearTabla(self):				
			if self.cajaTabla.text() != '':
				consulta = QSqlQuery()
				if self.combobd.currentText().lower()=='lote6':					
					sql = "CREATE TABLE "+ self.cajaTabla.text() +" ("
					sql = sql +"ID varchar(100), "
					sql = sql + "COD_LOTE_SA varchar(10), "
					sql = sql +"NUMERO_PREFACTURA varchar(100), "
					sql = sql +"CICLO_FACTURADO varchar(100), "
					sql = sql +"COD_CENTRO_FACTURACION varchar(100), "
					sql = sql +"DESC_CENTRO_FACTURACION varchar(300), "
					sql = sql +"CIF varchar(20), "
					sql = sql +"COD_SEDE varchar(30), "
					sql = sql +"CODIGO_CONCEPTO varchar(100), "
					sql = sql +"NOMBRE_CONCEPTO varchar(150), "
					sql = sql +"SERVICIO varchar(100), "
					sql = sql +"TELEFONO varchar(100), "
					sql = sql +"EXTENSION varchar(100), "
					sql = sql +"NUMERO_ADMINISTRATIVO varchar(100), "
					sql = sql +"TICKET_SIO varchar(100), "
					sql = sql +"FECHA_ALTA varchar(100), "
					sql = sql +"FECHA_BAJA varchar(100), "
					sql = sql +"FECHA_INICIO_AMORTIZACION varchar(100), "
					sql = sql +"IMPORTE varchar(100), "
					sql = sql +"UNIDADES varchar(100));"				
				elif self.combobd.currentText().lower()=='pasarela' :
					Sql = "CREATE TABLE "+ self.cajaTabla.text() +"( "
					Sql = Sql + "DNTV_CAB varchar(255), "
					Sql = Sql + "CICLO varchar(255), "
					Sql = Sql + "FACT_NO varchar(255), "
					Sql = Sql + "TELEF_EXT varchar(255), "
					Sql = Sql + "FECHA_HORA varchar(255), "
					Sql = Sql + "NO_RECEP varchar(255), "
					Sql = Sql + "TIPO varchar(255), "
					Sql = Sql + "DESTINO varchar(255), "
					Sql = Sql + "DURACION varchar(255), "
					Sql = Sql + "DURAC_SES varchar(255), "
					Sql = Sql + "VOLUMEN varchar(255), "
					Sql = Sql + "TIPO_FACT varchar(255), "
					Sql = Sql + "TARIFA varchar(255), "
					Sql = Sql + "DESCRIPCION varchar(255), "
					Sql = Sql + "CANAL varchar(255), "
					Sql = Sql + "EXT_ORIGEN varchar(255), "
					Sql = Sql + "IMPORTE varchar(255), "
					Sql = Sql + "IMPORTE_NETO varchar(255));"

				estado = consulta.exec(sql)
				if estado == True:
					QMessageBox.information(self, "Correcto", "Tabla creada con éxito.", QMessageBox.Ok)
					self.rellenarComboTabla()
				else:
					QMessageBox.warning(self, "Error", self.db.lastError().text(), QMessageBox.Discard)
			else:
				QMessageBox.warning(self, "Error", "El nombre de la tabla a crear no esta informado.", QMessageBox.Discard)
		
		def borrarTabla(self):
			consulta = QSqlQuery()
			tabla  = self.comboTabla.currentText()
			sql    = "DROP TABLE IF EXISTS "+tabla+" ;"
			estado = consulta.exec(sql)
			if estado == True:
				QMessageBox.information(self, "Correcto", "Tabla borrada con éxito.", QMessageBox.Ok)
				self.rellenarComboTabla()
			else:
				QMessageBox.warning(self, "Error", self.db.lastError().text(), QMessageBox.Discard)		

		def truncarTabla(self):
			consulta = QSqlQuery()
			tabla  = self.comboTabla.currentText()
			sql    = "TRUNCATE TABLE "+tabla+" ;"
			estado = consulta.exec(sql)
			if estado == True:
				QMessageBox.information(self, "Correcto", "Tabla vaciada con éxito.", QMessageBox.Ok)
				self.rellenarComboTabla()
			else:
				QMessageBox.warning(self, "Error", self.db.lastError().text(), QMessageBox.Discard)			

		def cargarTabla(self):
			self.labelestado.setText("Cargando...")
			fich    = self.nombreFichero.text().split('/')
			self.nombreFichero.setText("")			
			fichero = fich[len(fich)-1]			
			consulta = QSqlQuery()
			#os.system('cp "'+ self.nombreFichero.text() +'" /var/lib/mysql/'+self.combobd.currentText().lower()+'/')
			sql='load data infile "'+fichero+'" into table '+ self.comboTabla.currentText() +' fields terminated by ";" ignore 1 lines;'			
			estado = consulta.exec(sql)			
			if estado == True:
				self.labelestado.setText("Cargado.")
				os.system('rm /var/lib/mysql/'+self.combobd.currentText().lower()+'/'+ fichero)
				QMessageBox.information(self, "Correcto", "Fichero Cargado.", QMessageBox.Ok)				
			else:
				QMessageBox.warning(self, "Error", self.db.lastError().text(), QMessageBox.Discard)			

#instnacia para iniciar la aplicacion (obligatorio)
app = QApplication(sys.argv)
#crearun objeto de la clase Ventana
_ventana = Dialogo()
#Mostrar la ventana
_ventana.show()
#Ejecutar la aplicación
sys.exit(app.exec_())
