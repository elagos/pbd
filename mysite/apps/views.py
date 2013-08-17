#!/usr/bin/python
# -*- coding: Utf8 -*-
from django.core.context_processors import csrf
from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,Group
from django.core.urlresolvers import reverse
from mysite.apps.models import *
from mysite.apps.forms import *

"""
Para cambiar tambien objetos relacionados, como nombre subtipos, se debe usar select_related()
Buscarlo en "making queries"
"""

def index_view(request):
	return render_to_response('home/index.html',context_instance=RequestContext(request))

def menuA_view(request):
    return render_to_response('home/menuA.html',context_instance=RequestContext(request))

def menuE_view(request):
    return render_to_response('home/menuE.html',context_instance=RequestContext(request))
    
def prueba_view(request):
	if request.method == 'POST':
		form = registroUsuario(request.POST)
		if form.is_valid():
			rut = form.cleaned_data['rut']
			nombre = form.cleaned_data['nombre']
			mail = form.cleaned_data['mail']
			telefono = form.cleaned_data['telefono']
			pass1 = form.cleaned_data['pass1']
			#Comprobacion del password
			pass2 = form.cleaned_data['pass2']
			return HttpResponseRedirect('/agregar_user_sucess/') #PÁGINA NO CREADA! Redirigimos después del envío POST
	
	else:
		form = registroUsuario()
	
	return render(request, 'prueba.html', {'form': form})

"""
def login(request):
	username = request.POST['username']
	password = request.POST['password']
	user = auth.authenticate(username=username, password=password)
	if user is not None
		#El password es correcto, y el usuario está marcado como activo
		auth.login(request, user)
		#Redirigimos a una página, ya logueado
		return HttpResponseRedirect("#")
	else:
		#Error de autentificación
		return HttpResponseRedirect("#")
"""

#Funcion que genera formulario para agregar tipo.	
def agregar_tipo(request):
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
			ctx_success = {'success':success,'agregarTipoForm':nuevo_tipo_form}
			return render_to_response('agregar_tipo.html',ctx_success, context_instance = RequestContext(request))
	else:
		formulario = tipoForm() 
	return render(request, 'agregar_tipo.html',{'agregarTipoForm':formulario})

#FALTA VALIDAR NULL
def editar_tipo(request):
	lista_tipos = Tipo.objects.all()
	if request.method == 'POST':
		formulario = tipoForm(request.POST)
		if formulario.is_valid():
			nuevo_nombre_tipo = formulario.cleaned_data['nombre_tipo']
			tipoEscogido = request.POST['tipo']
			editar_tipo = Tipo.objects.filter(nombre_tipo = tipoEscogido).update(nombre_tipo = nuevo_nombre_tipo)
			#editar_tipo.save()
			formulario = tipoForm()
			success = True
			ctx_success = {'success': success,'editarTipoForm':formulario,'lista_tipos':lista_tipos}
			return render_to_response('editar_tipo.html',ctx_success,context_instance = RequestContext(request))
	else:
		formulario = tipoForm()
		ctx = {'editarTipoForm':formulario,'lista_tipos':lista_tipos}
	return render(request, 'editar_tipo.html',ctx)

def eliminar_tipo(request):
	lista_tipos = Tipo.objects.all()
	if request.method == 'POST':
		tipoEscogido = request.POST['tipo']
		if tipoEscogido == "VACIO":
			error = True
			success = False
		else:
			error = False
			eliminar_tipo = Tipo.objects.filter(id = tipoEscogido).delete()
			success = True
		ctx= {'success':success, 'lista_tipos':lista_tipos,'error':error}
		return render_to_response('eliminar_tipo.html',ctx, context_instance = RequestContext(request))
	else:
		ctx = {'lista_tipos':lista_tipos}
	return render_to_response('eliminar_tipo.html',ctx,context_instance = RequestContext(request))

def agregar_subtipo(request):
	global lista_subtipos
	hay_tipos = Tipo.objects.all()
	if request.method == 'POST':
		formulario = subtipoForm(request.POST)
		if formulario.is_valid():
			nuevo_nombre = formulario.cleaned_data['nombre_subtipo']
			tipo_asignado = formulario.cleaned_data['tipo']
			nuevo_sub_subtipo = formulario.cleaned_data['sub_subtipo']

			#####Falta crear validacion de que subtipo pertenezca al tipo escogido
			#Almacenamos valor de estos 2 campos
			nuevo_subtipo = Subtipo(nombre_subtipo = nuevo_nombre, tipo = tipo_asignado)

			if nuevo_sub_subtipo:
				add_subsubtipo = Subtipo(sub_subtipo = nuevo_sub_subtipo)
			
			#Almacenamos en la base de datos
			nuevo_subtipo.save()
			nuevo_subtipo_form = subtipoForm()
			success = True
			ctx_success = {'success':success,'agregarTipoForm':nuevo_subtipo_form,'hay_tipos':hay_tipos}
			return render_to_response('agregar_subtipo.html',ctx_success, context_instance = RequestContext(request))
	else:
		formulario = subtipoForm() 
	return render(request, 'agregar_subtipo.html',{'agregarSubtipoForm':formulario,'hay_tipos':hay_tipos})

