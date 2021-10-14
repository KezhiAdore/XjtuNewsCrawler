import scrapy
import json
import time
import random

class XjtunewsspiderSpider(scrapy.Spider):
    name = 'XjtuNewsSpider'
    domain = 'http://news.xjtu.edu.cn/'
    start_url = 'http://news.xjtu.edu.cn/zyxw.htm'
    filename='news.json'
    count=0
    data=[]

    def start_requests(self):
        yield scrapy.Request(self.start_url,callback=self.process_page)
        return super().start_requests()


    def process_page(self,response):
        if self.count==100:
            return
        # 读取该页面上的新闻链接
        news_links=response.xpath('//a[@class="bt"]/@href').extract()
        # 遍历新闻链接提取新闻内容
        for news_link in news_links:
            yield scrapy.Request(response.urljoin(news_link),callback=self.get_news)
        # 进入下一页
        next_page_url=response.xpath('//a[text()="下页"]/@href').extract()[0]
        time.sleep(random.random())
        yield scrapy.Request(response.urljoin(next_page_url),callback=self.process_page)

    def get_news(self,response):
        if self.count==100:
            return
        news={}
        # 提取页面标题
        title_list=response.xpath('//head/title/text()').extract()
        title=""
        for item in title_list:
            title+=item
        # 提取新闻内容
        content_list=response.xpath('//div[@class="v_news_content"]/descendant::text()').extract()
        content=""
        for item in content_list:
            content+=item
        # 构造存储字典
        news['title']=title
        news['content']=content
        news['url']=response.url
        print("当前爬取新闻数量："+str(self.count))
        self.data.append(news)
        self.count+=1
        with open(self.filename,'w+',encoding='utf-8') as f:
            json.dump(self.data,f,ensure_ascii=False,indent=4)
            f.close()
        time.sleep(random.random())
        pass
