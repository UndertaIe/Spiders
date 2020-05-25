function main(splash,args)
    splash:clear_cookies()
    splash.images_enabled = false
    splash:on_request(function(request)
        request:set_proxy{
	        host = "*proxy_host*",
	        port = *proxy_port*,
	    }
		end)
    splash:set_custom_headers({
        ["User-Agent"] = "*UA*",
        ['Referer'] = "https://www.zhipin.com/web/common/security-check.html",
        ['Content-Type'] = 'application/json'
    })
    splash:go("*url*")
    splash:wait(1)
    cookie = splash:get_cookies()
    splash:clear_cookies()
    return cookie
end