def eliminar_subtipo(request):
	lista_subtipos = Subtipo.objects.all()
	if request.method == 'POST':
		subtipoEscogido = request.POST['subtipo']
		if subtipoEscogido == "VACIO":
			error = True
			success = False
		else:
			error = False
			eliminar_subtipo = Subtipo.objects.filter(id = subtipoEscogido).delete()
			success = True
		ctx= {'success':success, 'lista_subtipos':lista_subtipos,'error':error}
		return render_to_response('eliminar_subtipo.html',ctx, context_instance = RequestContext(request))
	else:
		ctx = {'lista_subtipos':lista_subtipos}
		return render_to_response('eliminar_subtipo.html',ctx,context_instance = RequestContext(request))

"""
def editar_subtipo(request):
		lista_subtipos = Subtipo.objects.all()
		if request.method == 'POST':
				subtipoEscogido = request.POST.get['subtipo']
				nuevo_nombre_subtipo = request.POST.get['']

				#Trigger
				if Dispositivo.objects.filter(subtipo_disp = subtipoEscogido):
					for dispositivo in disp_editar:
						dispositivo.update(subtipo_disp = nuevo_nombre_subtipo)

				if carac_editar = Caracteristica.objects.filter()


				editar_tipo = Subtipo.objects.filter(nombre_subtipo = subtipoEscogido).update(nombre_subtipo = nuevo_nombre_subtipo)
				formulario = editarSubtipoForm()
				success = True
				ctx = {'success': success,'editarSubtipoForm':formulario,'lista_tipos':lista_tipos}
		else:
			formulario = editarSubtipoForm()
			ctx = {'editarSubtipoForm':formulario,'lista_subtipos':lista_subtipos}
	return render_to_response('editar_subtipo.html',ctx,context_instance = RequestContext(request))
"""

#FALTA CORREGIR LO DE EDITAR_DISPOSITIVO PARA QUE ESTO QUEDE BUENO
def ingresar_stock(request):
	lista_dispositivo = Dispositivo.objects.all()
	lista_subtipo = Subtipo.objects.all()
	lista_stock = Abastecimiento.objects.all()
	if request.method == 'POST':
		formulario = abastecimientoForm(request.POST)
		if formulario.is_valid():
			producto = formulario.cleaned_data['producto_abast']
			cantidad = formulario.cleaned_data['cant_abast']
			fecha = formulario.cleaned_data['fecha']
			#producto = request.POST.get('disp_elegido')
			nuevo_abast = Abastecimiento(producto_abast = producto, cant_abast = cantidad, fecha = fecha)
			stockForm = abastecimientoForm()
			nuevo_abast.save()
			success = True
			stockForm = abastecimientoForm()

			#Trigger que suma la cantidada a tabla "Dispositivo"
			dispositivo = Dispositivo.objects.get(nombre_produc = producto)
			nueva_cantidad = dispositivo.cantidad_disp + cantidad
			producto_id = dispositivo.id
			update_cantidad = Dispositivo.objects.get(id = producto_id)
			update_cantidad.cantidad_disp = nueva_cantidad
			update_cantidad.save()
			disp_nueva_cant = Dispositivo.objects.get(id = producto_id)
			ctx = {'success':success,'stockForm':stockForm,'lista_stock':lista_stock,'dispositivo':disp_nueva_cant}
	else:
		formulario = abastecimientoForm() 
		ctx = {'stockForm':formulario,'lista_subtipo':lista_subtipo,'lista_dispositivo':lista_dispositivo,'lista_stock':lista_stock}
	return render_to_response('ingresar_stock.html', ctx,context_instance = RequestContext(request))

def agregar_dispositivo(request):
	hay_dispositivos = Dispositivo.objects.all()
	if request.method == 'POST':
		formulario = dispositivoForm(request.POST,request.FILES)
		if formulario.is_valid():
			nombre = formulario.cleaned_data['nombre_produc']
			subtipo = formulario.cleaned_data['subtipo_disp']
			precio = formulario.cleaned_data['precio_disp']
			descripcion = formulario.cleaned_data['descrip_disp']
			imagen = formulario.cleaned_data['imagen_disp']
			marca = formulario.cleaned_data['marca_disp']

			nuevo_dispositivo = Dispositivo(nombre_produc = nombre, subtipo_disp = subtipo,destacado = False, cantidad_disp = 0,precio_disp = precio, imagen_disp = imagen,descrip_disp = descripcion, marca_disp = marca)
			nuevo_dispositivo.save()
			formulario = dispositivoForm()
			success = True
			ctx_success = {'success':success,'agregarDispositivoForm':formulario, 'hay_dispositivos':hay_dispositivos}
			return render_to_response('agregar_dispositivo.html',ctx_success, context_instance = RequestContext(request))
	else:
		formulario = dispositivoForm()
	return render_to_response('agregar_dispositivo.html',{'agregarDispositivoForm':formulario,'hay_dispositivos':hay_dispositivos},context_instance = RequestContext(request))




