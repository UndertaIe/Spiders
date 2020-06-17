function main(splash,args)
    splash:clear_cookies()
    splash:on_request(function(request)
        request:set_proxy{
	        host = "*proxy_host*",
	        port = *proxy_port*,
	    }
		end)
    splash:set_custom_headers({
        ["User-Agent"] = "*UA*",
        ['Referer'] = "https://www.zhipin.com"
    })
    splash:go("*url*")
    splash:wait(1)
    cookie = splash:get_cookies()
    splash:clear_cookies()
    return cookie
end

