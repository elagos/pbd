# -*- coding: utf-8 -*-
from django import forms
from mysite.apps.models import *
from datetimewidget.widgets import DateTimeWidget

#form registro usuario en la web
class registroUsuario(forms.Form):

	rut = forms.IntegerField()
	nombre = forms.CharField()
	mail = forms.EmailField()
	telefono = forms.IntegerField()
	pass1 = forms.CharField()
	#Comprobacion del password
	pass2 = forms.CharField()

#Para almacenar datos que no llenaran todos los campos de una tablar,
#recordar form.save(commit=False)
#Django previene cualquier intento de guardar un modelo incompleto.

class dispositivoForm(forms.ModelForm):
	class Meta:
		model = Dispositivo
		exclude = ('destacado','cantidad_disp')
"""
class servicioForm(forms.ModelForm):
	class Meta:
		model = ServicioTecnico
"""
class equipoForm(forms.ModelForm):
	class Meta:
		model = EquipoArmado

class tipoForm(forms.ModelForm):
	class Meta:
		model = Tipo

class subtipoForm(forms.ModelForm):
	class Meta:
		model = Subtipo
		#fields = ('tipo','nombre_subtipo')

class abastecimientoForm(forms.ModelForm):
	class Meta:
		model = Abastecimiento
		#exclude = ('producto_abast')
		opcionesFecha = {
			'format': 'dd/mm/yyyy HH:ii P',
			'autoclose': 'true',
			'showMeridian' : 'true'
		}
		widgets = {
				'fecha': DateTimeWidget(options = opcionesFecha)
		}

class caracteristicaForm(forms.ModelForm):
	class Meta:
		model = Caracteristica