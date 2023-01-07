from xml.etree import ElementTree as ET


class Canciones:
    def __init__(self, id: str, nombre: str, año: int, artista: str, genero: str) -> None:
        self.id = id
        self.nombre = nombre
        self.año = año
        self.artista = artista
        self.genero = genero


class PlayList:
    def __init__(self, id: str, nit: str, vinilo: bool, compacto: bool, categoria: str) -> None:
        self.id = id
        self.nit = nit
        self.vinilo = vinilo
        self.compacto = compacto
        self.categoria = categoria
        self.canciones: list[Canciones] = []
        self.monto = 0

    def agregar_canciones(self, canciones: list[ET.Element]):
        for cancion in canciones:
            nuevo = Canciones(cancion.get("id"), cancion.find("./nombre").text, int(cancion.find(
                "./anio").text), cancion.find("./artista").text, cancion.find("./genero").text)
            if nuevo.año <=1960:
                self.monto+=25
            elif nuevo.año <= 1990:
                self.monto +=15
            else:
                self.monto += 5 
            self.canciones.append(nuevo)


class Clientes:

    def __init__(self, nit: str, nombre: str, usuario: str, clave: str, direccion: str, correo: str, empresa: str, lista: list) -> None:
        self.nit = nit
        self.nombre = nombre
        self.usuario = usuario
        self.clave = clave
        self.direccion = direccion
        self.correo = correo
        self.empresa = empresa
        self.lista = lista


class Empresas:

    def __init__(self, id:str, nombre:str) -> None:
        self.id = id
        self.nombre = nombre


class Gestor:
    def __init__(self) -> None:
        self.play_lists_client: list[PlayList] = []
        self.clientes: list[Clientes] = []
        self.empresas: list[Empresas] = []
        self.noFactura = 1

    def agregar_play_list(self, play_list_client: ET.Element):
        play_list = play_list_client.findall("./playlist")
        i = 0
        for play in play_list:
            vinilo = False
            if play.find("./vinyl").text == "True" or play.find("./vinyl").text == "true":
                vinilo = True
            compacto = False
            if play.find("./compacto").text == "True" or play.find("./compacto").text == "true":
                compacto = True
            nuevo = PlayList(play.get("id"), play.find("./nitCliente").text, vinilo, compacto, play.find("./categoria").text)
            nuevo.agregar_canciones(
                play.find("./canciones").findall("./cancion"))
            if nuevo.vinilo == True:
                nuevo.monto += 500
            if nuevo.compacto == True:
                nuevo.monto += 100
            self.play_lists_client.append(nuevo)
            i+=1
        return i

    def agregar_clientes(self, lista_clientes: ET.Element):
        clientes = lista_clientes.findall("./cliente")
        x = 0
        for cliente in clientes:
            play_list = []
            i = 0
            for item in cliente.find("./playlistsAsociadas").findall("./playlist"):
                if i > 3:
                    break
                play_list.append(item.text)
                i += 1
            nuevo = Clientes(cliente.get("nit"), cliente.find("./nombre").text, cliente.find("./usuario").text, cliente.find(
                "./clave").text, cliente.find("./direccion").text, cliente.find("./correoElectronico").text, cliente.find("./empresa").text, play_list)
            self.clientes.append(nuevo)
            x += 1
        return x

    def agregar_empresa(self, lista_empresa: ET.Element):
        empresas = lista_empresa.findall("./empresa")
        i = 0
        for empresa in empresas:
            nuevo = Empresas(empresa.get("id"), empresa.find("./nombre").text)
            self.empresas.append(nuevo)
            i += 1
        return i
        
    def mostrar_datos(self):
        datos = {
            "playList": [],
            "clientes":[],
            "empresas":[]        
        }
        for playlist in self.play_lists_client:
            lista = {
                "id":playlist.id,
                "nitCliente": playlist.nit,
                "Vynil": playlist.vinilo,
                "compacto":playlist.compacto,
                "categoria":playlist.categoria,
                "canciones":[]
            }
            for cancion in playlist.canciones:
                lista_cancion = {
                    "id":cancion.id,
                    "nombre":cancion.nombre,
                    "anio":cancion.año,
                    "artista":cancion.artista,
                    "genero":cancion.genero
                    }
                lista["canciones"].append(lista_cancion)
            datos["playList"].append(lista)
        for cliente in self.clientes:
            lista = {
                "nit":cliente.nit,
                "nombre":cliente.nombre,
                "usuario":cliente.usuario,
                "clave":cliente.clave,
                "direccion":cliente.direccion,
                "correo":cliente.correo,
                "empresa":cliente.empresa,
                "playList":cliente.lista
            }
            datos["clientes"].append(lista)
        for empresa in self.empresas:
            lista = {
                "id":empresa.id,
                "nombre":empresa.nombre
            }
            datos["empresas"].append(lista)
        return datos
    
    def eliminar_cancion(self, id:str):
        for i in range(len(self.play_lists_client)):
            for x in range(len(self.play_lists_client[i].canciones)):
                if self.play_lists_client[i].canciones[x].id == id:
                    del self.play_lists_client[i].canciones[x]
                    return True
        return False
    
    def eliminar_cliente(self, nit:str):
        for i in range(len(self.clientes)):
            if self.clientes[i].nit == nit:
                del self.clientes[i]
                return True
        return False

    def crear_factura(self,id:str):
        factura = {
            "noFactura" : self.noFactura,
            "empresa": "",
            "clientes" : [],
            "Total":0
        }
        self.noFactura += 1
        for empresa in self.empresas:
            if empresa.id == id:
                factura["empresa"] = empresa.nombre
                for cliente in self.clientes:
                    if cliente.empresa == empresa.id:
                        valor = {
                            "nit":cliente.nit,
                            "nombre":cliente.nombre,
                            "correo":cliente.correo,
                            "playList":[]
                        }
                        for item in cliente.lista:
                            for playlist in self.play_lists_client:
                                if playlist.id == item:
                                    lista = {
                                        "categoria": playlist.categoria,
                                        "id":playlist.id,
                                        "monto":playlist.monto
                                    }
                                    valor["playList"].append(lista)
                                    factura["Total"] += playlist.monto
                        factura["clientes"].append(valor)
                break
        return factura
        

                
