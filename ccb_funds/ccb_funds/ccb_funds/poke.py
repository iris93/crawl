import scrapy

class CcbGetnews(scrapy.Spider):
    name = 'ccbgetnews'
    allowed_domains = ['ccb.com']
    start_urls = ['http://finance.ccb.com/cc_webtran/queryFinanceProdList.gsp?jsoncallback=jsonpCallback']
    
    def start_requests(self):
        yield scrapy.FormRequest(
            url = 'http://finance.ccb.com/cc_webtran/queryFinanceProdDetail.gsp?jsoncallback=jQuery191036942510719116894_1533864732025&params.code=ZHQYAX20180600001',
            formdata={'jsoncallback':'jQuery191036942510719116894_1533864732025','params.code':'ZHQYAX20180600001'},
            method = 'POST',
            callback=self.parse)
    
    def parse(self, response):
        print(response.text)