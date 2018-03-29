import urllib3
from urllib3 import util
from bs4 import BeautifulSoup


class TreeGenerator():
    def __init__(self, main_page_url):
        self.main_url = main_page_url
        self.http = urllib3.PoolManager()

    def get_page(self, url):
        if url.find(self.main_url) < 0:
            if __name__ == '__main__':
                url = self.main_url + url
        return BeautifulSoup(self.http.request('GET', url).data.decode('utf-8'), 'html5lib')

    def get_main_page(self):
        return BeautifulSoup(self.http.request('GET', self.main_url).data.decode('utf-8'), 'html5lib')

    def get_page_name(self, page):
        return page.title.text

    def get_all_hrefs(self, page):
        hrefs = map(
                lambda url: url['href'] if url.has_attr('href') else None,
                page.find_all('a')
            )
        hrefs = filter(
            lambda url: url is not None,
            hrefs
        )

        hrefs = map(
            lambda url: self.main_url+url if self.get_url_root(url) is None and url.find('images') == -1 else url,
            hrefs
        )

        hrefs = filter(
            lambda url: self.get_url_root(url) == self.get_url_root(self.main_url),
            hrefs
        )
        return list(hrefs)

    def get_url_root(self, url):
        return util.parse_url(url).hostname

    def generate_tree(self):
        hrefs = self.get_all_hrefs(self.get_main_page())
        names = []
        for url in hrefs:
            try:
                names.append(self.get_page_name(self.get_page(url)))
            except(UnicodeDecodeError):
                pass
        return names

tree = TreeGenerator('www.trema.hr')
print(tree.get_page_name(tree.get_main_page()))
for name in tree.generate_tree():
    print("\t|\n\t|-{}".format(name))
