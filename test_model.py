import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()
    # Переходим на страницу авторизации
    driver.get('https://petfriends.skillfactory.ru/login')

    yield driver

    driver.quit()

@pytest.fixture(autouse=True)
def test_login(driver):
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('qa@qu')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('poiuy')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    #проверяем что заголовок в коде не равен строке h1
    assert WebDriverWait(driver, 5).until(EC.title_is("PetFriends: My Pets"))


def test_all_pets(driver):
    # переходим в раздел мои питомцы
    driver.find_element(By.LINK_TEXT, "Мои питомцы").click()
    # находим колличество питомцев
    pets_number = driver.find_element(By.XPATH, '//*[@class=".col-sm-4 left"]').text.split("\n")[1].split(': ')[1]
    #неявные ожидания присутсвия в коде класса таблица
    driver.implicitly_wait(5)
    driver.find_element(By.XPATH, "//*[@class='table table-hover']")
    # находим таблицу с питомцами и сверяем колличество
    pets_count = driver.find_elements(By.XPATH, './/*[@id="all_my_pets"]/table/tbody/tr')
    assert len(pets_count) == int(pets_number)


def test_image(driver):
    # переходим в раздел мои питомцы
    driver.find_element(By.LINK_TEXT, "Мои питомцы").click()
    # находим таблицу с питомцами
    pets_count = driver.find_elements(By.XPATH, './/*[@id="all_my_pets"]/table/tbody/tr')
    #вычесляем значение половины от общего числа питомцев
    half_pets = len(pets_count)//2
    #поиск строки с фото в коде
    driver.implicitly_wait(5)
    driver.find_elements(By.TAG_NAME, "img")
    #поиск фото в карточках питомцев
    image = driver.find_elements(By.XPATH, '//img[starts-with(@src, "data:image/")]')
    #сравниваем полученное колличество фото с значением половины питомцев
    #фото должно быть у половины имеющихся питомцев
    assert float(half_pets) <= len(image)

def test_name_age_breed(driver):
    # переходим в раздел мои питомцы
    driver.find_element(By.LINK_TEXT, "Мои питомцы").click()
    #проверяем что у всех питомцев есть имя, порода, возраст
    names = driver.find_elements(By.CSS_SELECTOR, 'tr > td:first-child')
    breed = driver.find_elements(By.CSS_SELECTOR, 'tr > td:nth-child(2)')
    age = driver.find_elements(By.CSS_SELECTOR, 'tr > td:nth-child(3)')
    for name in names:
        assert name.text.strip() != ''

    for br in breed:
        assert br.text.strip() != ''

    for ag in age:
        assert ag.text.strip() != ''

def test_different_name(driver):
    # переходим в раздел мои питомцы
    driver.find_element(By.LINK_TEXT, "Мои питомцы").click()
    #находим значение имени всех питомцев и сравниваем на наличие дубликатов
    names = driver.find_elements(By.CSS_SELECTOR, 'tr > td:first-child')
    name_set = set()
    for name in names:
        assert name.text.strip() not in name_set
        name_set.add(name.text.strip())



