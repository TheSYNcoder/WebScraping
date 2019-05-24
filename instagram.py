'''
JUST a prototype model , can be configured later to select photos
with more hashtags or user profile , or any other ways
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import os
from bs4 import BeautifulSoup
from xlsxwriter import Workbook
import requests
import lxml
import shutil

error =False
class App:
    def __init__(self ,username ,password , path):

        self.username =username
        self.password =password
        self.path =path
        error =False
        chromedriver ='/Users/shuvayan/Downloads/chromedriver'
        os.environ["webdriver.chrome.driver"] = chromedriver
        self.driver = webdriver.Chrome(chromedriver)

        if not os.path.exists(path):
            os.mkdir(path)

        sleep(5)


    def open(self):
        try:

            self.driver.get("https://www.instagram.com/")
            sleep(3)
        except Exception as e:
            error =True

            print("Page won't open")



    def signUp(self):
        try:

            signUp = self.driver.find_element_by_xpath('//a[@href = "/accounts/login/?source=auth_switcher"]')
            signUp.click()
            sleep(5)

        except Exception as e:
            error =True
            print("Some attributes of page(SignUp) changed")


    def logIn(self):
        try:
            username_element = self.driver.find_element_by_xpath(
                '//div[@class="f0n8F "]/input[@aria-label="Phone number, username, or email"]')
            username_element.send_keys(self.username)

            password_element = self.driver.find_element_by_xpath('//div[@class="f0n8F "]/input[@aria-label="Password"]')
            password_element.send_keys(self.password)
            password_element.submit()
            # input()
            sleep(6)

        except Exception as e:
            error=True
            print("Some attributes of login page changed")

    def closePopUp(self):

        try:
            notnowButton = self.driver.find_element_by_xpath('//button[@class="aOOlW   HoLwm "]')
            notnowButton.click()

        except Exception as e:
            error =True
            print("Pop Up window chars changed!")

    def OpenTargetHashTag(self):

        try:
            searchBar = self.driver.find_element_by_xpath('//input[@placeholder="Search"]')
            searchBar.send_keys("sunset")
            sleep(2)
            searchBar.send_keys(Keys.ENTER)
            searchBar.send_keys(Keys.ENTER)

            sleep(5)

        except Exception as e:
            error =True
            print(e)
            print("Something Wrong with search bar")

    def ScrollDown(self):

        try:

#                             We 'll scroll down 10 times
#             OR   CAN BE DONE BY COUNTING THE NO OF IMAGES FIND XPATH OF THE NUMBER.text.replace(",","")
#                 THEN SCROLLING ACCORDING NO OF IMAGES LOADED IN A SCROLL
            for i in range(10):
                self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
                sleep(1)
        except Exception as e:
            error =True
            print("Can't scroll" )


    def WriteToExcel(self , images , caption_path):

        workbook = Workbook(os.path.join(caption_path , 'captions.xlsx'))
        row = 0
        worksheet = workbook.add_worksheet()
        worksheet.write(row, 0, 'IMAGE_NAME')
        worksheet.write(row, 1, 'CAPTION')

        for index, image in enumerate(images):
            try:
                caption = image['alt'])
                except KeyError:
                caption = 'No caption for this image'
            link = image['src']
            filename = 'image_' + str(index)
            # filepath = os.path.join(captions_folder_path, filename)
            worksheet.write(row, 0, filename)
            worksheet.write(row, 1, caption)
            row+=1

        workbook.close()



    def downloadCaptions(self, images):

        try:
            captions_folder_path = os.path.join(self.path , 'captions')
            if not os.path.exists(captions_folder_path)
                os.mkdir(captions_folder_path)
            for index , image in enumerate(images):
                try:
                    caption =image['alt'])
                except KeyError:
                    caption ='No caption for this image'
                # Writing captions for each image in a separate txt file
                link = image['src']
                filename ='caption_' + str(index ) + '.txt'
                filepath = os.path.join(captions_folder_path ,filename )
                with open( filepath , 'wb') as file:
                    file.write(str('link:' + str(link) + '\n' + 'caption:' +caption).encode())

                    #encoding necessary for emojis and stuff
        #     Writing the captions in a xlsx file

            WriteToExcel(images , captions_folder_path)




        except Exception as e:
            print(e)
            error=True
            print('CANT Download Captions')



    def downloading(self):

        try:
            soup = BeautifulSoup(self.driver.page_source,'lxml')
            all_images  = soup.find_all('img')
            print(len(all_images))
            self.downloadCaptions(all_images)
            for index,image in enumerate(all_images):
                filename = "image_" + str(index) +'.jpeg'
                # imagepath = self.path +'/'+ filename
                imagepath = os.path.join(self.path , filename)
                link =image['src']
                print("Downloading Image" , index)
                response =requests.get(link , stream =True)
                try:
                    with open(imagepath , 'wb') as file:
                        shutil.copyfileobj(response.raw ,file )
                except Exception as e:
                    print(e)
                    print ('CAnT download image ' , index)
                    print('Image link ', link)

        except Exception as e:
            error =True
            print(e)
            print('Can\'t Download')








inst =App("<username>" , "********" , "<PATH_NAME>")
if not error:
    inst.open()
if not error:
    inst.signUp()
if not error:
    inst.logIn()
if not error:
    inst.closePopUp()
if not error:
    inst.OpenTargetHashTag()
if not error:
    inst.ScrollDown()
if not error:
    inst.downloading()


