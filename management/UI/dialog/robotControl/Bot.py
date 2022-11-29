import sys
import os
from time import sleep
from random import uniform

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common import exceptions as SExceptions

from PyQt6.QtCore import pyqtSignal, QObject

from ....CONSTANTS import PATH_CHROME, PATH_CHROMEDRIVER, PATH_PROFILES_BROWSER, TEXT_MOREPLACE, MARKETPLACE
from ....helper import _getExactlyPath
from ....helper import _initItem

class Bot(QObject):
    progress_msg = pyqtSignal(dict)
    finished = pyqtSignal(dict)
    changeAccount = pyqtSignal(int)
    sellDelay = pyqtSignal(int)
    delayTime = pyqtSignal(dict)
    def __init__(self, payload, parent=None):
        super().__init__(parent)
        self.action = payload['action']
        self.setting = payload['setting']
        self.profiles = payload['profiles']
        self.hiddenBrowser = self.setting['hidden_browser']

    
    def run(self):
        if self.action == 'sell':
            itemCountMax = 0
            for profile in self.profiles.values():
                itemList = profile['items']
                if len(itemList) > itemCountMax:
                    itemCountMax = len(itemList)
            sellDelay = self.setting['sell_delay']
            changeAccount = self.setting['change_account']

            for i in range(itemCountMax):
                for profile in self.profiles.values():
                    if len(profile['items']) <= 0:
                        continue
                    _username = profile['username']
                    _name = profile['name']
                    _idProduct = profile['items'].pop()
                    _product = _initItem(_idProduct)
                    if _product:
                        # print(_product)
                        self.__sellingBot(_username, _name, _product)
                    self.__changeAccount(changeAccount)
                self.__sellDelay(sellDelay)

        elif self.action == 'care':
            for profile in self.profiles.values():
                _username = profile['username']
                _name = profile['name']
                self.__careBot(_username, _name)

        self.finished.emit({'status' : 'success'})
    
    def __sellingBot(self, username, name, item):
        if self.__initDriver(username, name) == 'logged':
            dialog = self.__clickComposer()
            if dialog:
                if self.__fillComposerForm(dialog, item):
                    self.__listInMorePlace()
                    self.driver.close()
                    self.driver.quit()
                    self.progress_msg.emit({'status': 'success', 'msg': 'Closed browser'})
                    return True
                else:
                    self.driver.close()
                    self.driver.quit()
                    return False
            else:
                self.driver.close()
                self.driver.quit()
                return False
        else:
            self.driver.close()
            self.driver.quit()
            return False

    def __initDriver(self, username, name):
        self.urlLogin = 'https://www.facebook.com/login'
        self.urlCheckpoint = 'https://www.facebook.com/checkpoint/'
        self.urlGroup = f'https://facebook.com/groups/2427280817529774'

        pathProfile = _getExactlyPath(PATH_PROFILES_BROWSER) + '\\' + f'profile_{username}'
        pathChromeDrive = _getExactlyPath(PATH_CHROMEDRIVER)
        options = Options()
        options.add_experimental_option('debuggerAddress', 'localhost:9223')
        options.add_argument('--disable-notifications')
        service = Service(pathChromeDrive)

        if os.path.exists(pathProfile) is False:
            os.mkdir(pathProfile)
        os.popen(f'"{PATH_CHROME}" --remote-debugging-port=9223 --user-data-dir="{pathProfile}"')
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.set_window_size(960, 1080)
        self.wait = WebDriverWait(self.driver, 10)

        try:
            self.driver.get(self.urlLogin)
            self.wait.until(EC.url_changes(self.urlLogin))
            currentUrl = self.driver.current_url
            if currentUrl.find(self.urlCheckpoint) >= 0:
                sleep(10)
                self.progress_msg.emit({'status': 'false', 'msg': f'{name} checkpoint'})
                return 'checkpoint'
            else:
                self.progress_msg.emit({'status': 'success', 'msg': f'{name} logged'})
                return 'logged'
        except:
            self.progress_msg.emit({'status': 'false', 'msg': f'{name} unlogged'})
            return 'unlogged'
    
    def __clickComposer(self):
        sleep(uniform(1,5))
        self.driver.get(self.urlGroup)
        try:
            try:
                groupInlineComposer = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-pagelet="GroupInlineComposer"]')))
                groupInlineComposer = groupInlineComposer.find_element(By.CSS_SELECTOR, 'div[role="button"]')
            except SExceptions.TimeoutException:
                try:
                    groupInlineComposer = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Bán gì đó"]')))
                except SExceptions.TimeoutException:
                    self.progress_msg.emit({'status': 'error', 'msg': 'GroupInlineComposer is not available'})
                    return False
            sleep(uniform(1, 5))
            desired_y = (groupInlineComposer.size['height'] / 2) + groupInlineComposer.location['y']
            window_h = self.driver.execute_script('return window.innerHeight')
            window_y = self.driver.execute_script('return window.pageYOffset')
            current_y = (window_h / 2) + window_y
            scroll_y_by = desired_y - current_y
            self.driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)

            groupInlineComposer.click()
            self.progress_msg.emit({'status': 'running', 'msg': 'Clicked GroupInlineComposer'})

            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="dialog"]')))
            self.wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Đang tải..."]')))
            dialog = self.driver.find_elements(By.CSS_SELECTOR, 'div[role="dialog"]')[-1]

            sleep(uniform(1, 5))
            WebDriverWait(dialog, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[role="button"]')))
            btnCreateElm = dialog.find_elements(By.CSS_SELECTOR, 'div[role="button"]')[1]

            sleep(uniform(1, 5))
            btnCreateElm.click()
            self.progress_msg.emit({'status': 'success', 'msg': 'composerForm starting ..'})
            return dialog
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            self.progress_msg.emit({'status': 'error', 'msg': 'Can not click composerForm'})
            return False

    def __fillComposerForm(self, dialog, product):
        self.progress_msg.emit({'status': 'running', 'msg': 'Fill composerForm ..'})
        sleep(uniform(3, 5))
        currentUrl = self.driver.current_url
        try:
            inputs = dialog.find_elements(By.CSS_SELECTOR, 'input[type="text"]')
            textareas = dialog.find_elements(By.CSS_SELECTOR, 'textarea')
            image = dialog.find_element(By.CSS_SELECTOR, 'input[accept="image/*,image/heif,image/heic"]')
            status = dialog.find_element(By.CSS_SELECTOR, 'label[role="combobox"]')
            title = inputs[0]
            price = inputs[1]
            location = inputs[2]
            description = textareas[0]

            image.send_keys(product['images'])
            sleep(uniform(1, 5))
            self.progress_msg.emit({'status': 'running', 'msg': 'Select condition ..'})
            status.click()
            option = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="option"]')))
            sleep(uniform(1, 5))
            option.click()

            self.progress_msg.emit({'status': 'running', 'msg': 'Fill title ..'})
            title.send_keys(product['header'])
            sleep(uniform(1, 5))
            self.progress_msg.emit({'status': 'running', 'msg': 'Fill price ..'})
            price.send_keys('0')
            sleep(uniform(1, 5))
            self.progress_msg.emit({'status': 'running', 'msg': 'Fill description ..'})
            description.send_keys(product['description'])
            sleep(uniform(1, 5))
            self.progress_msg.emit({'status': 'running', 'msg': 'Select city ..'})
            location.send_keys(product['district'])
            sleep(uniform(1, 5))

            locationList = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul[role="listbox"]')))
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="presentation"]')))
            dalat  = locationList.find_element(By.CSS_SELECTOR, 'div[role="presentation"]')
            sleep(uniform(1, 5))
            dalat.click()

            self.progress_msg.emit({'status': 'running', 'msg': 'Click next ..'})
            nextBtn = dialog.find_elements(By.CSS_SELECTOR, 'div[role="button"]')[-1]
            self.driver.execute_script("arguments[0].scrollIntoView();", nextBtn)
            sleep(uniform(1, 5))
            nextBtn.click()
            try:
                self.progress_msg.emit({'status': 'running', 'msg': 'Click post ..'})
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Đăng"]')))
                postBtn = self.driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Đăng"]')
                self.driver.execute_script("arguments[0].scrollIntoView();", postBtn)
                sleep(uniform(3, 5))
                self.progress_msg.emit({'status': 'success', 'msg': 'Clicked post'})
                postBtn.click()
            except:
                self.progress_msg.emit({'status': 'error', 'msg': 'Can not click post'})
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                return False
            self.wait.until(EC.url_changes(currentUrl))
            return True
        except:
            self.progress_msg.emit({'status': 'error', 'msg': 'Can not fill composerForm'})
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return False

    def __openDialog(self):
        try:
            self.progress_msg.emit({'status': 'running', 'msg': 'Click menu button'})
            webpage = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[role="main"]')))
            ariaPosinset = WebDriverWait(webpage, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[aria-posinset="1"]')))
            menuBtn = WebDriverWait(ariaPosinset, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[aria-haspopup="menu"]')))
            # self.driver.execute_script("arguments[0].scrollIntoView();", menuBtn)
            sleep(uniform(0.2, 5))
            menuBtn.click()
            self.progress_msg.emit({'status': 'running', 'msg': 'Click List more places'})
            menuBox = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[role="menu"]')))
            if WebDriverWait(menuBox, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[role="menuitem"]'))):
                menuItems = self.driver.find_elements(By.CSS_SELECTOR, 'div[role="menuitem"]')
            else:
                return False
            for menuItem in menuItems:
                if menuItem.get_attribute('innerText').lower() == TEXT_MOREPLACE.lower():
                    sleep(uniform(0.2, 5))
                    menuItem.click()
                    break

            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="dialog"]')))
            dialog = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, F'div[aria-label="{TEXT_MOREPLACE}"]')))
            self.progress_msg.emit({'status': 'success', 'msg': 'Opened dialog'})
            return dialog
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            self.progress_msg.emit({'status': 'error', 'msg': 'Cannot open dialog'})
            return False

    def __listInMorePlace(self):
        sleep(uniform(0, 5))
        groupCount = self.__getGroupCount()
        if groupCount:
            self.placePrevs = []
            while groupCount > 0:
                if groupCount % 20 > 0:
                    self.__clickPlaces(groupCount - groupCount % 20, groupCount)
                    groupCount -= groupCount %20
                sleep(uniform(3, 5))
                if int(groupCount / 20) > 0:
                    self.__clickPlaces(groupCount - 20, groupCount)
                    groupCount -= 20
            return True

    def __clickPlaces(self, startPlace, endPlace):
        dialog = self.__openDialog()
        try:
            self.progress_msg.emit({'status': 'running', 'msg': 'Click places'})
            WebDriverWait(dialog, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-visualcompletion="ignore-dynamic"]')))
            places = dialog.find_elements(By.CSS_SELECTOR, 'div[data-visualcompletion="ignore-dynamic"]')
            for i in reversed(range(startPlace, endPlace)):
                if i == 0:
                    continue
                if places[i].get_attribute('innerText') in self.placePrevs:
                    continue
                else:
                    self.placePrevs.append(places[i].get_attribute('innerText'))
                    btn = places[i].find_element(By.CSS_SELECTOR, 'div[role="button"]')
                    self.driver.execute_script("arguments[0].scrollIntoView();", btn)
                    sleep(uniform(0.1, 1))
                    btn.click()
                    # self.progress_msg.emit({'status': 'running', 'msg': 'Clicked'})

            sleep(uniform(0.1, 5))
            self.__clickPostBtn(dialog)
            self.progress_msg.emit({'status': 'success', 'msg': 'Clicked post'})
        except:
            self.progress_msg.emit({'status': 'error', 'msg': 'Cannot list'})
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return False

    def __getGroupCount(self):
        dialog = self.__openDialog()
        if dialog:
            try:
                WebDriverWait(dialog, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-visualcompletion="ignore-dynamic"]')))
                places = dialog.find_elements(By.CSS_SELECTOR, 'div[data-visualcompletion="ignore-dynamic"]')
                groupCount = 0
                isMarketplaceClicked = False
                for place in places:
                    if len(place.find_elements(By.CSS_SELECTOR, 'i')) > 0:
                        if place.get_attribute('innerText').lower() == MARKETPLACE.lower():
                            isMarketplaceClicked = True
                            place.click()
                        groupCount += 1
                
                if isMarketplaceClicked:
                    self.progress_msg.emit({'status': 'success', 'msg': 'Clicked Marketplace'})
                    self.__clickPostBtn(dialog)
                else: self.__clickCancelBtn(dialog)
                return groupCount
            except:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                return False

    def __clickCancelBtn(self, dialog):
        try:
            e = WebDriverWait(dialog, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Hủy"]')))
            self.driver.execute_script("arguments[0].scrollIntoView();", e)
            btns = dialog.find_elements(By.CSS_SELECTOR, 'div[aria-label="Hủy"]')
            for btn in btns:
                try:
                    btn.click()
                except SExceptions.WebDriverException:
                    continue
            return True
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return False
        
    def __clickPostBtn(self, dialog):
        try:
            e = WebDriverWait(dialog, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Đăng"]')))
            self.driver.execute_script("arguments[0].scrollIntoView();", e)
            btns = dialog.find_elements(By.CSS_SELECTOR, 'div[aria-label="Đăng"]')
            for btn in btns:
                try:
                    btn.click()
                except SExceptions.WebDriverException:
                    continue
            return True
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return False

##########################################

    def __careBot(self, username, name):
        if self.__initDriver(username, name) == 'logged':
            if self.setting['newfeed'] != '':
                self.__newFeed()
            if self.setting['video'] != '':
                self.__video()
            if self.setting['groupFeed'] != '':
                self.__groupFeed()

            self.driver.close()
            self.driver.quit()
            self.progress_msg.emit({'status' : 'success', 'msg': f'{username} finished'})
        else:
            self.driver.close()
            self.driver.quit()
            self.progress_msg.emit({'status' : 'false', 'msg': f'{username} unlogged'})
            return False
        
        return True

    def __newFeed(self):
        timeRemain = int(self.setting['newfeed'])
        self.progress_msg.emit({'status': 'newfeed', 'msg': 'start'})
        count = 1
        while timeRemain > 0:
            try:
                ariaPosinset = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'div[aria-posinset="{count}"]')))
            except:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                self.progress_msg.emit({'status': 'false', 'msg': 'cannot get element ariaPosinset '})
                return False
            count += 1
            delayTime = uniform(3, 8)
            self.__delayTime(delayTime, 'newfeed')
            self.driver.execute_script("arguments[0].scrollIntoView();", ariaPosinset)
            timeRemain -= delayTime
        self.progress_msg.emit({'status': 'newfeed', 'msg': 'finished'})
        return True

    def __video(self):
        urlVideo = 'https://www.facebook.com/watch'
        self.driver.get(urlVideo)
        videosCount = int(self.setting['video'])
        self.progress_msg.emit({'status': 'video', 'msg': 'start'})
        try: 
            wacthFeed = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#watch_feed')))
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            self.progress_msg.emit({'status': 'false', 'msg': 'cannot get element watch_feed '})
            return False
        for i in range(videosCount):
            self.progress_msg.emit({'status': 'video', 'msg': f'watch video {i}'})
            try:
                WebDriverWait(wacthFeed, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'video')))
                videos = self.driver.find_elements(By.CSS_SELECTOR, 'video')
                self.driver.execute_script("arguments[0].scrollIntoView();", videos[i])
                self.__delayTime(180, 'video')
            
            except:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                self.progress_msg.emit({'status': 'false', 'msg': f'cannot get element of video {i} '})
                return False
        self.progress_msg.emit({'status': 'video', 'msg': 'finished'})
        return True
  
    def __groupFeed(self):
        urlGroupFeed = 'https://www.facebook.com/groups/feed/'
        self.driver.get(urlGroupFeed)
        timeRemain = int(self.setting['groupFeed'])
        self.progress_msg.emit({'status': 'groupFeed', 'msg': 'start'})
        count = 1
        while timeRemain > 0:
            try:
                ariaPosinset = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'div[aria-posinset="{count}"]')))
            except:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                self.progress_msg.emit({'status': 'false', 'msg': 'cannot get element ariaPosinset '})
                return False
            count += 1
            delayTime = uniform(3, 8)
            self.__delayTime(delayTime, 'groupFeed')
            self.driver.execute_script("arguments[0].scrollIntoView();", ariaPosinset)
            timeRemain -= delayTime
        self.progress_msg.emit({'status': 'groupFeed', 'msg': 'finished'})
        return True
        pass

# div[aria-posinset="15"]
##########################################

    def __changeAccount(self, time):
        if time == '':
            _time = 0
        else:
            _time = int(time)
        while _time >= 0:
            self.changeAccount.emit(_time)
            sleep(1)
            _time -= 1

    def __sellDelay(self, time):
        if time == '':
            _time = 0
        else:
            _time = int(time)
        while _time >= 0:
            self.changeAccount.emit(_time)
            sleep(1)
            _time -= 1

    def __delayTime(self, time, action):
        if time == '':
            _time = 0
        else:
            _time = int(time)
        while _time >= 0:
            self.delayTime.emit({'action' : action, 'time': _time})
            sleep(1)
            _time -= 1
