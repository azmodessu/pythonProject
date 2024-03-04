# from selenium import webdriver
# from selenium_stealth import stealth
# from selenium.webdriver.common.by import By
# from openpyxl import Workbook
#
import BD
import sneakers
import Winter_shoes
#
# wb = Workbook()
# ws = wb.active
# ws.title = "Sneakers"
# ws.append(['Title', 'Price', 'Image', ''])
#
# from selenium.webdriver.chrome.service import Service
#
# options = webdriver.ChromeOptions()
# options.add_argument("start-maximized")
#
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)
#
# s = Service('D:/chromedriver.exe')
# driver = webdriver.Chrome(service=s)
#
# stealth(driver,
#         languages=["en-US", "en"],
#         vendor="Google Inc.",
#         platform="Win64",
#         webgl_vendor="Intel Inc.",
#         renderer="Intel Iris OpenGL Engine",
#         fix_hairline=True,
#         )
#
# for page in range(1, 2):
#     url = f"https://sneakerhead.ru/shoes/sneakers/?PAGEN_1={page}"
#     driver.get(url)
#     blocks = driver.find_element(By.CLASS_NAME, "product-cards__list")
#     posts = blocks.find_elements(By.CLASS_NAME, "product-cards__item")
#
#     for post in posts:
#         title = post.find_element(By.CLASS_NAME, "product-card").find_element(By.CLASS_NAME,
#                                                                               "product-card__title").find_element(
#             By.CLASS_NAME, "product-card__link").get_attribute("title")
#         price = post.find_element(By.CLASS_NAME, "product-card").find_element(By.CLASS_NAME,
#                                                                               "product-card__price").find_element(
#             By.CLASS_NAME, "product-card__price-value").text.replace(" ", ".")
#         image = "https://sneakerhead.ru/" + post.find_element(By.CLASS_NAME, "product-card").find_element(By.CLASS_NAME,
#                                                                                                           "product-card__image").find_element(
#             By.CLASS_NAME, "product-card__image-inner").find_element(By.TAG_NAME, "source").get_attribute(
#             "data-srcset").split("1x")[0]
#         ws.append([title, price, image])
#         print(title, price, image)
# wb.save('sneakers.xlsx')

#sneakers.export()

#sneakers.export()
import sqlite3

# Устанавливаем соединение с базой данных
connection = sqlite3.connect('sneakers.db')
cursor = connection.cursor()

# Выбираем всех пользователей
cursor.execute('SELECT * FROM sneakers')
users = cursor.fetchall()
# Преобразуем результаты в список словарей

# Выводим результаты
users_list = []
for user in users:
  users_list.append(user)

print(users_list[0])
print(users_list[1])
print(users_list[2])
connection.close()
