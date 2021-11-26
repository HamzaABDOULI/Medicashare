from datetime import time
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time


# # Test 1

# class Hosttest(LiveServerTestCase):

#    def testhomepage(self):
#        driver = webdriver.Chrome()

#        driver.get('http://127.0.0.1:8000/')

#        time.sleep(5)

#        assert "Hello, world!!"


# Test 2  Login Page 

class LoginFormTest(LiveServerTestCase):

    def testform(self):
        driver = webdriver.Chrome()

        driver.get('http://127.0.0.1:8000/login/')

        time.sleep(3)

        user_name = driver.find_element_by_name('username')
        user_password = driver.find_element_by_name('password')

        time.sleep(3)

        submit = driver.find_element_by_id('submit')

        user_name.send_keys('admin')
        user_password.send_keys('admin')

        submit.send_keys(Keys.RETURN)

        time.sleep(10)

        assert 'admin' in driver.page_source



#         tologout = driver.find_element_b('button')
#         time.sleep(3)
#         tologout.click()

#         # logout = driver.find_element_by_class_name('dropdown-item')
#         # time.sleep(3)
#         # logout.send_keys(Keys.RETURN)
#         time.sleep(10)

# Test 3  SignUp Page 

# class LoginFormTest(LiveServerTestCase):

#     def testform(self):
#         driver = webdriver.Chrome()

#         driver.get('http://127.0.0.1:8000/login/')

#         time.sleep(3)

#         joinus = driver.find_element_by_id('joinus')

#         time.sleep(3)
#         joinus.send_keys(Keys.RETURN)

#         time.sleep(5)

#         user_name = driver.find_element_by_name('username')
#         email = driver.find_element_by_name('email')
#         first_name = driver.find_element_by_name('first_name')
#         last_name = driver.find_element_by_name('last_name')
#         password1 = driver.find_element_by_name('password1')
#         password2 = driver.find_element_by_name('password2')

#         time.sleep(3)

#         signup = driver.find_elements_by_id('Sign up')

#         user_name.send_keys('adminaaa')
#         email.send_keys('admin@admin.com')
#         first_name.send_keys('admin')
#         last_name.send_keys('admin')
#         password1.send_keys('adminadmin')
#         password2.send_keys('adminadmin')

#         time.sleep(3)

#         signup.send_keys(Keys.RETURN)
#driver.find_element_by_id("submit_btn").click()
#a revoir 

#         time.sleep(10)


       
# https://www.thepythoncode.com/article/automate-login-to-websites-using-selenium-in-python