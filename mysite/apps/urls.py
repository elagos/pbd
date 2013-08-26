from django.conf.urls import patterns,url
from django.conf import settings
from mysite.apps.forms import registroUsuario

urlpatterns = patterns('mysite.apps.views',
	url(r'^$','index_view', name='index'),
    url(r'^home/$','index_view', name='index'),
    url(r'^categorias/$','categorias_view', name='categorias'),
    url(r'^search/$','search_view', name='search'),
    url(r'^dispositivo/$','dispositivo_view', name='dispositivo'),
    url(r'^servicios/$','servicios_view', name='servicios'),
    url(r'^abast/$','abast_view', name='abast'),

    #url(r'^menuA//$','_view',name=''),

    url(r'^carrito/$','carrito_view',name='carrito'),

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
    url(r'^menuA/admCompatibilidades/agIncompatibilidad/$','agIncompatibilidad_view',name='agIncompatibilidad'),
    url(r'^menuA/admCompatibilidades/elIncompatibilidad/$','elIncompatibilidad_view',name='elIncompatibilidad'),

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

    # AJAX
    url(r'^ajax/validar_dispositivo_diferente/$','ajax_validar_disp_diferente',name='ajax validar disp diferente'),
    url(r'^ajax/validar_dispositivo_diferente_comp/$','ajax_validar_disp_diferente_comp',name='ajax validar disp diferente'),
    # url(r'^ajax/escoger_subtipo/$','ajax_escoger_subtipo',name='escoger subtipo'),
    # url(r'^ajax/escoger_subtipo2/$','ajax_escoger_subtipo2',name='escoger subtipo2'),
    # url(r'^ajax/escoger_dispositivo/$','ajax_escoger_dispositivo',name='escoger dispositivo'),
    url(r'^ajax/activar_input/$','ajax_activar_input',name='activar_input'),
    url(r'^ajax/listar_compatibilidad/$','ajax_listar_compatibilidad',name='ajax listar compat'),
    url(r'^ajax/listar_incompatibilidad/$','ajax_listar_incompatibilidad',name='ajax listar incompat'),
    url(r'^ajax/editar_servicio/$','ajax_editar_servicio',name='ajax editar servicio'),

	url(r'^menuE/$','menuE_view',name='menuE'),
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
