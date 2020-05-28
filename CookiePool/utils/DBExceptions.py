
import config

class ConException(Exception):
    def __str__(self):
        mes = "###[ERROR] DBException，Network ERROR ###"
        return mes
