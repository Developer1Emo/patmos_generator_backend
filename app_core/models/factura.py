class Factura:
    def __init__(self, compania, co, tipo_documento, consecutivo):
        self.compania = compania
        self.co = co
        self.tipo_documento = tipo_documento
        self.consecutivo = consecutivo

    def __str__(self):
        return f"Factura {self.co} - {self.tipo_documento} - {self.consecutivo}"
