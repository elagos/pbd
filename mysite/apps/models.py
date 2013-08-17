# -*- coding: utf-8 -*-

from django.db import models
from django.forms import ModelForm
from django.core.files.storage import FileSystemStorage

CHOICES = (
    (True, "Si"),
    (False, "No")
)

#Tabla Productos
class Producto(models.Model):
	nombre_produc = models.CharField("nombre producto",max_length = 200, blank = False)
	destacado = models.BooleanField("¿Es producto destacado?",choices = CHOICES)

	def __unicode__(self):
		return self.nombre_produc

#OJOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO FALTA VALIDAR QUE CANTIDAD SEA POSITIVA!!!
#Tabla de los abastecimientos de productos
class Abastecimiento(models.Model):
	producto_abast = models.ForeignKey(Producto, related_name = 'abast_producto', verbose_name = "Producto a ingresar")
	cant_abast = models.IntegerField("cantidad") 
	fecha = models.DateTimeField("fecha")

	def __unicode__(self):
		return u'%s %s %s' % (self.cant_abast, self.fecha, self.producto_abast)

#Tabla de equipos armados. Hereda nombre_produc
class EquipoArmado(Producto):
	precio_equipo = models.IntegerField("precio")
	imagen_equipo =  models.ImageField("imagen",upload_to = 'productos/')

	def __unicode__(self):
		return u'%s %s' % (self.precio_equipo, self.nombre_produc)

class Tipo(models.Model):
	nombre_tipo = models.CharField("nombre tipo",max_length = 100, blank = False)

	def __unicode__(self):
		return self.nombre_tipo

class Subtipo(models.Model):
	tipo = models.ForeignKey(Tipo, verbose_name = "Nombre tipo al que pertenece")
	sub_subtipo = models.ForeignKey('self',null = True, blank = True, verbose_name = "Sub-subtipo. Deje en blanco si no pertenece a ningun subtipo")
	nombre_subtipo = models.CharField("nombre subtipo",max_length = 100,blank = False)

	def __unicode__(self):
		return self.nombre_subtipo

class Caracteristica(models.Model):
	subtipo = models.ForeignKey(Subtipo)
	nombre_caracteristica = models.CharField("nombre caracteristica", max_length = 200, blank = False)
	unidad = models.CharField("unidad de medida", max_length= 50, blank = True)

	def __unicode__(self):
		return u'%s %s' % (self.nombre_caracteristica, self.unidad)

#Hereda nombre_produc
class Dispositivo(Producto):
	subtipo_disp = models.ForeignKey(Subtipo, verbose_name="Subtipo")
	cantidad_disp = models.IntegerField("cantidad")
	precio_disp = models.IntegerField("precio")
	marca_disp = models.CharField("marca", max_length = 100)
	imagen_disp = models.ImageField("imagen",upload_to = 'productos/',)
	descrip_disp = models.TextField("descripcion")

	def __unicode__(self):
		return u'%s %s %s %s %s' % (self.cantidad_disp,self.precio_disp,self.descrip_disp,self.nombre_produc, self.imagen_disp)

class DetalleCaracteristica(models.Model):
	caracteristica = models.ForeignKey(Caracteristica, verbose_name = "Caracteristica")
	dispositivo = models.ForeignKey(Dispositivo, verbose_name = "Dispositivo")
	medida = models.IntegerField("valor")

#Tabla intermedia entre EquipoArmado y Dispositivos
class DetalleEquipo(models.Model):
	dispositivo = models.ForeignKey(Dispositivo)
	equipo_armado = models.ForeignKey(EquipoArmado, unique = True)
	cantidad_equipo = models.IntegerField("cantidad")

class Incompat(models.Model):
	producto1 = models.ForeignKey(Dispositivo, related_name = 'produc_incomp_1')
	producto2 = models.ForeignKey(Dispositivo, related_name = 'produc_incomp_2')

class Compat(models.Model):
	producto1 = models.ForeignKey(Dispositivo, related_name = 'produc_comp_1')
	producto2 = models.ForeignKey(Dispositivo, related_name = 'produc_comp_2')

"""
#Tabla servicio tecnico
class ServicioTecnico(Producto):
	producto_serv = models.ForeignKey(Producto, unique = True, related_name = 'servicio_producto')
	precio_serv = models.IntegerField()
	descrip_serv = models.TextField()

	def __unicode__(self):
		return u'%s %s' % (self.precio_serv, self.descrip_serv)
"""	