import undetected_chromedriver
from bs4 import BeautifulSoup
import time as time_s


def get_Y_time_km(url):
    driver = undetected_chromedriver.Chrome()
    driver.get(url)
    time_s.sleep(2)
    with open("Yandex_parsed_page.html", "w") as file:
        file.write(driver.page_source)
    time_s.sleep(2)
    with open('Yandex_parsed_page.html', 'r') as f:
        contents = f.read()
        html = BeautifulSoup(contents, 'html.parser')

        convert = html.find_all('div', class_='auto-route-snippet-view__route-title-primary')
        find_time = str(convert[0].contents[0])
        c = find_time.split(' ')
        if len(c) == 1:
            if "мин" in c[0]:
                hrs = 0
                mins = int(c[0].replace("мин", ""))
            else:
                mins = 0
                hrs = int(c[0].replace("ч", ""))
        elif len(c) == 2:
            hrs = int(c[0].replace("ч", ""))
            mins = int(c[1].replace("мин", ""))

        convert = html.find_all('div', class_='auto-route-snippet-view__route-subtitle')
        find_km = str(convert[0].contents[0])
        try:
            find_km.index('км')
        except ValueError:
            km = float(find_km.split('м')[0]) / 1000
        else:
            km = float(find_km.split('км')[0].replace(",", "."))
        min_km = [hrs * 60 + mins, km]
        return min_km









