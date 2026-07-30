
class BusinessError(Exception):
    def __init__(self, codigo:int, mensaje:str, status_code:int = 400):
        self.codigo = codigo
        self.mensaje = mensaje
        self.status_code = status_code


        