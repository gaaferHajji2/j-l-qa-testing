import requests

from bs4 import BeautifulSoup

from content import Content

from website import Website

class Crawler:

    def __init__(self, website: Website):
        self.site  = website
        self.found = {}

    def get_page(self, url):
        try:
            data = requests.get(url)
        except Exception as e:
            print("Error In Get Page: ", e.__str__())
            return None
        # print("The Data For BS Is: ", data.content);
        return BeautifulSoup(data.content, 'lxml')

    def get_elements(self, bs, selector):
        # select Returns Empty String If No Object Found
        items = bs.select(selector)

        if items is not None and len(items)> 0:
            return '\n'.join([' '.join(item.get_text().strip().split()) for item in items])
        else:
            print(f"No Items Found For selector {selector}")

    def get_content(self, website: Website, path) -> Content:
        url = website.url + path
        bs = self.get_page(url)

        if bs is not None:
            title = self.get_elements(bs, website.titleTag)
            body  = self.get_elements(bs, website.bodyTag)

            return Content('', url, title, body)
    
        return Content('', url, '', '')

    def get_content_2(self, topic, url):
        bs = self.get_page(url)
        
        if bs is not None:
            title = self.get_elements(bs, self.site.titleTag)
            body  = self.get_elements(bs, self.site.bodyTag)
            return Content(topic, url, title, body)

        return Content(topic, url, '', '')

    def search(self, topic):
        bs = self.get_page(self.site.searchUrl + topic)
        searchResults = bs.select(self.site.resultListing)

        if searchResults is not None and len(searchResults) > 0:
            for result in searchResults:
                url = result.select(self.site.resultUrl)[0].attrs['href']
                url = url if self.site.absoluteUrl else self.site.url + url
                if url not in self.found:
                    self.found[url] = self.get_content_2(topic, url)
                self.found[url].get_data()
        else:
            print(f"No Data Found For: {self.site.searchUrl}{topic}")
            print(f"The Search Results Listing is: {self.site.resultListing}")
