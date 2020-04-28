# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

global number 
number = 10
class GetAllDetailSpider(scrapy.Spider):
    name = 'get_all_detail'
    allowed_domains = ['t.me']
    # start_urls = ['https://t.me/']

    # ''' - is multiline string in python
# this script is from splash
    script = '''
        function main(splash, args)
            splash.private_mode_enable = false
            splash:on_request(
                        function(request)
                            request:set_header('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/81.0.4044.113 Chrome/81.0.4044.113 Safari/537.36')
                        end)

                    url = args.url
                    assert(splash:go(url))
                    assert(splash:wait(1))
                
                    splash:set_viewport_full()
                    return splash:html()
            
           
          
        end

    '''

    # since we're using splash we can't send request using the script_requset class,it won't work,
    # so insted we use another class specific to splash ="SplashRequest"

    #endpoint="execute" - is because we want to exectue the above splash "script"
    #args = tells which script to run

    def start_requests(self):
        yield SplashRequest(url="https://t.me/s/aliexplorer?after={0}".format(number),callback=self.parse,endpoint="execute",args = {
            'lua_source':self.script
        })

    def parse(self, response):
       
        # yield{
        #     'channalName': response.xpath("//div[@class = 'tgme_channel_info_header']/div/span/text()").get(),
        #     'channalUserName': response.xpath("//div[@class = 'tgme_channel_info_header_username']/a/text()").get(),
        #     'Members': response.xpath("(//div[@class = 'tgme_channel_info_counter']/span)[1]/text()").get(),
        # }

        for post in response.xpath("//div[@class ='tgme_widget_message_bubble']"):
                yield{
                    'PostTitle':post.xpath(".//div[2]/b/text()").get(),
                    'PostView':post.xpath(".//div[3]/div/span[1]/text()").get()
                    
                }
        global number
        number+=50
       
        next_page =  SplashRequest(url='https://t.me/s/aliexplorer?after={0}'.format(number),callback= self.parse,endpoint="execute",args = {
            'lua_source':self.script,
            'wait':1
        })

        if next_page:
            yield next_page


    # def parseAgain(self, response):
    #     for post in response.xpath("//div[@class ='tgme_widget_message_bubble']"):
    #             yield{
    #                 'PostTitle':post.xpath(".//div[2]/b/text()").get(),
    #                 'PostView':post.xpath(".//div[3]/div/span[1]/text()").get()
                    
    #             }
