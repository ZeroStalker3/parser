# 🕷️ Парсер ноутбуков с Яндекс.Маркета на Selenium

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Selenium](https://img.shields.io/badge/Selenium-Automation-brightgreen)
![CSV Export](https://img.shields.io/badge/Output-CSV-yellow)
![Logger](https://img.shields.io/badge/Logging-Enabled-orange)

## 📌 Описание

Данный проект полностью автоматизированный веб-парсер, написанный на Python с использованием Selenium WebDriver. Он собирает данные о ноутбуках с сайта [Яндекс.Маркет](https://market.yandex.ru/catalog--noutbuki/54544), включая:

- Название товара  
- Цену  
- Ссылку на страницу  

Фильтрация: в CSV попадают только ноутбуки с ценой **до 100 000 ₽**.  
Пример удобного парсера с логированием и автоскроллом страницы, подходящий для демонстрации навыков.

---

## 📂 Возможности

✅ Прокрутка страницы для подгрузки товаров  
✅ Сбор до 100 товаров  
✅ Фильтрация по цене  
✅ Сохранение результатов в `laptops.csv`  
✅ Логирование событий в `parser.log`  
✅ Гибкая настройка парсинга

---

## 📸 Пример результата

```csv
№,Название,Цена,Ссылка
1,Acer Nitro 5 AN515,74999,https://market.yandex.ru/...
2,Lenovo IdeaPad 3,64999,https://market.yandex.ru/...
...
```

---

## 🚀 Установка и запуск

### 🔧 Зависимости

- Python 3.10+
- Selenium
- Firefox
- Geckodriver

### 🛠 Установка

Установите зависимости:

```bash
pip install selenium
```

Скачайте Geckodriver и укажите путь в коде:

```python
from selenium.webdriver.firefox.service import Service
service = Service(r'C:\my\myproject\parser\geckodriver.exe')
```

Запустите парсер:

```bash
python parser.py
```
