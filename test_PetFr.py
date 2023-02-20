import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from settings import valid_email, valid_password


def test_show_my_pets():

   #Настраиваем переменную явного ожидания
   wait = WebDriverWait(pytest.driver, 5)

   # Вводим email
   element = wait.until(EC.presence_of_element_located((By.ID, "email")))
   pytest.driver.find_element_by_id('email').send_keys(valid_email)

   # Вводим пароль
   element = wait.until(EC.presence_of_element_located((By.ID, "pass")))
   pytest.driver.find_element_by_id('pass').send_keys(valid_password)

   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element_by_css_selector('button[type="submit"]').click()

   # Проверяем, что мы оказались на главной странице пользователя
   # и ожидаем, что на странице есть тег h1 с текстом "PetFriends"(ожидаем определенный текст внутри документа)
   assert wait.until(EC.text_to_be_present_in_element((By.TAG_NAME,'h1'), "PetFriends"))

   # 1) Присутствуют все питомцы

   # Нажимаем на кнопку "Мои питомцы"
   pytest.driver.find_element_by_link_text('Мои питомцы').click()

   # Получаем список всех питомцев
   all_pets = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]/table[1]/tbody[1]/tr/td/a/div')

   # Проверяем, что присутствуют все питомцы
   assert len(all_pets) == 4


   # 2) Проверяем, что хотя бы у половины питомцев есть фото
   images = pytest.driver.find_elements_by_xpath('//th[@scope="row"]/img')
   assert len(images) >= 2

   # 3) Проверяем, что у всех питомцев есть имя, возраст и порода
   names = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]/table[1]/tbody[1]/tr/td[1]')
   pytest.driver.implicitly_wait(5)
   types = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]/table[1]/tbody[1]/tr/td[2]')
   pytest.driver.implicitly_wait(5)
   ages = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]/table[1]/tbody[1]/tr/td[3]')

   for i in range(len(names)):
      assert names[i].text != ''
   for i in range(len(types)):
      assert types[i].text != ''
   for i in range(len(ages)):
      assert ages[i].text != ''

   # 4) Проверяем, что у всех питомцев разные имена

   list_names = []
   for i in range(len(names)):
      list_names.append(names[i].text)
   set_names = set(list_names)
   assert len(list_names) == len(set_names)


   # 5) Проверяем, что в списке нет повторяющихся питомцев

   all_my_pets = pytest.driver.find_elements_by_css_selector('tbody>tr')
   list_all_my_pets = []
   for i in range(len(all_my_pets)):
      list_pets_split = all_my_pets[i].text.split('\n')
      list_all_my_pets.append(list_pets_split[0])
   set_all_my_pets = set(list_all_my_pets)
   assert len(list_all_my_pets) == len (set_all_my_pets)
