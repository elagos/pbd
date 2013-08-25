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

class Abastecimiento(models.Model):
	producto_abast = models.ForeignKey(Producto, related_name = 'abast_producto', verbose_name = "Producto a ingresar")
	cant_abast = models.PositiveIntegerField("cantidad") 
	fecha = models.DateTimeField("fecha")

	def __unicode__(self):
		return u'%s' % (self.producto_abast)

#Tabla de equipos armados. Hereda nombre_produc
class EquipoArmado(Producto):
	precio_equipo = models.PositiveIntegerField("precio")
	imagen_equipo =  models.ImageField("imagen",upload_to = 'productos/')

	def __unicode__(self):
		return u'%s %s' % (self.precio_equipo, self.nombre_produc)

class Tipo(models.Model):
	nombre_tipo = models.CharField("nombre tipo",max_length = 100, blank = False)

	def __unicode__(self):
		return self.nombre_tipo

class Subtipo(models.Model):
	tipo_padre= models.ForeignKey(Tipo,null = True, blank = True, verbose_name = "Tipo padre")
	subtipo_padre = models.ForeignKey('self',null = True, blank = True, verbose_name = "Subtipo padre")
	nombre_subtipo = models.CharField("nombre subtipo",max_length = 100,blank = False)

	def __unicode__(self):
		return u'%s' % (self.nombre_subtipo)

class Caracteristica(models.Model):
	subtipo = models.ForeignKey(Subtipo)
	nombre_caracteristica = models.CharField("nombre caracteristica", max_length = 200, blank = False)
	unidad = models.CharField("unidad de medida", max_length= 50, blank = True)

	def __unicode__(self):
		return u'%s' % (self.nombre_caracteristica)

class Dispositivo(Producto):
	subtipo_disp = models.ForeignKey(Subtipo, verbose_name="Subtipo")
	cantidad_disp = models.PositiveIntegerField("cantidad")
	precio_disp = models.PositiveIntegerField("precio")
	marca_disp = models.CharField("marca", max_length = 100)
	imagen_disp = models.ImageField("imagen",upload_to = 'productos/',)
	descrip_disp = models.TextField("descripcion")

	def __unicode__(self):
		return u'%s' % (self.nombre_produc)

class DetalleCaracteristica(models.Model):
	caracteristica = models.ForeignKey(Caracteristica, verbose_name = "Caracteristica")
	dispositivo = models.ForeignKey(Dispositivo, verbose_name = "Dispositivo")
	medida = models.PositiveIntegerField("valor")

class DetalleEquipo(models.Model):
	dispositivo = models.ForeignKey(Dispositivo)
	equipo_armado = models.ForeignKey(EquipoArmado, unique = True)
	cantidad_equipo = models.PositiveIntegerField("cantidad")

class Incompatibilidad(models.Model):
	dispositivo1 = models.ForeignKey(Dispositivo, related_name = 'produc_incomp_1')
	dispositivo2 = models.ForeignKey(Dispositivo, related_name = 'produc_incomp_2')

	def __unicode__(self):
		return u'%s %s' % (self.dispositivo1, self.dispositivo2)

class Compatibilidad(models.Model):
	dispositivo = models.ForeignKey(Dispositivo, related_name = 'dispositivo_compatible')
	subtipo = models.ForeignKey(Subtipo, related_name = 'subtipo_compatible')

	def __unicode__(self):
		return u'%s %s' % (self.dispositivo, self.subtipo)


#Tabla servicio tecnico
class ServicioTecnico(models.Model):
	nombre_serv = models.CharField("nombre", max_length = 200)
	precio_serv = models.PositiveIntegerField("precio servicio")
	descrip_serv = models.TextField("descripcion")

	def __unicode__(self):
		return u'%s' % (self.nombre_serv)