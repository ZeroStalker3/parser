from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re
import csv
import logging

# Настройка логирования
logging.basicConfig(
    filename='parser.log',
    level=logging.INFO,  # INFO — можно сменить на DEBUG, WARNING, ERROR
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

# Эмулируем прокрутку страницы
def scroll_page(driver, scrolls=10, delay=1):
    body = driver.find_element(By.TAG_NAME, 'body')
    for _ in range(scrolls):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(delay)


def run_parser(max_items, min_price, max_price):

    service = Service(r'C:\my\myproject\DefaultApp\parser\geckodriver.exe')

    options = Options()
    #options.add_argument('--headless')         # ⛔ Без открытия окна браузера
    options.add_argument('--disable-gpu')      # Оптимизация
    options.add_argument('--log-level=3')      # Убирает лишние предупреждения

    driver = webdriver.Firefox(service=service, options=options)

    driver.get("https://market.yandex.ru/catalog--noutbuki/54544")

    parsed_links = set()

    time.sleep(5)

    titles = driver.find_elements(By.CSS_SELECTOR, '[data-zone-name="title"] a')
    prices = driver.find_elements(By.CSS_SELECTOR, '[data-zone-name="price"]')

    # Получаем карточки товаров
    cards = driver.find_elements(By.CSS_SELECTOR, '[data-zone-name="productSnippet"]')
    print(f"Найдено карточек: {len(cards)}")

    logging.info("Начало парсинга...")

    with open('laptops.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(['№', 'Название', 'Цена', 'Ссылка'])

        while True:
            scroll_page(driver, scrolls=5, delay=1.5)
            cards = driver.find_elements(By.CSS_SELECTOR, '[data-zone-name="productSnippet"]')
            print(f"Найдено карточек: {len(cards)}")

            if len(parsed_links) >= max_items or len(cards) == len(parsed_links):
                break

            for i, card in enumerate(cards, 1):
                try:
                    title_elem = card.find_element(By.CSS_SELECTOR, '[data-zone-name="title"] a')
                    link = title_elem.get_attribute('href')

                    if link in parsed_links:
                        continue

                    price_elem = card.find_element(By.CSS_SELECTOR, '[data-zone-name="price"]')
                    lines = price_elem.text.splitlines()
                    price_line = next((line for line in lines if re.search(r'\d+', line)), None)

                    if not price_line:
                        logging.info(f"{i}. Пропущено — не найдена строка с ценой.")
                        continue

                    digits = re.findall(r'\d+', price_line)
                    if not digits:
                        logging.info(f"{i}. Пропущено — нет цены.")
                        continue

                    price = int(''.join(digits))
                    title = title_elem.text.strip()

                    if price < max_price and price > min_price:
                            line = f"{len(parsed_links)+1}. {title} — {price} ₽ — {link}\n"
                            #print(line.strip())
                            writer.writerow([i, title, price, link])
                            logging.info(f"{i}. Сохранён: {title} — {price} ₽ — {link}")
                            parsed_links.add(link)
                            #return len(parsed_links) 
                    else:
                        logging.info(f"{i}. Пропущено — цена {price} > 100000.")

                except Exception as e:
                    print(f"{i}. Ошибка: {e}")
                    continue
    driver.quit()
