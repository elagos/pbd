from django.conf.urls import patterns,url
from django.conf import settings
from mysite.apps.forms import registroUsuario

urlpatterns = patterns('mysite.apps.views',
	url(r'^$','index_view', name='index'),
	url(r'^menuA/$','menuA_view',name='menuA'),
	url(r'^menue/$','menuE_view',name='menuE'),
	url(r'^prueba/$','prueba_view',name='agregar_disp'),
    url(r'^agregar_tipo/$','agregar_tipo',name='add_tipo'),
    url(r'^agregar_subtipo/$','agregar_subtipo',name='add_subtipo'),
    url(r'^editar_tipo/$','editar_tipo',name='editar_tipo'),
    url(r'^eliminar_tipo/$','eliminar_tipo',name='eliminar_tipo'),
    url(r'^eliminar_subtipo/$','eliminar_subtipo',name='eliminar_subtipo'),
    url(r'^agregar_dispositivo/$','agregar_dispositivo',name='agregar dispositivo'),
    url(r'^escoger_dispositivo/$','escoger_dispositivo',name='escoger dispositivo'),
    url(r'^editar_dispositivo/$','editar_dispositivo',name='editar dispositivo'),
    url(r'^ingresar_stock/$','ingresar_stock',name='ingresar stock'),
    #url(r'^consulta/$','funcion_filtro',name='funcion_filtro'),
    url(r'^agregar_caracteristica/$','agregar_caracteristica',name='agregar caracteristica'),
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
