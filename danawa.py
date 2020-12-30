from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from bs4 import BeautifulSoup


class DanawaSearch:
    def __init__(self):
        # 브라우저 띄우지 않고 하기
        options = ChromeOptions()
        options.add_argument('headless')
        self.driver = Chrome(options=options)

    def get_data(self, address_list):
        temp_list = []
        for l in address_list:
            # 제품 링크에서 HTML 불러오기
            self.driver.get(l)
            response = self.driver.page_source

            # 태그 파싱
            soup = BeautifulSoup(response, 'html.parser')
            # 제품명 파싱
            product_name = soup.find('div', {'class': 'top_summary'}).find('h3', {'class': 'prod_tit'}).text
            # 전체 가격 리스트 파싱
            table = soup.find('tbody', {'class': 'high_list'})
            # 최저가 모듈 파싱
            low_price_module = table.find('tr', {'class': 'cash_lowest'})
            is_cash = "현금"
            if low_price_module is None:  # 현금가 존재 안함
                low_price_module = table.find('tr', {'class': 'lowest'})
                is_cash = ""
            # 최저가, 배송비, 링크 저장
            product_price = low_price_module.find('em', {'class': 'prc_t'}).text
            ship_price = low_price_module.find('span', {'class': 'stxt'}).text
            link = low_price_module.find('a').get('href')

            # 가격변동그래프 캡쳐
            image = self.driver.find_element_by_class_name('smr_graph').screenshot("test1.png")
            temp_dict = {'product_name': product_name,
                         'product_price': product_price,
                         'ship_price': ship_price,
                         'is_cash': is_cash,
                         'link': link}
            temp_list.append(temp_dict)
        return temp_list

    def __del__(self):
        self.driver.quit()