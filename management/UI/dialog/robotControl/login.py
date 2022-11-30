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

from PyQt6.QtCore import pyqtSignal, QObject
from ....CONSTANTS import PATH_CHROME, PATH_CHROMEDRIVER, PATH_PROFILES_BROWSER
from ....helper import _getExactlyPath

class Login(QObject):
    progress_msg = pyqtSignal(dict)
    finished = pyqtSignal(dict)
    def __init__(self, payload, parent=None):
        super().__init__(parent)
        self.username = payload['username']
        self.password = payload['password']
    
    def run(self):
        result = self.__mainControl()
        # self.driver.close()
        # self.driver.quit()
        self.finished.emit(result)
    
    def __mainControl(self):
        if self.__initDriver():
            loginStatus = self.__handleLogin()
            if loginStatus == 'logged':
                profileName = self.__handleGetName()
                if profileName == 'error':
                    # self.driver.close()
                    # self.driver.quit()
                    return {'status': profileName, 'name': ''}
                else:
                    # self.driver.close()
                    # self.driver.quit()
                    return {'status': 'logged', 'name': profileName}
            else:
                # self.driver.close()
                # self.driver.quit()
                return {'status': loginStatus, 'name': ''}
        else:
            # self.driver.close()
            # self.driver.quit()
            return {'status': 'error', 'name': ''}

    def __initDriver(self):
        self.urlLogin = 'https://www.facebook.com/login'
        self.urlCheckpoint = 'https://www.facebook.com/checkpoint/'
        self.urlProfile = 'https://www.facebook.com/profile.php'
        pathProfile = _getExactlyPath(PATH_PROFILES_BROWSER) + os.sep + f'profile_{self.username}'
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
        
        return True
    
    def __handleLogin(self):
        def login():
            try:
                emailInput = self.wait.until(EC.visibility_of_element_located((By.ID, 'email')))
                passInput = self.wait.until(EC.visibility_of_element_located((By.ID, 'pass')))
                loginBtn = self.wait.until(EC.visibility_of_element_located((By.NAME, 'login')))

                emailInput.send_keys(self.username)
                sleep(0.1)
                passInput.send_keys(self.password)
                sleep(0.1)
                loginBtn.click()               
            except:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                sleep(1)
                return False

            try:
                self.wait.until(EC.url_changes(self.urlLogin))
                if self.driver.current_url.find(self.urlLogin) < 0 and self.driver.current_url.find(self.urlCheckpoint) < 0:
                    self.progress_msg.emit({'url': self.driver.current_url, 'msg': 'logged'})
                    return 'logged'
                elif self.driver.current_url.find(self.urlCheckpoint) >= 0:
                    sleep(10)
                    self.progress_msg.emit({'url': self.driver.current_url, 'msg': 'checkpoint'})
                    return 'checkpoint'
                elif self.driver.current_url.find(self.urlLogin) >= 0:
                    sleep(10)
                    self.progress_msg.emit({'url': self.driver.current_url, 'msg': 'false'})
                    return 'false'
            
            except:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                self.progress_msg.emit({'url': self.driver.current_url, 'msg': 'not redirected'})
                return 'false'

        try:
            self.driver.get(self.urlLogin)
            self.wait.until(EC.url_changes(self.urlLogin))
            currentUrl = self.driver.current_url
            if currentUrl.find(self.urlCheckpoint) >= 0:
                sleep(10)
                self.progress_msg.emit({'url': self.driver.current_url, 'msg': 'checkpoint'})
                return 'checkpoint'
            else:
                self.progress_msg.emit({'url': self.driver.current_url, 'msg': 'logged'})
                return 'logged'
        except:
            self.progress_msg.emit({'url': self.driver.current_url, 'msg': 'logging ...'})
            return login()
        
    def __handleGetName(self):
        sleep(uniform(0, 5))
        self.driver.get(self.urlProfile)
        try:
            h1Elms = self.driver.find_elements(By.CSS_SELECTOR, 'h1')
            profileName = h1Elms[-1].get_attribute('innerText')
            self.progress_msg.emit({'url': self.driver.current_url, 'msg': profileName})
            sleep(1)
            return profileName
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            self.progress_msg.emit({'url': self.driver.current_url, 'msg': 'error'})
            sleep(1)
            return 'error'