import requests
from bs4 import BeautifulSoup
from bs4 import NavigableString
from bs4 import Tag


class MovieSpider:
    def __init__(self, site_url):
        self.siteURL = site_url
        self.__headers = {
            'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
        print(self.siteURL)

    def getPageWithNum(self, pageIndex):
        url = self.siteURL + "?page=" + str(pageIndex)
        request = requests.request(method="get", url=url, headers=self.__headers)
        response = request.content
        return response.decode("gbk")

    def getPage(self):
        url = self.siteURL
        requests.ReadTimeout = 10000

        request = requests.request(method="get", url=url, headers=self.__headers)
        response = request.content
        return response


s = MovieSpider("https://movie.douban.com/")
content = s.getPage()
soup = BeautifulSoup(content, "lxml")
result = soup.find_all("li", {"class": "ui-slide-item"})
for i, child in enumerate(result):

    if child.ul != None:
        # print("i:", i, child)
        print("-------------------------------------------------->")
        print("片名:", child.attrs['data-title'])
        print("主演:", child.attrs['data-actors'])
        print("导演:", child.attrs['data-director'])
        print("时长:", child.attrs['data-duration'])
        print("评价:", child.attrs['data-rater'])
        print("国家:", child.attrs['data-region'])
        print("发布时间:", child.attrs['data-release'])
        print("购票:", child.attrs['data-ticket'])
        print("预告片:", child.attrs['data-trailer'])
        for i, child_child in enumerate(child.ul):
            if type(child_child) == NavigableString:
                continue
            if type(child_child) == Tag:
                if child_child['class'][0] == "poster":
                    print("海报:", child_child.a.img['src'])
                    # if child_child['class'][0] == "title":
                    # print(i, "==title===>", child_child['a'])
                if child_child['class'][0] == "rating":
                    if child_child.span.string == None:
                        print("评分:", list(child_child.children)[2].string)
                    else:
                        print("评分:", child_child.span.string)
                if child_child['class'][0] == "ticket_btn":
                    print("订票:", child_child.span.a['href'])