#######REVISAR EDITAR DISPOSITIVO!!!!!!!!!!!
def escoger_dispositivo(request):
	lista_dispositivo = Dispositivo.objects.all()
	lista_subtipo = Subtipo.objects.all()
	
	#Si ya se escogio el producto, se genera el formulario para editar el dispositivo
	if (request.method=='POST'):
		dispositivo = request.POST.get('disp_elegido')
		dispositivoEdit = Dispositivo.objects.get(id = dispositivo)
		formulario = dispositivoForm(instance = dispositivoEdit)
		editar_listo = True
		ctx = {'dispositivoEdit':dispositivoEdit,'editarDispositivoForm':formulario,'editar_listo':editar_listo,'id_dispositivo':dispositivo}
		return render_to_response('editar_dispositivo.html',ctx,context_instance = RequestContext(request))
	else:
		ctx = {'lista_dispositivo':lista_dispositivo,'lista_subtipo':lista_subtipo}
		return render_to_response('escoger_dispositivo.html', ctx, context_instance = RequestContext(request))

#Está malo! se tiene que corregir unas leseras
def editar_dispositivo(request):
	if (request.method=='POST'):
		if formulario.is_valid():
			dispositivo_elegido = request.POST.get('dispositivo')
			nombre_produc_edit = formulario.cleaned_data['nombre_produc']
			subtipo_disp_edit = formulario.cleaned_data['subtipo_disp']
			precio_disp_edit = formulario.cleaned_data['precio_disp']
			descrip_disp_edit = formulario.cleaned_data['descrip_disp']
			imagen_disp_edit = formulario.cleaned_data['imagen_disp']
			marca_disp_edit = formulario.cleaned_data['marca_disp']
			editar_dispositivo = Dispositivo.objects.get(id = dispositivo_elegido).update(
				nombre_produc = nombre_produc_edit,
				destacado=destacado_edit,
				subtipo_disp=subtipo_disp_edit,
				cantidad_disp=cantidad_disp_edit,
				precio_disp=precio_disp_edit,
				marca_disp=marca_disp_edit,
				imagen_disp=imagen_disp_edit,
				descrip_disp=descrip_disp_edit
				)
			success = True
			editar_listo = False
			ctx = {'success':success,'editar_listo':editar_listo}
			return render_to_response('editar_dispositivo.html',ctx,context_instance = RequestContext(request))
		else:
			formulario = editarDispositivoForm(request.POST, request.FILES)
			ctx = {'editarDispositivoForm':formulario}
			return	render_to_response('editar_dispositivo.html', ctx, context_instance = RequestContext(request))

#NO FUNCIONAL
"""
def funcion_filtro(request):
	resultados = json_decode(data)
	datos_filtrados = json(resultados)
	ctx = {'datos_filtrados':datos_filtrados}
	return render_to_response('editar_dispositivo.html',ctx,context_instance = RequestContext(request))
"""

def agregar_caracteristica(request):
	lista_caracteristica = Caracteristica.objects.all()
	if request.method == 'POST':
		formulario = caracteristicaForm(request.POST)
		if formulario.is_valid():
			nombre = formulario.cleaned_data['nombre_caracteristica']
			subtipo = formulario.cleaned_data['subtipo']
			unidad = formulario.cleaned_data['unidad']

			nuevo_caracteristica = Caracteristica(subtipo = subtipo,nombre_tipo = nuevo_nombre, unidad = unidad)
			nuevo_caracteristica.save()
			formulario = caracteristicaForm()
			success = True
			ctx = {'success':success,'agregarCaracteristicaForm':formulario,'lista_caracteristica':lista_caracteristica}
			return render_to_response('agregar_caracteristica.html',ctx, context_instance = RequestContext(request))
	else:
		formulario = caracteristicaForm() 
	ctx = {'agregarCaracteristicaForm':formulario, 'lista_caracteristica':lista_caracteristica}
	return render_to_response('agregar_caracteristica.html',ctx,context_instance = RequestContext(request))

def eliminar_dispositivo(request):
	lista_dispositivo = Dispositivo.objects.all()
	lista_subtipo = Subtipo.objects.all()
	if request.method == 'POST':
		dispositivoEscogido = request.POST['disp_elegido']
		error = False
		eliminar_dispositivo = Dispositivo.objects.filter(id = dispositivoEscogido).delete()
		success = True
		ctx= {'success':success, 'lista_dispositivo':lista_dispositivo,'error':error,'lista_subtipo':lista_subtipo}
	else:
		ctx = {'lista_subtipo':lista_subtipo,'lista_dispositivo':lista_dispositivo}
	return render_to_response('eliminar_dispositivo.html',ctx,context_instance = RequestContext(request))

def definir_compatibilidad(request):
	pass

def definir_incompatibilidad(request):
	pass

def armar_equipo(request):
	pass

def eliminar_equipo(request):
	pass


def ver_servicio():
	pass
