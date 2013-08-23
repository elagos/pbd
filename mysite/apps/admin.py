from django.contrib import admin
from mysite.apps.models import *


admin.site.register(Producto)
admin.site.register(Abastecimiento)
admin.site.register(EquipoArmado)
admin.site.register(Tipo)
admin.site.register(Subtipo)
admin.site.register(Caracteristica)
admin.site.register(Dispositivo)
admin.site.register(DetalleCaracteristica)
admin.site.register(DetalleEquipo)
admin.site.register(Incompatibilidad)
admin.site.register(Compatibilidad)
