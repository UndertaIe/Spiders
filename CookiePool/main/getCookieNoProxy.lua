function main(splash,args)
    splash:clear_cookies()
    splash.images_enabled = false
    splash:set_custom_headers({
        ["User-Agent"] = "*UA*",
        ['Referer'] = "https://www.zhipin.com",
        ['Content-Type'] = 'application/json'
    })
    splash:go("*url*")
    splash:wait(1)
    cookie = splash:get_cookies()
    splash:clear_cookies()
    return cookie
end
