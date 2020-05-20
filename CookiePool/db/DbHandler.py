

class DbHanlder:

    # 插入cookie
    def insert(self, cookie):
        raise NotImplemented

    # 返回所有cookie
    def select(self, cookie):
        raise NotImplemented

    # 得到随机cookie
    def get(self):
        raise NotImplemented

    def count(self):
        raise NotImplemented

    # 去除cookie
    def remove(self):
        raise NotImplemented