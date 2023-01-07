from django import forms

class Cargar_configuracion(forms.Form):
    file=forms.FileField(label="file")

class Crear_factura(forms.Form):
    empresa = forms.CharField(label="empresa")

class CrearEmpresa(forms.Form):
    id = forms.CharField(label="id")
    name = forms.CharField(label="name")
