from django.shortcuts import render
import requests
from .forms import Cargar_configuracion, Crear_factura, CrearEmpresa
# Create your views here.


servidor = "http://127.0.0.1:4000/"

def cargar(request):
    ctx={
        'texto':None
    }
    if request.method=='POST':
        form=Cargar_configuracion(request.POST, request.FILES)
        if form.is_valid():
            f=request.FILES['file']
            xml_binary=f.read()
            r=requests.post(servidor+'configuracion',data=xml_binary)
            response = r.json()
            ctx['texto']=str(response["clienteConteo"]) + ' nuevos clientes creados, '+ str(response["playConteo"])+ ' nuevas playlists creadas, '+ str(response["empresaConteo"])+' empresas nuevas creadas'
            print(ctx['texto'])
    else:
        return render(request,'configuracion.html')
    return render(request,'configuracion.html',ctx)

def consultar_datos(request):
    contexto={
        'empresas':[],
        'clientes' : [],
        'playList' : [],
        'canciones' : []
    }
    try:
        response=requests.get(servidor+'consultarDatos') #http://127.0.0.1:5000/canciones
        datos=response.json()
        contexto['empresas']=datos['empresas']
        contexto['clientes']=datos['clientes']
        contexto['playList']=datos['playList']
        for canciones in datos['playList']:
            for cancion in canciones['canciones']:
                contexto['canciones'].append(cancion)
    except:
        print('Error en la API')
    return render(request,'consultarDatos.html',contexto)

def factura(request):
    ctx={
        'noFactura':None,
        'empresa':None,
        'clientes':[],
        'Total': 0
    }
    if request.method=='POST':
        form=Crear_factura(request.POST)
        if form.is_valid():
            id=form.cleaned_data['empresa']
            r=requests.post(servidor+'factura/'+id)
            response = r.json()
            ctx['noFactura'] = response['noFactura']
            ctx['empresa'] = response['empresa']
            ctx['clientes'] = response['clientes']
            ctx['Total'] = response['Total']
    else:
        return render(request,'factura.html')
    return render(request,'factura.html',ctx)

def crear_empresa(request):
    ctx={
        'texto':None
    }
    if request.method=='POST':
        form=CrearEmpresa(request.POST)
        if form.is_valid():
            id=form.cleaned_data['id']
            name=form.cleaned_data['name']
            xml_binary="<configuracion><listaEmpresas><empresa id=\""+id+"\"><nombre>\""+ name+ "\"</nombre></empresa></listaEmpresas></configuracion>"
            r=requests.post(servidor+'crearEmpresa',data=xml_binary)
            response = r.json()
            ctx['texto']=response["mensaje"]
    else:
        return render(request,'crearEmpresa.html')
    return render(request,'crearEmpresa.html',ctx)