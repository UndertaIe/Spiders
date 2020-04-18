
def driver2cookie(cookie_from_driver):
    cookie = {}
    for coo in cookie_from_driver:
        cookie.setdefault(coo['name'], coo['value'])
    return cookie