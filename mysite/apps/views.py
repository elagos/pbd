#!/usr/bin/python
# -*- coding: Utf8 -*-
from django import forms
from django.core.context_processors import csrf
from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,Group
from django.core.urlresolvers import reverse
from mysite.apps.models import *
from mysite.apps.forms import *
from cart import Cart

"""
Para cambiar tambien objetos relacionados, como nombre subtipos, se debe usar select_related()
Buscarlo en "making queries"
"""

def index_view(request):
	lista_tipo = Tipo.objects.all()
	lista_subtipo = Subtipo.objects.all()
	ctx = {'lista_tipo': lista_tipo, 'lista_subtipo':lista_subtipo}
	return render_to_response('home/index.html',ctx,context_instance=RequestContext(request))


#def _view(request):
#    return render_to_response('home/.html',context_instance=RequestContext(request))

###################### registro ############################
##########------------------------------------##############
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/accounts/profile/")
        else:
        	failure=True
        	form = UserCreationForm()
    		return render_to_response('registration/register.html', {'form': form,'failure':failure},context_instance = RequestContext(request))
    else:
        form = UserCreationForm()
    	return render_to_response('registration/register.html', {'form': form,},context_instance = RequestContext(request))

def logout_view(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/home/")    	
##########------------------------------------##############
###################### registro ############################



####################### Carrito ############################
##########------------------------------------##############
def formularioCarrito_view(request):
	if request.method == 'POST':
		productito = request.POST['disp']
		cant = request.POST['cant']
		add_to_cart(productito,cant)
		success = True
		ctx = {'success':success}
		return render_to_response('home/carrito/formularioCarrito.html',ctx,context_instance = RequestContext(request))# Fin Menu Administrador
	else:
		return render_to_response('home/carrito/formularioCarrito.html',context_instance = RequestContext(request))# Fin Menu Administrador

def addCarrito(numerito):
	numerito = numerito * 2
	return numerito

def add_to_cart(request,product_id, quantity):
    product = Dispositivo.objects.get(nombre_produc=product_id)
    cart = Cart(request)
    cart.add(product, product.precio_disp, quantity)

def remove_from_cart(request,product_id):
    product = Producto.objects.get(id=product_id)
    cart = Cart(request)
    cart.remove(product)

def carrito_view(request):
    return render_to_response('home/carrito/cart.html', dict(cart=Cart(request)))
##########------------------------------------##############
####################### Carrito ############################




################## Menu Administrador ######################
##########------------------------------------##############
def menuA_view(request):
	return render_to_response('home/menuA/admStock.html',context_instance = RequestContext(request))# Fin Menu Administrador

def admStock_view(request):
    return render_to_response('home/menuA/admStock.html',context_instance=RequestContext(request))

#### Dispositivos-------------------------------------
def admDispositivos_view(request):
    return render_to_response('home/menuA/admDispositivos/index.html',context_instance=RequestContext(request))

def agDispositivo_view(request):# Agregar Dispositivo
	lista_dispositivos = Dispositivo.objects.all()
	if request.method == 'POST':
		formulario = dispositivoForm(request.POST,request.FILES)
		if formulario.is_valid():
			nombre = formulario.cleaned_data['nombre_produc']
			subtipo = formulario.cleaned_data['subtipo_disp']
			precio = formulario.cleaned_data['precio_disp']
			descripcion = formulario.cleaned_data['descrip_disp']
			# imagen = formulario.cleaned_data['imagen_disp']
			marca = formulario.cleaned_data['marca_disp']
			nuevo_dispositivo = Dispositivo(nombre_produc = nombre, subtipo_disp = subtipo,destacado = False, cantidad_disp = 0,precio_disp = precio, descrip_disp = descripcion, marca_disp = marca)
			nuevo_dispositivo.save()
			formulario = dispositivoForm()
			success = True
			ctx = {'success':success,'agregarDispositivoForm':formulario}
			return render_to_response('home/menuA/admDispositivos/agDispositivo.html',ctx, context_instance = RequestContext(request))
		else:
			formulario = dispositivoForm(request.POST)
			failure=True
			error="Debe rellenar apropiadamente los datos."
			ctx={'agregarDispositivoForm':formulario,'error':error,'failure':failure}
			return render_to_response('home/menuA/admDispositivos/agDispositivo.html',ctx, context_instance = RequestContext(request))
	else:
		formulario = dispositivoForm()
		ctx={'agregarDispositivoForm':formulario}
    	return render_to_response('home/menuA/admDispositivos/agDispositivo.html',ctx,context_instance=RequestContext(request))

def elDispositivo_view(request):# Eliminar Dispositivo
	lista_dispositivo = Dispositivo.objects.all().order_by('nombre_produc')
	lista_subtipo = Subtipo.objects.all()
	if request.method == 'POST':
		dispositivoEscogido = request.POST['disp_elegido']
		eliminar_dispositivo = Dispositivo.objects.filter(id = dispositivoEscogido).delete()
		success = True
		ctx= {'success':success, 'lista_dispositivo':lista_dispositivo,'lista_subtipo':lista_subtipo}
	else:
		ctx = {'lista_subtipo':lista_subtipo,'lista_dispositivo':lista_dispositivo}
    	return render_to_response('home/menuA/admDispositivos/elDispositivo.html',ctx,context_instance=RequestContext(request))

def edDispositivo_view(request):# Editar Dispositivo
    return render_to_response('home/menuA/admDispositivos/edDispositivo.html',context_instance=RequestContext(request))

#### Equipos Armados-------------------------------------
def admEArmados_view(request):
    return render_to_response('home/menuA/admEArmados/index.html',context_instance=RequestContext(request))

def agEquipo_view(request):# Agregar Equipo
    return render_to_response('home/menuA/admEArmados/agEquipo.html',context_instance=RequestContext(request))

def elEquipo_view(request):# Eliminar Equipo
    return render_to_response('home/menuA/admEArmados/elEquipo.html',context_instance=RequestContext(request))

def edEquipo_view(request):# Editar Equipo
    return render_to_response('home/menuA/admEArmados/edEquipo.html',context_instance=RequestContext(request))

#### Servicios Técnicos------------------------------------------
def admSTecnicos_view(request):
    return render_to_response('home/menuA/admSTecnicos/index.html',context_instance=RequestContext(request))

def agSTecnico_view(request):# Agregar STecnico
    return render_to_response('home/menuA/admSTecnicos/agSTecnico.html',context_instance=RequestContext(request))

def elSTecnico_view(request):# Eliminar STecnico
    return render_to_response('home/menuA/admSTecnicos/elSTecnico.html',context_instance=RequestContext(request))

def edSTecnico_view(request):# Editar STecnico
    return render_to_response('home/menuA/admSTecnicos/edSTecnico.html',context_instance=RequestContext(request))

#### Compatibilidades------------------------------------------
def admCompatibilidades_view(request):
    return render_to_response('home/menuA/admCompatibilidades/index.html',context_instance=RequestContext(request))

def agCompatibilidad_view(request):# Agregar Compatibilidad
    return render_to_response('home/menuA/admCompatibilidades/agCompatibilidad.html',context_instance=RequestContext(request))

def elCompatibilidad_view(request):# Eliminar Compatibilidad
    return render_to_response('home/menuA/admCompatibilidades/elCompatibilidad.html',context_instance=RequestContext(request))

def edCompatibilidad_view(request):# Editar Compatibilidad
    return render_to_response('home/menuA/admCompatibilidades/edCompatibilidad.html',context_instance=RequestContext(request))

#### Tipos y Subtipos-------------------------------------
def admTySubtipos_view(request):
    return render_to_response('home/menuA/admTySubtipos/index.html',context_instance=RequestContext(request))

def agTipo_view(request):# Agregar Tipo
	global lista_tipos
	lista_tipos = Tipo.objects.all()
	if request.method == 'POST':
		formulario = tipoForm(request.POST)
		if formulario.is_valid():
			success = True
			nuevo_nombre = formulario.cleaned_data['nombre_tipo']
			nuevo_tipo = Tipo(nombre_tipo = nuevo_nombre)
			nuevo_tipo.save()
			nuevo_tipo_form = tipoForm()
			ctx = {'success':success,'agregarTipoForm':nuevo_tipo_form}
			return render_to_response('home/menuA/admTySubtipos/agTipo.html',ctx, context_instance = RequestContext(request))
		else:
			formulario = tipoForm(request.POST)
			failure=True
			error="Debe rellenar apropiadamente los datos."
			ctx={'agregarTipoForm':formulario,'failure':failure,'error':error}
			return render_to_response('home/menuA/admTySubtipos/agTipo.html',ctx, context_instance = RequestContext(request))
	else:
		formulario = tipoForm()
		ctx={'agregarTipoForm':formulario}
		return render_to_response('home/menuA/admTySubtipos/agTipo.html',ctx, context_instance = RequestContext(request))

def elTipo_view(request):# Eliminar Tipo
	lista_tipos = Tipo.objects.all().order_by('nombre_tipo')
	if request.method == 'POST':
		tipoEscogido = request.POST['tipo']
		if tipoEscogido == "VACIO":
			failure = True
			success = False
			error="Debe elegir el tipo a eliminar."
		else:
			failure = False
			eliminar_tipo = Tipo.objects.filter(id = tipoEscogido).delete()
			success = True
			error="holi"
		ctx= {'success':success, 'lista_tipos':lista_tipos,'failure':failure,'error':error}
		return render_to_response('home/menuA/admTySubtipos/elTipo.html',ctx, context_instance = RequestContext(request))
	else:
		ctx = {'lista_tipos':lista_tipos}
		return render_to_response('home/menuA/admTySubtipos/elTipo.html',ctx,context_instance = RequestContext(request))

def edTipo_view(request):# Editar Tipo
	lista_tipos = Tipo.objects.all().order_by('nombre_tipo')
	if request.method == 'POST':
		formulario = tipoForm(request.POST)
		if formulario.is_valid():
			nuevo_nombre_tipo = formulario.cleaned_data['nombre_tipo']
			tipoEscogido = request.POST['tipo']
			if tipoEscogido == "VACIO":
				success = False
				failure = True
				error="Debe elegir el tipo a editar"
			else:
				success = True
				failure = False
				error="holi"
				editar_tipo = Tipo.objects.filter(nombre_tipo = tipoEscogido).update(nombre_tipo = nuevo_nombre_tipo)
				#editar_tipo.save()
				formulario = tipoForm(request.POST)
			ctx = {'success': success,'failure':failure,'editarTipoForm':formulario,'lista_tipos':lista_tipos,'error':error}
			return render_to_response('home/menuA/admTySubtipos/edTipo.html',ctx,context_instance = RequestContext(request))
		else:
			formulario = tipoForm(request.POST)
			failure=True
			error="Debe rellenar apropiadamente los datos."
			ctx={'editarTipoForm':formulario,'failure':failure,'lista_tipos':lista_tipos,'error':error}
			return render_to_response('home/menuA/admTySubtipos/edTipo.html',ctx,context_instance = RequestContext(request))

	else:
		formulario = tipoForm()
		ctx = {'editarTipoForm':formulario,'lista_tipos':lista_tipos}
		return render_to_response('home/menuA/admTySubtipos/edTipo.html',ctx, context_instance = RequestContext(request))

def agSTipo_view(request):# Agregar Subtipo
	global lista_subtipos
	lista_tipos = Tipo.objects.all().order_by('nombre_tipo')
	if request.method == 'POST':
		formulario = subtipoForm(request.POST)
		if formulario.is_valid():
			nuevo_nombre = formulario.cleaned_data['nombre_subtipo']
			tipo_asignado = formulario.cleaned_data['tipo_padre']
			subtipo_asignado = formulario.cleaned_data['subtipo_padre']

			if tipo_asignado or subtipo_asignado:
				#Si se eligio Tipo y Subtipo, se lanza error
				if tipo_asignado and subtipo_asignado:
					failure=True
					error = "Debe elegir un tipo o un subtipo, no ambas."
					formulario = subtipoForm(request.POST)
					ctx = {'failure':failure,'error':error,'agregarSubtipoForm':formulario,'lista_tipos':lista_tipos}
					return render_to_response('home/menuA/admTySubtipos/agSTipo.html',ctx, context_instance = RequestContext(request))
				#Se revisa si subtipo agregado pertenece a un tipo o a un subtipo
				
				if tipo_asignado:
					nuevo_subtipo = Subtipo(nombre_subtipo = nuevo_nombre, tipo_padre = tipo_asignado)
				elif subtipo_asignado:
					nuevo_subtipo = Subtipo(nombre_subtipo = nuevo_nombre, subtipo_padre = subtipo_asignado)
				
				#Almacenamos en la base de datos
				nuevo_subtipo.save()
				formulario = subtipoForm()
				success = True
				ctx = {'success':success,'agregarSubtipoForm':formulario,'lista_tipos':lista_tipos}
				return render_to_response('home/menuA/admTySubtipos/agSTipo.html',ctx, context_instance = RequestContext(request))
			else:
				error = "Debe elegir un tipo o un subtipo padre."
				failure=True
				formulario = subtipoForm(request.POST)
				ctx = {'failure':failure,'error':error,'agregarSubtipoForm':formulario,'lista_tipos':lista_tipos}
				return render_to_response('home/menuA/admTySubtipos/agSTipo.html',ctx, context_instance = RequestContext(request))
		else:
			formulario = subtipoForm(request.POST)
			failure=True
			error="Debe rellenar apropiadamente los datos."
			ctx = {'failure':failure,'error':error,'agregarSubtipoForm':formulario,'lista_tipos':lista_tipos}
			return render_to_response('home/menuA/admTySubtipos/agSTipo.html',ctx, context_instance = RequestContext(request))
	else:
		formulario = subtipoForm()
		ctx ={'agregarSubtipoForm':formulario,'lista_tipos':lista_tipos}
		return render_to_response('home/menuA/admTySubtipos/agSTipo.html',ctx,context_instance=RequestContext(request))

def elSTipo_view(request):# Eliminar Subtipo
	lista_subtipos = Subtipo.objects.all().order_by('nombre_subtipo')
	if request.method == 'POST':
		subtipoEscogido = request.POST['subtipo']
		if subtipoEscogido == "VACIO":
			success = False
			failure = True
			error="Debe elegir el subtipo a eliminar"
		else:
			failure = False
			error="holi"
			eliminar_subtipo = Subtipo.objects.filter(id = subtipoEscogido).delete()
			success = True
		ctx= {'success':success, 'lista_subtipos':lista_subtipos,'error':error,'failure':failure}
		return render_to_response('home/menuA/admTySubtipos/elSTipo.html',ctx, context_instance = RequestContext(request))
	else:
		ctx = {'lista_subtipos':lista_subtipos}
		return render_to_response('home/menuA/admTySubtipos/elSTipo.html',ctx,context_instance=RequestContext(request))

def edSTipo_view(request):# Editar Subtipo
    return render_to_response('home/menuA/admTySubtipos/edSTipo.html',context_instance=RequestContext(request))

#### Empleados---------------------------------------
def admEmpleados_view(request):
    return render_to_response('home/menuA/admEmpleados/index.html',context_instance=RequestContext(request))

def agEmpleado_view(request):# Agregar Empleado
    return render_to_response('home/menuA/admEmpleados/agEmpleado.html',context_instance=RequestContext(request))

def elEmpleado_view(request):# Editar Empleado
    return render_to_response('home/menuA/admEmpleados/elEmpleado.html',context_instance=RequestContext(request))

def edEmpleado_view(request):# Eliminar Empleado
    return render_to_response('home/menuA/admEmpleados/edEmpleado.html',context_instance=RequestContext(request))

#### Asignar Armado---------------------------------------
def asigArmado_view(request):
    return render_to_response('home/menuA/asigArmado/index.html',context_instance=RequestContext(request))

def asigServicio_view(request):
    return render_to_response('home/menuA/asigServicio/index.html',context_instance=RequestContext(request))

def confArmado_view(request):
    return render_to_response('home/menuA/confArmado/index.html',context_instance=RequestContext(request))

def confServicio_view(request):
    return render_to_response('home/menuA/confServicio/index.html',context_instance=RequestContext(request))

def regServicio_view(request):
    return render_to_response('home/menuA/regServicio/index.html',context_instance=RequestContext(request))
##########------------------------------------##############
################## Menu Administrador ######################







def menuE_view(request):
    return render_to_response('home/menuE.html',context_instance=RequestContext(request))
    
