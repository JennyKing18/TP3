###########################################################
#Elaborado por Jenny King Josue Salazar
#Fecha de creacion 14/05/23 10:30am
#Ultima modificacion 14/05/23 10:30pm
#version 3.10.6
###########################################################
# Variable Global
registro=[]

class Registro:
    """
    Definición de Atributos y métodos de la clase
    """
    def __init__(self):
        """
        Método constructor = Crea la estructura de la clase Paciente
        Método que se llama al instanciar
        """
        self.cedula=0
        self.nombre=''
        self.fechaNac=''
        self.fechaExp=''
        self.fechaVenc=''
        self.tipoLicencia=''
        self.sangre=''
        self.donador=''
        self.sede=0
        self.puntaje=0
        self.correo=''

    #asignar
    def asignarCedula(self,pcedula):
        self.cedula=pcedula
        return    
    
    def asignarNombre(self,pnombre):
        self.nombre=pnombre
        return 
    
    def asignarFechaNac(self,pfechaNac):
        self.fechaNac=pfechaNac
        return
    
    def asignarFechaExp(self,pfechaExp):
        self.fechaExp=pfechaExp
        return
    
    def asignarFechaVenc(self,pfechaVenc):
        self.fechaVenc=pfechaVenc
        return
    
    def asignarTipoLicencia(self,ptipoLicencia):
        self.tipoLicencia=ptipoLicencia
        return
    
    def asignarSangre(self,psangre):
        self.sangre=psangre
        return
    
    def asignarDonador(self,pdonador):
        self.donador=pdonador
        return
    
    def asignarSede(self,psede):
        self.sede=psede
        return
    
    def asignarPuntaje(self,ppuntaje):
        self.puntaje=ppuntaje
        return
    
    def asignarCorreo(self,pcorreo):
        self.correo=pcorreo
        return
    
    #mostrar
    def mostrarCedula(self):
        return self.cedula
    
    def mostrarNombre(self):
        return self.nombre
    
    def mostrarFechaNac(self):
        return self.fechaNac
    
    def mostrarFechaExp(self):
        return self.fechaExp
    
    def mostrarFechaVenc(self):
        return self.fechaVenc
    
    def mostrarTipoLicencia(self):
        return self.tipoLicencia
    
    def mostrarSangre(self):
        return self.sangre
    
    def mostrarDonador(self):
        return self.donador
    
    def mostrarSede(self):
        return self.sede
    
    def mostrarPuntaje(self):
        return self.puntaje
    
    def mostrarCorreo(self):
        return self.correo
    
    #mostrar Todo
    def indicarDatos(self):
        info=(f'Cédula: {self.cedula}'+
                f'\nNombre:{self.nombre}'+
                f'\nFecha Nacimiento: {self.fechaNac}'+
                f'\nFecha Expedición: {self.fechaExp}'+
                f'\nFecha Vencimiento: {self.fechaVenc}'+
                f'\nTipo de Licencia: {self.tipoLicencia}'+
                f'\nTipo de Sangre: {self.sangre}'+
                f'\nDonador: {self.donador}'+
                f'\nSede: {self.sede}'+
                f'\nPuntaje: {self.puntaje}'+
                f'\nCorreo electrónico: {self.correo}')
        return info