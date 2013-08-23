from django.conf.urls import patterns,url
from django.conf import settings
from mysite.apps.forms import registroUsuario

urlpatterns = patterns('mysite.apps.views',
	url(r'^$','index_view', name='index'),

    #url(r'^menuA//$','_view',name=''),

    url(r'^carrito/$','carrito_view',name='carrito'),
    url(r'^formcarrito/$','formularioCarrito_view',name='formularioCarrito'),

# Menu Administrador
#------------------------------------
	url(r'^menuA/$','menuA_view',name='menuA'),

    url(r'^menuA/admStock/$','admStock_view',name='admStock'),

    url(r'^menuA/admDispositivos/$','admDispositivos_view',name='admDispositivos'),
    url(r'^menuA/admDispositivos/agDispositivo/$','agDispositivo_view',name='agDispositivo'),
    url(r'^menuA/admDispositivos/elDispositivo/$','elDispositivo_view',name='elDispositivo'),
    url(r'^menuA/admDispositivos/edDispositivo/$','edDispositivo_view',name='edDispositivo'),

    url(r'^menuA/admEArmados/$','admEArmados_view',name='admEArmados'),
    url(r'^menuA/admEArmados/agEquipo/$','agEquipo_view',name='agEquipo'),
    url(r'^menuA/admEArmados/elEquipo/$','elEquipo_view',name='elEquipo'),
    url(r'^menuA/admEArmados/edEquipo/$','edEquipo_view',name='edEquipo'),

    url(r'^menuA/admSTecnicos/$','admSTecnicos_view',name='admSTecnicos'),
    url(r'^menuA/admSTecnicos/agSTecnico/$','agSTecnico_view',name='agSTecnico'),
    url(r'^menuA/admSTecnicos/elSTecnico/$','elSTecnico_view',name='elSTecnico'),
    url(r'^menuA/admSTecnicos/edSTecnico/$','edSTecnico_view',name='edSTecnico'),

    url(r'^menuA/admCompatibilidades/$','admCompatibilidades_view',name='admCompatibilidades'),
    url(r'^menuA/admCompatibilidades/agCompatibilidad/$','agCompatibilidad_view',name='agCompatibilidad'),
    url(r'^menuA/admCompatibilidades/elCompatibilidad/$','elCompatibilidad_view',name='elCompatibilidad'),
    url(r'^menuA/admCompatibilidades/edCompatibilidad/$','edCompatibilidad_view',name='edCompatibilidad'),

    url(r'^menuA/admTySubtipos/$','admTySubtipos_view',name='admTySubtipos'),
    url(r'^menuA/admTySubtipos/agTipo/$','agTipo_view',name='agTipo'),
    url(r'^menuA/admTySubtipos/edTipo/$','edTipo_view',name='edTipo'),
    url(r'^menuA/admTySubtipos/elTipo/$','elTipo_view',name='elTipo'),
    url(r'^menuA/admTySubtipos/agSTipo/$','agSTipo_view',name='agSTipo'),
    url(r'^menuA/admTySubtipos/edSTipo/$','edSTipo_view',name='edSTipo'),
    url(r'^menuA/admTySubtipos/elSTipo/$','elSTipo_view',name='elSTipo'),

    url(r'^menuA/admEmpleados/$','admEmpleados_view',name='admEmpleados'),
    url(r'^menuA/admEmpleados/agEmpleado/$','agEmpleado_view',name='agEmpleado'),
    url(r'^menuA/admEmpleados/elEmpleado/$','elEmpleado_view',name='elEmpleado'),
    url(r'^menuA/admEmpleados/edEmpleado/$','edEmpleado_view',name='edEmpleado'),

    url(r'^menuA/asigArmado/$','asigArmado_view',name='asigArmado'),
    url(r'^menuA/asigServicio/$','asigServicio_view',name='asigServicio'),
    url(r'^menuA/confArmado/$','confArmado_view',name='confArmado'),
    url(r'^menuA/confServicio/$','confServicio_view',name='confServicio'),
    url(r'^menuA/regServicio/$','regServicio_view',name='regServicio'),
#------------------------------------
# Menu Administrador

	url(r'^menue/$','menuE_view',name='menuE'),
	url(r'^prueba/$','prueba_view',name='agregar_disp'),
    url(r'^agregar_tipo/$','agregar_tipo',name='add_tipo'),
    url(r'^agregar_subtipo/$','agregar_subtipo',name='add_subtipo'),
    url(r'^editar_tipo/$','editar_tipo',name='editar_tipo'),
    url(r'^eliminar_tipo/$','eliminar_tipo',name='eliminar_tipo'),
    url(r'^eliminar_subtipo/$','eliminar_subtipo',name='eliminar_subtipo'),
    url(r'^agregar_dispositivo/$','agregar_dispositivo',name='agregar dispositivo'),
    url(r'^escoger_dispositivo/$','escoger_dispositivo',name='escoger dispositivo'),
    url(r'^editar_dispositivo/$','editar_dispositivo',name='editar dispositivo'),##
    url(r'^ingresar_stock/$','ingresar_stock',name='ingresar stock'),
    #url(r'^consulta/$','funcion_filtro',name='funcion_filtro'),
    url(r'^agregar_caracteristica/$','agregar_caracteristica',name='agregar caracteristica'),##
    url(r'^eliminar_dispositivo/$','eliminar_dispositivo',name='eliminar dispositivo'),
    )


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
)
