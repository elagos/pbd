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



########################## Home ###############################
############------------------------------------###############
def index_view(request):
	productos = Producto.objects.all()
	for prod in productos:
		print prod.destacado
	ctx = {'lista_categorias': Tipo.objects.all().order_by('nombre_tipo'),'lista_dispositivo':Producto.objects.filter(destacado='True')}
	return render_to_response('home/index.html',ctx,context_instance=RequestContext(request))

def categorias_view(request):
	if request.method == 'POST':
		subtipo = int(request.POST['subtipo'])
		if subtipo == -1:
			return HttpResponseRedirect("/home/")
		categoria = request.POST['categoria']
		lista_subtipo = Subtipo.objects.all().order_by('nombre_subtipo')
		lista_dispositivo = []
		#Conseguimos los dispositivos de ese subtipo
		lista_dispos = Dispositivo.objects.filter(subtipo_disp = subtipo)
		for disp in lista_dispos:
					lista_dispositivo.append(disp)
		#Subtipo escogido
		subtipo_filtrado = Subtipo.objects.get(id = subtipo)
		#hijos directos del subtipo para mostrarlos en el select
		lista_subtipos_hijos = Subtipo.objects.filter(subtipo_padre = subtipo_filtrado)
		#Nombre subtipo
		nombre = subtipo_filtrado.nombre_subtipo
		#Almacenamos el nivel de categoria en que se encuentra, para mostrarlo en el template
		categoria = categoria + ' / ' + nombre
		#funcioncon la que se retornan todos los dispositivos de subtipos hijos
		for subt in lista_subtipos_hijos:
			hijos = descendientes_de_subtipo(subt.id)
			for elemento in hijos:
				dispositivo = Dispositivo.objects.filter(subtipo_disp = elemento)
				for disp in dispositivo:
					lista_dispositivo.append(disp)
		ctx = {'lista_subtipo':lista_subtipos_hijos,'lista_dispositivo':lista_dispositivo,'nombre':nombre,'lista_subtipos_hijos':lista_subtipos_hijos,'categoria':categoria,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
		return render_to_response('home/categorias.html',ctx, context_instance = RequestContext(request))
	if request.method == 'GET':
		if 'tipo' in request.GET:
			nombre = request.GET['tipo']
			if Tipo.objects.filter(nombre_tipo= nombre):
				tipo = Tipo.objects.get(nombre_tipo= nombre)
				nombre = tipo.nombre_tipo
				lista_subtipos_hijos = Subtipo.objects.filter(tipo_padre = tipo)
				lista_dispositivo = []
				categoria = nombre
				for subtipo in lista_subtipos_hijos:
					hijos = descendientes_de_subtipo(subtipo.id)
					for elemento in hijos:
						dispositivo = Dispositivo.objects.filter(subtipo_disp = elemento)
						for disp in dispositivo:
							lista_dispositivo.append(disp)
				ctx = {'lista_dispositivo':lista_dispositivo,'lista_subtipos_hijos':lista_subtipos_hijos,'nombre':nombre,'categoria':categoria,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
				return render_to_response('home/categorias.html',ctx, context_instance = RequestContext(request))
	return HttpResponseRedirect("/home/")

def search_view(request):
	if request.method == 'POST':
		nombre = request.POST['q']
		orden = int(request.POST['orden'])
		direcc = int(request.POST['direcc'])
		if orden==3 and direcc==1:
			lista_dispositivo=Dispositivo.objects.filter(nombre_produc__icontains=nombre).order_by('precio_disp')
		if orden==3 and direcc==2:
			lista_dispositivo=Dispositivo.objects.filter(nombre_produc__icontains=nombre).order_by('-precio_disp')
		if orden==2 and direcc==1:
			lista_dispositivo=Dispositivo.objects.filter(nombre_produc__icontains=nombre).order_by('marca_disp')
		if orden==2 and direcc==2:
			lista_dispositivo=Dispositivo.objects.filter(nombre_produc__icontains=nombre).order_by('-marca_disp')
		if (orden==-1 or orden==1) and direcc==1:
			lista_dispositivo=Dispositivo.objects.filter(nombre_produc__icontains=nombre).order_by('nombre_produc')
		if (orden==-1 or orden==1) and direcc==2:
			lista_dispositivo=Dispositivo.objects.filter(nombre_produc__icontains=nombre).order_by('-nombre_produc')
		ctx={'q':nombre,'lista_dispositivo':lista_dispositivo,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
		return render_to_response('home/busqueda.html',ctx,context_instance=RequestContext(request))
	if request.method == 'GET':
		if 'q' in request.GET:
				nombre = request.GET['q']
				if nombre:
					lista_dispositivo=Dispositivo.objects.filter(nombre_produc__icontains=nombre)
					ctx={'q':nombre,'lista_dispositivo':lista_dispositivo,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
					return render_to_response('home/busqueda.html',ctx,context_instance=RequestContext(request))
	return HttpResponseRedirect("/home/")

def dispositivo_view(request):
	if request.method == 'GET':
		if 'd' in request.GET:
				nombre = request.GET['d']
				if nombre:
					if Dispositivo.objects.filter(nombre_produc=nombre):
						disp=Dispositivo.objects.get(nombre_produc=nombre)
						ctx={'disp':disp,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
						return render_to_response('home/dispositivo.html',ctx,context_instance=RequestContext(request))
	return render_to_response('home.html',context_instance=RequestContext(request))
############------------------------------------###############
########################## Home ###############################



#def _view(request):
#    return render_to_response('home.html',context_instance=RequestContext(request))

def getCore(request):
	if request.method == 'GET':
		variable = request.GET['cat']
		ctx={'variable':variable}
		return render_to_response('getCore.html',ctx,context_instance=RequestContext(request))
	return render_to_response('getCore.html',context_instance=RequestContext(request))


###################### registro ############################
##########------------------------------------##############
def digito_verificador(numRut):
	value = 11 - sum([ int(a)*int(b)  for a,b in zip(str(numRut).zfill(8), '32765432')])%11
	return {10: 'K', 11: '0'}.get(value, str(value))

def esRut(rut):
	try:
		val = int(rut[:-2])
	except ValueError:
		return False
	try:
		val = int(rut[-1:])
	except ValueError:
		return False
	if rut[-2:-1] == "-":
		return True
	return False

def esInt(numero):
	try:
		val = int(numero)
	except ValueError:
		return False
	return True

def register_view(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			numRut = request.POST['rut'][:-2]
			codVer = request.POST['rut'][-1:]
			if esRut(request.POST['rut']) and digito_verificador(numRut) == codVer:
				new_user = form.save()
				name = request.POST['name']
				rut = request.POST['rut']
				mail = request.POST['mail']
				new_user = User.objects.filter(username=new_user.username).update(first_name=name,last_name=rut,email=mail)
				return render_to_response('registration/register.html', {'registro':True,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')},context_instance = RequestContext(request))
			else:
				form = UserCreationForm(request.POST)
				ctx={'form': form,'error':"Debe ingresar un rut válido con el siguiente formato: XXXXXXXX-Y.",'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
				return render_to_response('registration/register.html',ctx ,context_instance = RequestContext(request))
		else:
			form = UserCreationForm(request.POST)
			return render_to_response('registration/register.html', {'form': form,'failure':True,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')},context_instance = RequestContext(request))
	else:
		form = UserCreationForm()
		return render_to_response('registration/register.html', {'form': form,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')},context_instance = RequestContext(request))

@login_required
def edprofile_view(request):
	if request.method == 'POST':
		passwd = request.POST['pass']
		if passwd:
			if request.user.check_password(passwd):
				newpass = request.POST['newpass']
				if newpass:
					newpass2 = request.POST['newpass2']
					if newpass == newpass2:
						name = request.user.first_name
						rut = request.user.last_name
						mail = request.user.email
						if request.POST['name']:
							name = request.POST['name']
						if request.POST['rut']:
							numRut = request.POST['rut'][:-2]
							codVer = request.POST['rut'][-1:]
							if esRut(request.POST['rut']) and  digito_verificador(numRut) == codVer:
								rut = request.POST['rut']
							else:
								ctx={'error':"Debe ingresar un rut válido con el siguiente formato: XXXXXXXX-Y.",'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
								return render_to_response('registration/edProfile.html', ctx,context_instance = RequestContext(request))
						if request.POST['mail']:
							mail = request.POST['mail']
						request.user.set_password(newpass)
						request.user.save()
						new_user = User.objects.filter(username=request.user.username).update(first_name=name,last_name=rut,email=mail)
						return render_to_response('registration/edProfile.html', {'success':True,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')},context_instance = RequestContext(request))
					else:
						return render_to_response('registration/edProfile.html', {'error':"Las nuevas contraseñas ingresadas no coinciden entre si.",'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')},context_instance = RequestContext(request))
				else:
					name = request.user.first_name
					rut = request.user.last_name
					mail = request.user.email
					if request.POST['name']:
						name = request.POST['name']
					if request.POST['rut']:
						numRut = request.POST['rut'][:-2]
						codVer = request.POST['rut'][-1:]
						if esRut(request.POST['rut']) and digito_verificador(numRut) == codVer:
							rut = request.POST['rut']
						else:
							return render_to_response('registration/edProfile.html', {'error':"Debe ingresar un rut válido con el siguiente formato: XXXXXXXX-Y.",'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')},context_instance = RequestContext(request))
					if request.POST['mail']:
						mail = request.POST['mail']
					new_user = User.objects.filter(username=request.user.username).update(first_name=name,last_name=rut,email=mail)
					return render_to_response('registration/edProfile.html', {'success':True},context_instance = RequestContext(request))
			else:
				return render_to_response('registration/edProfile.html', {'error':"La contraseña ingresada no es correcta.",'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')},context_instance = RequestContext(request))
		else:
			return render_to_response('registration/edProfile.html', {'error':"Debe ingresar su contraseña para realizar cualquier cambio.",'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')},context_instance = RequestContext(request))
	else:
		return render_to_response('registration/edProfile.html',{'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')},context_instance = RequestContext(request))

@login_required
def elprofile_view(request):
	if request.method == 'POST':
		new_user = User.objects.filter(username=request.user.username).delete()
		return render_to_response('registration/elProfile.html',{'success':True,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')},context_instance = RequestContext(request))
	else:
		return render_to_response('registration/elProfile.html',{'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')},context_instance = RequestContext(request))

@login_required
def profile_view(request):
	return render_to_response('registration/profile.html',{'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')},context_instance = RequestContext(request))

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
		success = request.POST['optionsRadios']
		ctx = {'success':success,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
		return render_to_response('home/carrito/formularioCarrito.html',ctx,context_instance = RequestContext(request))# Fin Menu Administrador
	return render_to_response('home/carrito/formularioCarrito.html',{'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')},context_instance = RequestContext(request))# Fin Menu Administrador


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
	return HttpResponseRedirect("/menuA/admStock/")

def admStock_view(request):
	lista_dispositivo = Dispositivo.objects.all()
	lista_subtipo = Subtipo.objects.all()
	if request.method == 'POST':
		if not request.POST['disp']:
			stockForm = abastecimientoForm() 
			ctx = {'lista_categorias': Tipo.objects.all().order_by('nombre_tipo'),'failure':"Asegurese de ingresar bien los datos",'stockForm':stockForm,'lista_sub':lista_subtipo,'lista_disp':lista_dispositivo}
			return render_to_response('home/menuA/admStock.html',ctx,context_instance=RequestContext(request))
		formulario = abastecimientoForm(request.POST)
		if formulario.is_valid():
			producto = request.POST['disp']
			cantidad = formulario.cleaned_data['cant_abast']
			fecha = formulario.cleaned_data['fecha']
			product = Producto.objects.get(id=producto)
			nuevo_abast = Abastecimiento(producto_abast = product, cant_abast = cantidad, fecha = fecha)
			stockForm = abastecimientoForm()
			nuevo_abast.save()
			success = True
			stockForm = abastecimientoForm()

			#Trigger que suma la cantidada a tabla "Dispositivo"
			dispositivo = Dispositivo.objects.get(id = producto)
			nueva_cantidad = dispositivo.cantidad_disp + cantidad
			producto_id = dispositivo.id
			update_cantidad = Dispositivo.objects.get(id = producto_id)
			update_cantidad.cantidad_disp = nueva_cantidad
			update_cantidad.save()
			disp_nueva_cant = Dispositivo.objects.get(id = producto_id)
			ctx = {'lista_categorias': Tipo.objects.all().order_by('nombre_tipo'),'success':"La base de datos ha sido actualizada",'stockForm':stockForm,'lista_sub':lista_subtipo,'lista_disp':lista_dispositivo}
		else:
			stockForm = abastecimientoForm() 
			ctx = {'failure':"Asegurese de ingresar bien los datos",'stockForm':stockForm,'lista_sub':lista_subtipo,'lista_disp':lista_dispositivo,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
	else:
		formulario = abastecimientoForm() 
		ctx = {'stockForm':formulario,'lista_sub':lista_subtipo,'lista_disp':lista_dispositivo,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
	return render_to_response('home/menuA/admStock.html',ctx,context_instance=RequestContext(request))

#### Dispositivos-------------------------------------
def admDispositivos_view(request):
	return render_to_response('home/menuA/admDispositivos/index.html',{'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')},context_instance=RequestContext(request))

def agDispositivo_view(request):# Agregar Dispositivo
	lista_dispositivos = Dispositivo.objects.all()
	if request.method == 'POST':
		formulario = dispositivoForm(request.POST,request.FILES)
		if formulario.is_valid():
			nombre = formulario.cleaned_data['nombre_produc']
			if Dispositivo.objects.filter(nombre_produc=nombre):
				failure="Ya existe un dispositivo con el nombre ingresado."
				ctx={'agregarDispositivoForm':formulario,'failure':failure}
				return render_to_response('home/menuA/admDispositivos/agDispositivo.html',ctx, context_instance = RequestContext(request))
			subtipo = formulario.cleaned_data['subtipo_disp']
			precio = formulario.cleaned_data['precio_disp']
			descripcion = formulario.cleaned_data['descrip_disp']
			destacado = formulario.cleaned_data['destacado']
			imagen = formulario.cleaned_data['imagen_disp']
			marca = formulario.cleaned_data['marca_disp']
			nuevo_dispositivo = Dispositivo(nombre_produc = nombre, subtipo_disp = subtipo,destacado = destacado, cantidad_disp = 0,precio_disp = precio,imagen_disp=imagen, descrip_disp = descripcion, marca_disp = marca)
			nuevo_dispositivo.save()
			formulario = dispositivoForm()
			success = "Dispositivo añadido a la base de datos."
			ctx = {'success':success,'agregarDispositivoForm':formulario,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
			return render_to_response('home/menuA/admDispositivos/agDispositivo.html',ctx, context_instance = RequestContext(request))
		else:
			formulario = dispositivoForm(request.POST)
			failure="Debe rellenar apropiadamente los datos."
			ctx={'agregarDispositivoForm':formulario,'failure':failure,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
			return render_to_response('home/menuA/admDispositivos/agDispositivo.html',ctx, context_instance = RequestContext(request))
	else:
		formulario = dispositivoForm()
		ctx={'agregarDispositivoForm':formulario,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
		return render_to_response('home/menuA/admDispositivos/agDispositivo.html',ctx,context_instance=RequestContext(request))

def elDispositivo_view(request):# Eliminar Dispositivo
	lista_dispositivo = Dispositivo.objects.all().order_by('nombre_produc')
	lista_subtipo = Subtipo.objects.all().order_by('nombre_subtipo')
	if request.method == 'POST':
		dispositivoEscogido = request.POST['disp_elegido']
		if dispositivoEscogido == "":
			failure = "Debe elegir el servicio a eliminar."
			success = False
		else:
			failure = False
			success = "Dispositivo eliminado de la base de datos."
			eliminar_dispositivo = Dispositivo.objects.filter(id = dispositivoEscogido).delete()
		ctx= {'success':success,'failure':failure,'lista_dispositivo':lista_dispositivo,'lista_subtipo':lista_subtipo,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
		return render_to_response('home/menuA/admDispositivos/elDispositivo.html',ctx,context_instance=RequestContext(request))
	else:
		ctx = {'lista_subtipo':lista_subtipo,'lista_dispositivo':lista_dispositivo,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
		return render_to_response('home/menuA/admDispositivos/elDispositivo.html',ctx,context_instance=RequestContext(request))

		id_disp = int(request.POST['id_dispositivo'])
		formulario = dispositivoForm(instance = Dispositivo.objetcs.get(id = id_disp))

def edDispositivo_view(request):# Editar Dispositivo
	lista = Dispositivo.objects.all().order_by('nombre_produc')
	lista_subtipo = Subtipo.objects.all().order_by('nombre_subtipo')
	if request.method == 'POST':
		seleccion = request.POST['selec']
		if seleccion == "":
			success = False
			failure = "Debe elegir el dispositivo a editar."
			ctx = {'lista':lista,'lista_subtipo':lista_subtipo,'failure':failure,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
			return render_to_response('home/menuA/admDispositivos/edDispositivo.html',ctx, context_instance = RequestContext(request))
		if seleccion == "seleccionado":
			name = request.POST['oldname']
			dispositivo = Dispositivo.objects.get(nombre_produc=name)
			formulario = dispositivoForm(request.POST,request.FILES)
			nombre = dispositivo.nombre_produc
			subtipo = dispositivo.subtipo_disp
			precio = dispositivo.precio_disp
			descripcion = dispositivo.descrip_disp
			destacado = dispositivo.destacado
			imagen = dispositivo.imagen_disp
			marca = dispositivo.marca_disp
			cambio=False
			if nombre != request.POST['nombre_produc']:
				if Dispositivo.objects.filter(nombre_produc=request.POST['nombre_produc']):
					failure="Ya existe un dispositivo con el nombre ingresado."
					ctx={'agregarDispositivoForm':formulario,'lista_subtipo':lista_subtipo,'lista':lista,'failure':failure,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
					return render_to_response('home/menuA/admDispositivos/edDispositivo.html',ctx, context_instance = RequestContext(request))
				nombre = request.POST['nombre_produc']
				cambio=True
			if subtipo != request.POST['subtipo_disp']:
				subtipo = request.POST['subtipo_disp']
				cambio=True
			if precio !=request.POST['precio_disp']:
				precio = request.POST['precio_disp']
				cambio=True
			if descripcion !=request.POST['descrip_disp']:
				descripcion = request.POST['descrip_disp']
				cambio=True
			if destacado !=request.POST['destacado']:
				destacado = request.POST['destacado']
				cambio=True
			try:
				if request.POST['imagen_disp']:
					imagen = request.POST['imagen_disp']
					cambio=True
			except:
				holi="holi"
			if marca !=request.POST['marca_disp']:
				marca = request.POST['marca_disp']
				cambio=True
			new_dispositivo = Dispositivo.objects.filter(nombre_produc=dispositivo).update(nombre_produc = nombre, subtipo_disp = subtipo,destacado = destacado, cantidad_disp = 0,precio_disp = precio,imagen_disp=imagen, descrip_disp = descripcion, marca_disp = marca)
			if cambio:
				success="El dispositivo ha sido modificado."
				failure=False
			else:
				success=False
				failure="Nada fue modificado."
			ctx={'success':success,'failure':failure,'lista_subtipo':lista_subtipo,'lista':lista,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
			return render_to_response('home/menuA/admDispositivos/edDispositivo.html',ctx,context_instance = RequestContext(request))
		else:
			seleccion = Dispositivo.objects.get(nombre_produc = seleccion)
			id_disp = seleccion.id
			formulario = dispositivoForm(instance = Dispositivo.objects.get(id = id_disp))
			ctx = {'lista':lista,'lista_subtipo':lista_subtipo,'seleccion':seleccion,'editarDispositivoForm':formulario,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
			return render_to_response('home/menuA/admDispositivos/edDispositivo.html',ctx,context_instance = RequestContext(request))
	else:
		ctx = {'lista':lista,'lista_subtipo':lista_subtipo,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
		return render_to_response('home/menuA/admDispositivos/edDispositivo.html',ctx, context_instance = RequestContext(request))

#### Equipos Armados-------------------------------------
def admEArmados_view(request):
	return render_to_response('home/menuA/admEArmados/index.html',{'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')},context_instance=RequestContext(request))

def agEquipo_view(request):# Agregar Equipo
	return render_to_response('home/menuA/admEArmados/agEquipo.html',context_instance=RequestContext(request))

def elEquipo_view(request):# Eliminar Equipo
	return render_to_response('home/menuA/admEArmados/elEquipo.html',context_instance=RequestContext(request))

def edEquipo_view(request):# Editar Equipo
	return render_to_response('home/menuA/admEArmados/edEquipo.html',context_instance=RequestContext(request))

#### Servicios Técnicos------------------------------------------
def admSTecnicos_view(request):
	return render_to_response('home/menuA/admSTecnicos/index.html',{'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')},context_instance=RequestContext(request))

def agSTecnico_view(request):# Agregar STecnico
	if request.method == 'POST':
		formulario = servicioForm(request.POST)
		if formulario.is_valid():
			nombre = formulario.cleaned_data['nombre_serv']
			if ServicioTecnico.objects.filter(nombre_serv=nombre):
				failure="Ya existe un servicio con el nombre ingresado."
				ctx={'agregarServicioForm':formulario,'failure':failure,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
				return render_to_response('home/menuA/admSTecnicos/agSTecnico.html',ctx, context_instance = RequestContext(request))
			if ServicioTecnico.objects.filter(nombre_serv=nombre):
				failure="Ya existe un servicio con el nombre ingresado."
				formulario = servicioForm(request.POST)
				ctx={'agregarServicioForm':formulario,'failure':failure,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
				return render_to_response('home/menuA/admSTecnicos/agSTecnico.html',ctx, context_instance = RequestContext(request))
			precio = formulario.cleaned_data['precio_serv']
			descripcion = formulario.cleaned_data['descrip_serv']
			nuevo_servicio = ServicioTecnico(nombre_serv = nombre, precio_serv = precio, descrip_serv = descripcion)
			nuevo_servicio.save()
			formulario = servicioForm()
			success = "Servicio añadido a la base de datos."
			ctx = {'success':success,'agregarServicioForm':formulario,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
			return render_to_response('home/menuA/admSTecnicos/agSTecnico.html',ctx, context_instance = RequestContext(request))
		else:
			formulario = servicioForm(request.POST)
			failure="Debe rellenar apropiadamente los datos."
			ctx={'agregarServicioForm':formulario,'failure':failure,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
			return render_to_response('home/menuA/admSTecnicos/agSTecnico.html',ctx, context_instance = RequestContext(request))
	else:
		formulario = servicioForm()
		ctx={'agregarServicioForm':formulario,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
		return render_to_response('home/menuA/admSTecnicos/agSTecnico.html',ctx,context_instance=RequestContext(request))

def elSTecnico_view(request):# Eliminar STecnico
	lista_servicios = ServicioTecnico.objects.all().order_by('nombre_serv')
	if request.method == 'POST':
		servicioEscogido = request.POST['servicio']
		if servicioEscogido == "VACIO":
			failure = "Debe elegir el servicio a eliminar."
			success = False
		else:
			failure = False
			eliminar_servicio = ServicioTecnico.objects.filter(nombre_serv = servicioEscogido).delete()
			success = "Servicio eliminado de la base de datos."
		ctx= {'success':success, 'lista_servicios':lista_servicios,'failure':failure,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
		return render_to_response('home/menuA/admSTecnicos/elSTecnico.html',ctx, context_instance = RequestContext(request))
	else:
		ctx = {'lista_servicios':lista_servicios,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
		return render_to_response('home/menuA/admSTecnicos/elSTecnico.html',ctx,context_instance = RequestContext(request))

def edSTecnico_view(request):# Editar STecnico
	lista = ServicioTecnico.objects.all().order_by('nombre_serv')
	if request.method == 'POST':
		seleccion = request.POST['selec']
		if seleccion == "":
			success = False
			failure = "Debe elegir el servicio a editar."
			ctx = {'lista':lista,'failure':failure,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
			return render_to_response('home/menuA/admSTecnicos/edSTecnico.html',ctx, context_instance = RequestContext(request))
		if seleccion == "seleccionado":
			name = request.POST['name']
			servicio = ServicioTecnico.objects.get(nombre_serv=name)
			newname = servicio.nombre_serv
			precio = servicio.precio_serv
			descrip = servicio.descrip_serv
			if request.POST['newname']:
				if ServicioTecnico.objects.filter(nombre_serv=request.POST['newname']):
					failure="Ya existe un servicio con el nombre ingresado."
					ctx={'lista':lista,'failure':failure,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
					return render_to_response('home/menuA/admSTecnicos/edSTecnico.html',ctx, context_instance = RequestContext(request))
				newname = request.POST['newname']
			if request.POST['precio']:
				if esInt(request.POST['precio']) and (int(request.POST['precio'])>0):
					precio = request.POST['precio']
				else:
					failure = "El precio debe ser un número mayor a cero."
					ctx={'lista':lista,'failure':failure,'seleccion':servicio,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
					return render_to_response('home/menuA/admSTecnicos/edSTecnico.html',ctx, context_instance = RequestContext(request))
			if request.POST['descrip']:
				descrip = request.POST['descrip']
			new_servicio = ServicioTecnico.objects.filter(nombre_serv=servicio).update(nombre_serv=newname,precio_serv=precio,descrip_serv=descrip)
			if request.POST['newname'] or request.POST['precio'] or request.POST['descrip']:
				success="El servicio ha sido modificado."
				failure=False
			else:
				success=False
				failure="Nada fue modificado."
			ctx={'success':success,'lista':lista,'failure':failure,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
			return render_to_response('home/menuA/admSTecnicos/edSTecnico.html',ctx,context_instance = RequestContext(request))
		else:
			seleccion = ServicioTecnico.objects.get(nombre_serv = seleccion)
			ctx = {'lista':lista,'seleccion':seleccion,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
			return render_to_response('home/menuA/admSTecnicos/edSTecnico.html',ctx,context_instance = RequestContext(request))
	else:
		ctx = {'lista':lista,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
		return render_to_response('home/menuA/admSTecnicos/edSTecnico.html',ctx, context_instance = RequestContext(request))

#### Compatibilidades------------------------------------------
def admCompatibilidades_view(request):
	return render_to_response('home/menuA/admCompatibilidades/index.html',{'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')},context_instance=RequestContext(request))

def agCompatibilidad_view(request):# Agregar Compatibilidad
	lista_dispositivo = Dispositivo.objects.all()
	lista_subtipo = Subtipo.objects.all()
	lista_compt = Compatibilidad.objects.all()
	
	if request.method =='POST':
		dispositivo_id = request.POST['disp_elegido']
		subtipo_escogido = request.POST.getlist('subtipo_escogido')

		if ((dispositivo_id == '-1') or (subtipo_escogido == [])):
			failure = "Debe elegir un dispositivo y al menos un subtipo"
			ctx = {'lista_dispositivo':lista_dispositivo, 'lista_subtipo':lista_subtipo,'failure':failure,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
			return render_to_response('home/menuA/admCompatibilidades/agCompatibilidad.html',ctx,context_instance = RequestContext(request))

		#Se selecciona el dispositivo elegido de la base de datos
		disp = Dispositivo.objects.get(id = dispositivo_id)

		#Se crea una lista con el dispositivo seleccionado y sus subtipos previamente compatibles
		lista_compat_disp = Compatibilidad.objects.filter(dispositivo = dispositivo_id)
		
		lista_subtipo_id = []
		for id_subtipo in lista_compat_disp:
			lista_subtipo_id.append(id_subtipo.subtipo.id)
		else:
			for subt in subtipo_escogido:
				subtipo = Subtipo.objects.get(id = subt)
				compatibilidad = Compatibilidad(dispositivo = disp, subtipo = subtipo)
				compatibilidad.save()
			success = "Compatibilidad(es) agregada(s) a la base de datos"
			ctx = {'lista_compt':lista_compt,'success':success,'dispositivo_comp':dispositivo_id,'subtipo_escogido':subtipo_escogido,'lista_dispositivo':lista_dispositivo, 'lista_subtipo':lista_subtipo,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
	else:
		lista_dispositivo = Dispositivo.objects.all()
		lista_subtipo = Subtipo.objects.all()
		ctx = {'lista_dispositivo':lista_dispositivo, 'lista_subtipo':lista_subtipo,'lista_compt':lista_compt,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
	return render_to_response('home/menuA/admCompatibilidades/agCompatibilidad.html',ctx,context_instance = RequestContext(request))

def elCompatibilidad_view(request):# Eliminar Compatibilidad
	lista_dispositivo_compat = Compatibilidad.objects.all()
	lista_subtipo = Subtipo.objects.all()
	# lista_subtipo = Subtipo.objects.all()
	# lista_dispositivo = Dispositivo.objects.all()

	#Ponemos todos los dispositivos compatibles en la lista
	lista_disp_compat = []
	lista_dispositivo = []
	for disp in lista_dispositivo_compat:
		lista_disp_compat.append(disp.dispositivo.id)

	lista_disp_compat = list(set(lista_disp_compat))

	for disp in lista_disp_compat:
		lista_dispositivo.append(Dispositivo.objects.get(id = disp))	

	if request.method == 'POST':
		lista_subtipos = request.POST.getlist('subtipos_compat')
		disp_elegido = request.POST['disp_compat']


		if (disp_elegido == '-1' or lista_subtipos == []):
			failure = "Debe elegir subtipos compatibles para eliminar"
			ctx = {'lista_dispositivo':lista_dispositivo,'failure':failure, 'lista_subtipo':lista_subtipo,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
			return render_to_response('home/menuA/admCompatibilidades/elCompatibilidad.html',ctx,context_instance = RequestContext(request))

		lista_subtipos_ids = []

		#Se almacenan lso ids de subtipos compatibles en una lista, debido a que dan problemas al manejarlos con el getlist
		for x in lista_subtipos:
			lista_subtipos_ids.append(int(x))

		#Borramos la compatibilidad para cada subtipo escogido con el dispositivo escogido
		for subt in lista_subtipos_ids:
			subtipo = Subtipo.objects.get(id = subt)
			disp = Dispositivo.objects.get(id = disp_elegido)
			query_borrar = Compatibilidad.objects.get(dispositivo = disp, subtipo = subtipo).delete()

		lista_dispositivo_compat = Compatibilidad.objects.all()
		# lista_subtipo = Subtipo.objects.all()
		# lista_dispositivo = Dispositivo.objects.all()

		#Ponemos todos los dispositivos compatibles en la lista
		lista_disp_compat = []
		lista_dispositivo = []
		for disp in lista_dispositivo_compat:
			lista_disp_compat.append(disp.dispositivo.id)

		lista_disp_compat = list(set(lista_disp_compat))

		for disp in lista_disp_compat:
			lista_dispositivo.append(Dispositivo.objects.get(id = disp))	

		ctx = {'lista_dispositivo':lista_dispositivo,'success':"Compatibilidad(es) eliminada(s) de la base de datos", 'lista_subtipo':lista_subtipo,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
	else:
		ctx = {'lista_dispositivo':lista_dispositivo, 'lista_subtipo':lista_subtipo,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
	return render_to_response('home/menuA/admCompatibilidades/elCompatibilidad.html',ctx,context_instance = RequestContext(request))

def agIncompatibilidad_view(request):# Agregar Incompatibilidad
	lista_dispositivo = Dispositivo.objects.all()
	lista_subtipo = Subtipo.objects.all()
	incompatibilidad = Incompatibilidad.objects.all()
	compatibilidad = Compatibilidad.objects.all()

	if request.method =='POST':
		dispositivo_id = request.POST['disp_elegido']
		dispositivo_incompat_ids = request.POST.getlist('disp_incompatibles')
		#Si no se elige alguno de los dos campos
		if (dispositivo_id == '-1' or dispositivo_incompat_ids==[]):
			failure = "Debe elegir un dispositivo y al menos otro dispositivo con que sea incompatible"
			ctx = {'lista_dispositivo':lista_dispositivo, 'lista_subtipo':lista_subtipo,'failure':failure,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
			return render_to_response('home/menuA/admCompatibilidades/agIncompatibilidad.html',ctx,context_instance = RequestContext(request))

		else:
			for disp in dispositivo_incompat_ids:
				dispositivo_id2 = int(disp)


				#Obtenemos disp1 y disp2, y los registramos en la tabla incompatibilidad
				disp1 = Dispositivo.objects.get(id = dispositivo_id)
				disp2 = Dispositivo.objects.get(id = dispositivo_id2)
				incompatibilidad = Incompatibilidad(dispositivo1 = disp1, dispositivo2 = disp2)
				incompatibilidad.save()
			success = "Incompatibilidad(es) agregada(s) a la base de datos"
			ctx = {'success':success,'dispositivo_incomp':dispositivo_id,'lista_dispositivo':lista_dispositivo, 'lista_subtipo':lista_subtipo,'incompatibilidad':incompatibilidad,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
	else:
		ctx = {'lista_dispositivo':lista_dispositivo, 'lista_subtipo':lista_subtipo,'incompatibilidad':incompatibilidad,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
	return render_to_response('home/menuA/admCompatibilidades/agIncompatibilidad.html',ctx,context_instance = RequestContext(request))

def elIncompatibilidad_view(request):# Eliminar Incompatibilidad
	lista_dispositivo_incompat = Incompatibilidad.objects.all()
	lista_subtipo = Subtipo.objects.all()
	lista_disp1_incompat = []
	lista_disp2_incompat = []
	lista_dispositivo = []
	for disp1 in lista_dispositivo_incompat:
		lista_disp1_incompat.append(disp1.dispositivo1.id)

	for disp2 in lista_dispositivo_incompat:
		lista_disp2_incompat.append(disp2.dispositivo2.id)

	lista_disp_incompatibles = list(set(lista_disp1_incompat + lista_disp2_incompat))

	lista_dispositivo1 = []
	for dispo in lista_disp_incompatibles:
		disp = Dispositivo.objects.get(id = dispo)
		lista_dispositivo1.append(disp)

	if request.method == 'POST':
		lista_disp = request.POST.getlist('disp_incompatibles')
		disp_elegido = request.POST['disp_elegido']

		if (disp_elegido == '-1' or lista_disp == []):
			failure = "Debe elegir dispositivos incompatibles para eliminar"
			ctx = {'lista_dispositivo1':lista_dispositivo1,'failure':failure, 'lista_subtipo':lista_subtipo,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
			return render_to_response('home/menuA/admCompatibilidades/elIncompatibilidad.html',ctx,context_instance = RequestContext(request))

		lista_dispositivo = []
		#Almacenamos los ids del getlist en una lista, de otro modo dan problemas
		for x in lista_disp:
			lista_dispositivo.append(int(x))

		#Borramos la incompatibilidad para cada subtipo escogido con el dispositivo escogido
		for disp in lista_dispositivo:
			id_incompatible = disp
			disp_inicial = Dispositivo.objects.get(id = disp_elegido)
			dispositivo_incompat = Dispositivo.objects.get(id = id_incompatible)
			intento_1 = Incompatibilidad.objects.filter(dispositivo1 = disp_inicial, dispositivo2 = dispositivo_incompat)
			intento_2 = Incompatibilidad.objects.filter(dispositivo1 =  dispositivo_incompat, dispositivo2 = disp_inicial)
			
			#Con .count(), vemos si existen dichas compatibilidades. No llama a error si es que no existen, por eso se utiliza.
			if intento_1.count()>0:
				intento_1.delete()
				pass
			else:
				intento_2.delete();
		lista_dispositivo_incompat = Incompatibilidad.objects.all()
		
		lista_disp1_incompat = []
		lista_disp2_incompat = []
		lista_dispositivo = []
		for disp1 in lista_dispositivo_incompat:
			lista_disp1_incompat.append(disp1.dispositivo1.id)

		for disp2 in lista_dispositivo_incompat:
			lista_disp2_incompat.append(disp2.dispositivo2.id)

		#Mezclamos las incompatibilidades hacia los dos lados, y seleccionamos los ids de dispositivos diferentes
		lista_disp_incompatibles = list(set(lista_disp1_incompat + lista_disp2_incompat))

		lista_dispositivo1 = []
		for dispo in lista_disp_incompatibles:
			disp = Dispositivo.objects.get(id = dispo)
			lista_dispositivo1.append(disp)

		ctx = {'lista_dispositivo':lista_dispositivo,'success':"Incompatibilidad(es) eliminada(s) de la base de datos",'lista_dispositivo1':lista_dispositivo1, 'lista_subtipo':lista_subtipo,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
	else:
		ctx = {'lista_dispositivo1':lista_dispositivo1, 'lista_subtipo':lista_subtipo,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
	return render_to_response('home/menuA/admCompatibilidades/elIncompatibilidad.html',ctx,context_instance = RequestContext(request))

#### Tipos y Subtipos-------------------------------------
def admTySubtipos_view(request):
	return render_to_response('home/menuA/admTySubtipos/index.html',{'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')},context_instance=RequestContext(request))

def agTipo_view(request):# Agregar Tipo
	global lista_tipos
	lista_tipos = Tipo.objects.all()
	if request.method == 'POST':
		formulario = tipoForm(request.POST)
		if formulario.is_valid():
			success = "Tipo añadido a la base de datos."
			nuevo_nombre = formulario.cleaned_data['nombre_tipo']
			si_no_armado = formulario.cleaned_data['armado_equipo']
			if Tipo.objects.filter(nombre_tipo=nuevo_nombre):
				failure="Ya existe un tipo con el nombre ingresado."
				ctx={'agregarTipoForm':formulario,'failure':failure,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
				return render_to_response('home/menuA/admTySubtipos/agTipo.html',ctx, context_instance = RequestContext(request))
			if Tipo.objects.filter(nombre_tipo=nuevo_nombre):
				failure="Ya existe un tipo con el nombre ingresado."
				formulario = tipoForm(request.POST)
				ctx={'agregarTipoForm':formulario,'failure':failure,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
				return render_to_response('home/menuA/admTySubtipos/agTipo.html',ctx, context_instance = RequestContext(request))
			nuevo_tipo = Tipo(nombre_tipo = nuevo_nombre)
			nuevo_tipo.save()
			nuevo_tipo_form = tipoForm()
			ctx = {'success':success,'agregarTipoForm':nuevo_tipo_form,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
			return render_to_response('home/menuA/admTySubtipos/agTipo.html',ctx, context_instance = RequestContext(request))
		else:
			formulario = tipoForm(request.POST)
			failure="Debe rellenar apropiadamente los datos."
			ctx={'agregarTipoForm':formulario,'failure':failure,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
			return render_to_response('home/menuA/admTySubtipos/agTipo.html',ctx, context_instance = RequestContext(request))
	else:
		formulario = tipoForm()
		ctx={'agregarTipoForm':formulario,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
		return render_to_response('home/menuA/admTySubtipos/agTipo.html',ctx, context_instance = RequestContext(request))

def elTipo_view(request):# Eliminar Tipo
	lista_tipos = Tipo.objects.all().order_by('nombre_tipo')
	if request.method == 'POST':
		tipoEscogido = request.POST['tipo']
		if tipoEscogido == "VACIO":
			failure = "Debe elegir el tipo a eliminar."
			success = False
		else:
			failure = False
			eliminar_tipo = Tipo.objects.filter(id = tipoEscogido).delete()
			success = "Tipo eliminado de la base de datos."
		ctx= {'success':success, 'lista_tipos':lista_tipos,'failure':failure,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
		return render_to_response('home/menuA/admTySubtipos/elTipo.html',ctx, context_instance = RequestContext(request))
	else:
		ctx = {'lista_tipos':lista_tipos,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
		return render_to_response('home/menuA/admTySubtipos/elTipo.html',ctx,context_instance = RequestContext(request))

def edTipo_view(request):# Editar Tipo
	lista = Tipo.objects.all().order_by('nombre_tipo')
	if request.method == 'POST':
		seleccion = request.POST['selec']
		if seleccion == "":
			success = False
			failure = "Debe elegir el tipo a editar."
			ctx = {'lista':lista,'failure':failure,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
			return render_to_response('home/menuA/admTySubtipos/edTipo.html',ctx, context_instance = RequestContext(request))
		if seleccion == "seleccionado":
			name = request.POST['name']
			armado = request.POST['armado_equipo']
			tipo = Tipo.objects.get(nombre_tipo=name)
			newname = tipo.nombre_tipo
			if request.POST['newname']:
				if Tipo.objects.filter(nombre_tipo=request.POST['newname']):
					failure="Ya existe un tipo con el nombre ingresado."
					ctx={'lista':lista,'failure':failure,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
					return render_to_response('home/menuA/admTySubtipos/edTipo.html',ctx, context_instance = RequestContext(request))
				newname = request.POST['newname']
			new_tipo = Tipo.objects.filter(nombre_tipo=tipo).update(nombre_tipo=newname)
			new_choice = Tipo.objects.filter(nombre_tipo=tipo).update(armado_equipo=armado)
			if name and armado:
				success="El tipo ha sido modificado."
				failure=False
			else:
				success=False
				failure="Nada fue modificado."
			ctx={'success':success,'lista':lista,'failure':failure,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
			return render_to_response('home/menuA/admTySubtipos/edTipo.html',ctx,context_instance = RequestContext(request))
		else:
			seleccion = Tipo.objects.get(nombre_tipo = seleccion)
			ctx = {'lista':lista,'seleccion':seleccion,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
			return render_to_response('home/menuA/admTySubtipos/edTipo.html',ctx,context_instance = RequestContext(request))
	else:
		ctx = {'lista':lista,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
		return render_to_response('home/menuA/admTySubtipos/edTipo.html',ctx, context_instance = RequestContext(request))

def agSTipo_view(request):# Agregar Subtipo
	global lista_subtipos
	lista_tipos = Tipo.objects.all().order_by('nombre_tipo')
	if request.method == 'POST':
		formulario = subtipoForm(request.POST)
		if formulario.is_valid():
			nuevo_nombre = formulario.cleaned_data['nombre_subtipo']
			if Subtipo.objects.filter(nombre_subtipo=nuevo_nombre):
				failure="Ya existe un subtipo con el nombre ingresado."
				formulario = subtipoForm(request.POST)
				ctx={'agregarSubtipoForm':formulario,'failure':failure,'lista_tipos':lista_tipos,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
				return render_to_response('home/menuA/admTySubtipos/agSTipo.html',ctx, context_instance = RequestContext(request))
			tipo_asignado = formulario.cleaned_data['tipo_padre']
			subtipo_asignado = formulario.cleaned_data['subtipo_padre']

			if tipo_asignado or subtipo_asignado:
				#Si se eligio Tipo y Subtipo, se lanza error
				if tipo_asignado and subtipo_asignado:
					failure="Debe elegir un tipo o un subtipo, no ambas."
					formulario = subtipoForm(request.POST)
					ctx = {'failure':failure,'agregarSubtipoForm':formulario,'lista_tipos':lista_tipos,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
					return render_to_response('home/menuA/admTySubtipos/agSTipo.html',ctx, context_instance = RequestContext(request))
				#Se revisa si subtipo agregado pertenece a un tipo o a un subtipo
				
				if tipo_asignado:
					nuevo_subtipo = Subtipo(nombre_subtipo = nuevo_nombre, tipo_padre = tipo_asignado)
				elif subtipo_asignado:
					nuevo_subtipo = Subtipo(nombre_subtipo = nuevo_nombre, subtipo_padre = subtipo_asignado)
				
				#Almacenamos en la base de datos
				nuevo_subtipo.save()
				formulario = subtipoForm()
				success = "subtipo añadido a la base de datos."
				ctx = {'success':success,'agregarSubtipoForm':formulario,'lista_tipos':lista_tipos,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
				return render_to_response('home/menuA/admTySubtipos/agSTipo.html',ctx, context_instance = RequestContext(request))
			else:
				failure="Debe elegir un tipo o un subtipo padre."
				formulario = subtipoForm(request.POST)
				ctx = {'failure':failure,'agregarSubtipoForm':formulario,'lista_tipos':lista_tipos,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
				return render_to_response('home/menuA/admTySubtipos/agSTipo.html',ctx, context_instance = RequestContext(request))
		else:
			formulario = subtipoForm(request.POST)
			failure="Debe rellenar apropiadamente los datos."
			ctx = {'failure':failure,'agregarSubtipoForm':formulario,'lista_tipos':lista_tipos,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
			return render_to_response('home/menuA/admTySubtipos/agSTipo.html',ctx, context_instance = RequestContext(request))
	else:
		formulario = subtipoForm()
		ctx ={'agregarSubtipoForm':formulario,'lista_tipos':lista_tipos,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
		return render_to_response('home/menuA/admTySubtipos/agSTipo.html',ctx,context_instance=RequestContext(request))

def elSTipo_view(request):# Eliminar Subtipo
	lista_subtipos = Subtipo.objects.all().order_by('nombre_subtipo')
	if request.method == 'POST':
		subtipoEscogido = request.POST['subtipo']
		if subtipoEscogido == "VACIO":
			success = False
			failure = "Debe elegir el subtipo a eliminar."
		else:
			failure = False
			error="holi"
			eliminar_subtipo = Subtipo.objects.filter(id = subtipoEscogido).delete()
			success = "Subtipo eliminado de la base de datos."
		ctx= {'success':success, 'lista_subtipos':lista_subtipos,'failure':failure,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
		return render_to_response('home/menuA/admTySubtipos/elSTipo.html',ctx, context_instance = RequestContext(request))
	else:
		ctx = {'lista_subtipos':lista_subtipos,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
		return render_to_response('home/menuA/admTySubtipos/elSTipo.html',ctx,context_instance=RequestContext(request))

def edSTipo_view(request):# Editar Subtipo
	lista = Subtipo.objects.all().order_by('nombre_subtipo')
	lista_tipo = Tipo.objects.all()
	if request.method == 'POST':
		seleccion = request.POST['selec']
		if seleccion == "":
			success = False
			failure = "Debe elegir el subtipo a editar."
			ctx = {'lista':lista,'lista_tipo':lista_tipo,'failure':failure,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
			return render_to_response('home/menuA/admTySubtipos/elSTipo.html',ctx, context_instance = RequestContext(request))
		if seleccion == "seleccionado":
			name = request.POST['name']
			subtipo = Subtipo.objects.get(nombre_subtipo=name)
			newname = subtipo.nombre_subtipo
			if request.POST['newname']:
				if Subtipo.objects.filter(nombre_subtipo=request.POST['newname']):
					failure="Ya existe un subtipo con el nombre ingresado."
					ctx={'lista':lista,'lista_tipo':lista_tipo,'failure':failure,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
					return render_to_response('home/menuA/admTySubtipos/edSTipo.html',ctx, context_instance = RequestContext(request))
				newname = request.POST['newname']
			new_tipo = Subtipo.objects.filter(nombre_subtipo=subtipo).update(nombre_subtipo=newname)
			if request.POST['newname']:
				success="El tipo ha sido modificado."
				failure=False
			else:
				success=False
				failure="Nada fue modificado."
			ctx={'success':success,'lista':lista,'failure':failure,'lista_tipo':lista_tipo,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
			return render_to_response('home/menuA/admTySubtipos/edSTipo.html',ctx,context_instance = RequestContext(request))
		else:
			seleccion = Subtipo.objects.get(nombre_subtipo = seleccion)
			ctx = {'lista':lista,'seleccion':seleccion,'lista_tipo':lista_tipo,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
			return render_to_response('home/menuA/admTySubtipos/edSTipo.html',ctx,context_instance = RequestContext(request))
	else:
		ctx = {'lista':lista,'lista_tipo':lista_tipo,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
		return render_to_response('home/menuA/admTySubtipos/edSTipo.html',ctx, context_instance = RequestContext(request))

#### Empleados---------------------------------------
def admEmpleados_view(request):
	return render_to_response('home/menuA/admEmpleados/index.html',{'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')},context_instance=RequestContext(request))

def agEmpleado_view(request):# Agregar Empleado
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			numRut = request.POST['rut'][:-2]
			codVer = request.POST['rut'][-1:]
			if esRut(request.POST['rut']) and digito_verificador(numRut) == codVer:
				new_user = form.save()
				name = request.POST['name']
				rut = request.POST['rut']
				mail = request.POST['mail']
				if request.POST['optionsRadios'] == "si":
					new_user = User.objects.filter(username=new_user.username).update(first_name=name,last_name=rut,email=mail,is_staff=True,is_superuser=True)
				else:
					new_user = User.objects.filter(username=new_user.username).update(first_name=name,last_name=rut,email=mail,is_staff=True)
				form = UserCreationForm()
				ctx={'success':"Empleado añadido a la base de datos.",'form':form,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
				return render_to_response('home/menuA/admEmpleados/agEmpleado.html',ctx,context_instance = RequestContext(request))
			else:
				form = UserCreationForm(request.POST)
				ctx={'form': form,'failure':"Debe ingresar un rut válido con el siguiente formato: XXXXXXXX-Y.",'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
				return render_to_response('home/menuA/admEmpleados/agEmpleado.html',ctx,context_instance = RequestContext(request))
		else:
			form = UserCreationForm(request.POST)
			ctx={'form': form,'failure':"Ingrese los datos siguiendo las instrucciones.",'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
			return render_to_response('home/menuA/admEmpleados/agEmpleado.html',ctx,context_instance = RequestContext(request))
	else:
		form = UserCreationForm()
		return render_to_response('home/menuA/admEmpleados/agEmpleado.html', {'form': form,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')},context_instance = RequestContext(request))

def elEmpleado_view(request):# Editar Empleado
	lista_empleados = User.objects.all().order_by('first_name')
	if request.method == 'POST':
		empleadoEscogido = request.POST['empleado']
		if empleadoEscogido == "VACIO":
			failure = "Debe elegir el empleado a eliminar."
			success = False
		else:
			failure = False
			new_user = User.objects.filter(username=empleadoEscogido).delete()
			success = "Empleado eliminado de la base de datos."
		ctx= {'success':success, 'lista_empleados':lista_empleados,'failure':failure,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
		return render_to_response('home/menuA/admEmpleados/elEmpleado.html',ctx, context_instance = RequestContext(request))
	else:
		ctx = {'lista_empleados':lista_empleados,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
		return render_to_response('home/menuA/admEmpleados/elEmpleado.html',ctx,context_instance = RequestContext(request))

def edEmpleado_view(request):# Eliminar Empleado
	lista_empleados = User.objects.all().order_by('first_name')
	if request.method == 'POST':
		empleadoEscogido = request.POST['empleado']
		if empleadoEscogido == "VACIO":
			failure = "Debe elegir el empleado a eliminar."
			success = False
		else:
			failure = False
			empleado = User.objects.get(username=empleadoEscogido)
			name = empleado.first_name
			rut = empleado.last_name
			mail = empleado.email
			is_staff = empleado.is_staff
			if request.POST['name']:
				name = request.POST['name']
			if request.POST['rut']:
				numRut = request.POST['rut'][:-2]
				codVer = request.POST['rut'][-1:]
				if esRut(request.POST['rut']) and  digito_verificador(numRut) == codVer:
					rut = request.POST['rut']
				else:
					ctx={'failure':"Debe ingresar un rut válido con el siguiente formato: XXXXXXXX-Y.",'lista_empleados':lista_empleados,'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')}
					return render_to_response('home/menuA/admEmpleados/edEmpleado.html',ctx,context_instance = RequestContext(request))
			if request.POST['mail']:
				mail = request.POST['mail']
			if request.POST['optionsRadios'] == "si":
				new_user = User.objects.filter(username=empleadoEscogido).update(first_name=name,last_name=rut,email=mail,is_staff=True,is_superuser=True)
			if request.POST['optionsRadios'] == "no":
				new_user = User.objects.filter(username=empleadoEscogido).update(first_name=name,last_name=rut,email=mail,is_staff=True,is_superuser=False)
			else:
				new_user = User.objects.filter(username=empleadoEscogido).update(first_name=name,last_name=rut,email=mail,is_staff=True)
			ctx={'lista_categorias': Tipo.objects.all().order_by('nombre_tipo'),'success':"El empleado ha sido modificado.",'lista_empleados':lista_empleados}
			return render_to_response('home/menuA/admEmpleados/edEmpleado.html',ctx,context_instance = RequestContext(request))
		ctx= {'lista_categorias': Tipo.objects.all().order_by('nombre_tipo'),'success':success, 'lista_empleados':lista_empleados,'failure':failure}
		return render_to_response('home/menuA/admEmpleados/edEmpleado.html',ctx, context_instance = RequestContext(request))
	else:
		ctx = {'lista_categorias': Tipo.objects.all().order_by('nombre_tipo'),'lista_empleados':lista_empleados}
		return render_to_response('home/menuA/admEmpleados/edEmpleado.html',ctx,context_instance = RequestContext(request))

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
	return render_to_response('home/menuE.html',{'lista_categorias': Tipo.objects.all().order_by('nombre_tipo')},context_instance=RequestContext(request))






#################################################################################
############   FUNCIONES EXTERNAS, NO RETORNAN NINGÚN TEMPLATE   ################
#################################################################################

#Función que consulta si el id que se le da tiene subtipos padres.
#OJO. retorna una lista con todos los subtipos padres, donde el primer elemento es el tipo_padre!
def padres(lista,id_subtipo):
	lista.append(id_subtipo)	
	query_subtipo_padre = Subtipo.objects.get(id = id_subtipo)

	if query_subtipo_padre.subtipo_padre:
		id_padre = query_subtipo_padre.subtipo_padre.id
		lista.append(id_padre)
		#Volvemos a ejecutar a funcion padre con el siguiente subtipo
		return padres(lista,id_padre)
	else:
		lista = eliminar_duplicados(lista, idfun = None)
		id_tipo_padre = query_subtipo_padre.tipo_padre.id
		#Insertamos tipo_padre al principio de la lista
		lista.insert(0,id_tipo_padre)
		return lista

#Función que elimina elementos duplicados manteniendo el orden de la valores en que fueron ingresados
def eliminar_duplicados(seq, idfun = None): 
   # order preserving
   	if idfun is None:
   	   def idfun(x): return x
	   seen = {}
	   result = []
	   for item in seq:
	       marker = idfun(item)
	       if marker in seen: continue
	       seen[marker] = 1
	       result.append(item)
	   return result



####Función que retorna una lista con el objeto tipo_padre y los objetos subtipo_padre dado un subtipo.
def encontrar_padres(id_subtipo):
	lista_p = []

	#En lista_padress_ se almacenan todos los padres del subtipo escogido
	lista_padres = padres(lista_p, id_subtipo = id_subtipo)
	lista_objeto_padre = []

	#Invertimos la lista, para que quede en orden desde el padre mayor, al padre menor:
	lista_padres.reverse()

	tipo = Tipo.objects.get(id = lista_padres.pop(-1))
	lista_objeto_padre.append(tipo)
	lista_objeto_padre

	#Almacenamos los objetos "subtipo" en lista_objeto_padre
	for padre in lista_padres:
		subtipo = Subtipo.objects.get(id = padre)
		lista_objeto_padre.append(subtipo)

	return lista_objeto_padre

# lista HijosDeUnSubtipo(Subtipo X)
# lista vacia
# for (sub in Subtipos)
# if (padre(sub) == X)
# lista.add(sub)
# return lista

def hijos_directos(id_subtipo):
	lista = []
	lista_subtipos = Subtipo.objects.all()
	subtipo_escogido = Subtipo.objects.get(id = id_subtipo)

	for subtipo in lista_subtipos:
		if (subtipo.subtipo_padre == subtipo_escogido):
			lista.append(subtipo)
	return lista


def descendientes_de_subtipo(id_subtipo):
	lista = []
	lista_subtipo = Subtipo.objects.all()
	lista_p = []

	for subtipo in lista_subtipo:
		#Considerar que el primer elemento, es el tipo. Y que todos son objetos
		lista_padres = encontrar_padres(id_subtipo = subtipo.id)
		#Eliminamos el tipo padre de la lista
		lista_padres.pop(0)
		for padre in lista_padres:
			if (padre.id == id_subtipo):
				lista.append(subtipo)
	return lista

# lista DescendientesDeUnSubTipo(Subtipo X)
	# lista vacia
	# for (sub in Subtipos)
		# for (padreSub in sub.padres)
		# if (padreSub == X)
			# lista.add(sub)
			# return lista



# #Si retorna None, no tiene subtipo padre
# def subt_padre(id_subtipo):
# 	subtipo = Subtipo.objects.get(id = id_subtipo)

# 	if subtipo.subtipo_padre:
# 		print "subtipo padre ",subtipo.subtipo_padre
# 		id_padre = subtipo.subtipo_padre.id
# 		return id_padre
# 	else:
# 		return None





#################################################################################
########################    FUNCIONES CON AJAX   ################################
#################################################################################

def ajax_validar_disp_diferente(request):

	if request.method == 'POST':
		id_disp = request.POST['id']
		lista_dispositivo =  Dispositivo.objects.all()
		lista_subtipo = Subtipo.objects.all()
		dispositivo_anulado = Dispositivo.objects.get(id = id_disp)

		query_incompat1 = Incompatibilidad.objects.filter(dispositivo1 = dispositivo_anulado)
		query_incompat2 = Incompatibilidad.objects.filter(dispositivo2 = dispositivo_anulado)

		if (query_incompat1 or query_incompat2):

			#Lista que almacena todos los ids de dispositivos2 incompatibles con dispositivo escogido
			lista_disp_incompat1 = []
			#Lista que almacena todos los ids de dispositivos1 incompatibles con dispositivo escogido
			lista_disp_incompat2 = []

			if query_incompat1:
				for incompat1 in query_incompat1:
					lista_disp_incompat1.append(incompat1.dispositivo2.id)
			if query_incompat2:
				for incompat2 in query_incompat2:
					lista_disp_incompat2.append(incompat2.dispositivo1.id)	

			#unimos las dos listas, obteniendo todos los ids incompatibles con el disp elegido, pueden haber repetidos, por eso usamos set
			dispositivos_incompatibles = list(set(lista_disp_incompat1 + lista_disp_incompat2))

			ctx = {'lista_dispositivo':lista_dispositivo, 'lista_subtipo':lista_subtipo, 'dispositivo_anulado':dispositivo_anulado, 'dispositivos_incompatibles':dispositivos_incompatibles}
			return render_to_response('ajax/validar_dispositivo_diferente.html',ctx,context_instance = RequestContext(request))
		else:
			ctx = {'lista_dispositivo':lista_dispositivo, 'lista_subtipo':lista_subtipo, 'dispositivo_anulado':dispositivo_anulado}
			return render_to_response('ajax/validar_dispositivo_diferente.html',ctx,context_instance = RequestContext(request))
	else:
		pass

def ajax_validar_disp_diferente_comp(request):
	if request.method == 'POST':
		id_disp = request.POST['id']
		lista_dispositivo =  Dispositivo.objects.all()
		lista_subtipo = Subtipo.objects.all()
		lista_subtipos_compatibles = []

		query_dispositivo = Dispositivo.objects.get(id = id_disp)
		query_compatibles_previos = Compatibilidad.objects.filter(dispositivo = query_dispositivo)
		subtipo_disp = query_dispositivo.subtipo_disp
		id_subtipo_disp = subtipo_disp.id

		lista_subtipos_compatibles.append(id_subtipo_disp)

		#Si existen compatibilidades previas:
		if query_compatibles_previos:
			#Lista de IDs de los subtipos que ya eran compatibles con el dispsotivo elegido
			
			for elemento in query_compatibles_previos:
				lista_subtipos_compatibles.append(elemento.subtipo.id)
			ctx = {'lista_dispositivo':lista_dispositivo, 'lista_subtipo':lista_subtipo, 'lista_subtipos_compatibles':lista_subtipos_compatibles}
			return render_to_response('ajax/validar_dispositivo_diferente_comp.html',ctx,context_instance = RequestContext(request))
		else:
			ctx = {'lista_dispositivo':lista_dispositivo, 'lista_subtipo':lista_subtipo, 'lista_subtipos_compatibles':lista_subtipos_compatibles}
			return render_to_response('ajax/validar_dispositivo_diferente_comp.html',ctx,context_instance = RequestContext(request))
	else:
		pass

def ajax_activar_input(request):
	if request.method == 'POST':
		ctx={}
		return render_to_response('ajax/activar_input.html',ctx,context_instance = RequestContext(request))
	else:
		pass

def ajax_listar_compatibilidad(request):
	if request.method == 'POST':
		id_disp = request.POST['id']
		dispositivo = Dispositivo.objects.get(id = id_disp)

		query_incompat1 = Compatibilidad.objects.filter(dispositivo = dispositivo)
		ctx = {'lista_subtipo':query_incompat1}
		return render_to_response('ajax/listar_compatibilidad.html',ctx,context_instance=RequestContext(request))		
	else:
		pass

def ajax_listar_incompatibilidad(request):
	if request.method == 'POST':
		id_disp = request.POST['id']
		dispositivo = Dispositivo.objects.get(id = id_disp)

		lista_disp_incompatibles = []
		query_incompat1 = Incompatibilidad.objects.filter(dispositivo1 = dispositivo)
		query_incompat2 = Incompatibilidad.objects.filter(dispositivo2 = dispositivo)

		#Lista que almacena todos los ids de dispositivos2 incompatibles con dispositivo escogido
		lista_disp_incompat1 = []
		#Lista que almacena todos los ids de dispositivos1 incompatibles con dispositivo escogido
		lista_disp_incompat2 = []

		if query_incompat1:
			for incompat1 in query_incompat1:
				lista_disp_incompat1.append(incompat1.dispositivo2.id)
		if query_incompat2:
			for incompat2 in query_incompat2:
				lista_disp_incompat2.append(incompat2.dispositivo1.id)	

		#unimos las dos listas, obteniendo todos los ids incompatibles con el disp elegido, pueden haber repetidos, por eso usamos set
		dispositivos_incompatibles = list(set(lista_disp_incompat1 + lista_disp_incompat2))
		lista_dispositivo = []
		
		#Llamamos a cada instancia del dispositivo con los ids
		for disp in dispositivos_incompatibles:
			lista_dispositivo.append(Dispositivo.objects.get(id = disp))

		ctx = {'lista_dispositivo':lista_dispositivo}
		return render_to_response('ajax/listar_incompatibilidad.html',ctx,context_instance=RequestContext(request))		
	else:
		pass

def ajax_editar_servicio(request):
	if request.method == 'POST':
		id_servicio = request.POST['id']
		
		#Se obtienen los datos del servicio y se rellena el formulario con ellos
		datos_servicio = ServicioTecnico.objects.get(id = id_servicio)
		formulario = servicioForm(instance = datos_servicio)

		ctx = {'editarServicioForm':formulario}
		return render_to_response('ajax/editar_servicio.html',ctx,context_instance=RequestContext(request))	
	else:
		pass