
import config

class ConException(Exception):
    def __str__(self):
        mes = "连接数据库失败，请检查网络连接"
        return mes
