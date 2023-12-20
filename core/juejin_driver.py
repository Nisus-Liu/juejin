import base64
import logging
import time
import random

import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from . import fileutil, util
from .track import track
from .config import *


class JuejinDriver(object):
    # 掘金首页
    juejin_home = "https://juejin.cn"

    # 掘金签到页面
    juejin_sign = "https://juejin.cn/user/center/signin"

    # 截屏
    screenshot_verify_image = 'temp/verify_image.png'
    screenshot_prepare_login = 'temp/prepare_login.png'

    # 重试
    retry = 10

    # 最长等待时间
    wait = 10

    def __init__(self, headless=True):
        chrome_options = Options()
        if headless:
            chrome_options.add_argument('--headless')
        self.juejin_username = JUEJIN_USERNAME
        self.juejin_password = JUEJIN_PASSWORD
        self.juejin_nickname = JUEJIN_NICKNAME
        #         self.driver = webdriver.Chrome(executable_path="./driver/linux/chromedriver", chrome_options=chrome_options)
        #         self.driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver", chrome_options=chrome_options)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(self.wait)
        self.driver.get(self.juejin_home)

    def run(self):
        try:
            self.prepare_login()
        except Exception as e:
            self.driver.save_screenshot(self.screenshot_prepare_login)
            raise Exception("Prepare login is error") from e
        flag = False
        for retry in range(self.retry):
            util.wait("get_cookies", 3)
            try:
                self.get_cookies()
                juejin_avatar_alt = self.juejin_nickname + "的头像"
                avatar = self.driver.find_element(By.XPATH, f'//img[@alt="{juejin_avatar_alt}"]')
                if avatar:
                    flag = True  # 有头像，说明登录成功
                    print(f'登录成功: {self.juejin_nickname}, 头像: {avatar.get_attribute("src")}')
                    break
            except Exception as e:
                logging.exception(f"Get cookies error, retry {retry+1} times")

        if flag is False:
            raise Exception(f"Verify slide image error and retry {self.retry}! ")

        return self.driver.get_cookies()

    def get_cookies(self):
        sliderImg, backgroundImg = self.get_verify_image_url()
        result = track.get_track(sliderImg, backgroundImg)
        self.click_and_move(result)

    def click_and_move(self, slide_track):
        iframe = self.driver.find_element(By.XPATH, '//iframe')
        # 切换到iframe
        self.driver.switch_to.frame(iframe)
        # verify_div = self.driver.find_element(By.XPATH, '''//div[@class="sc-kkGfuU bujTgx"]''')
        # verify_div = self.driver.find_element(By.XPATH, '//img[@id="captcha-verify_img_slide"]')
        verify_div = self.driver.find_element(By.XPATH, '//div[@class="captcha-slider-btn"]')

        # 按下鼠标左键
        ActionChains(self.driver).click_and_hold(verify_div).perform()
        # 遍历轨迹进行滑动
        for t in slide_track:
            ActionChains(self.driver).move_by_offset(xoffset=t, yoffset=0).perform()
        # 释放鼠标
        time.sleep(0.2)
        ActionChains(self.driver).release(on_element=verify_div).perform()
        time.sleep(random.randint(2, 5))
        self.driver.switch_to.default_content()

    def get_verify_image_url(self):
        # 获取验证图片
        # verify_image1 = self.driver.find_element(By.XPATH, '''//img[@id="captcha-verify-image"]/../img[1]''')
        # verify_image2 = self.driver.find_element(By.XPATH, '''//img[@id="captcha-verify-image"]/../img[2]''')

        # 使用XPath定位iframe   -- 页面结构变了 2023-12-20 M
        iframe = self.driver.find_element(By.XPATH, '//iframe')
        # 切换到iframe
        self.driver.switch_to.frame(iframe)

        # 在iframe中查找元素
        # verify_image = self.driver.find_element(By.XPATH, '''//img[@class="captcha-verify-image"]/../img[1]''')
        verify_image = self.driver.find_element(By.XPATH, '''//img[@id="captcha-verify_img_slide"]/../img[1]''')
        verify_canvas = self.driver.find_element(By.XPATH, '''//canvas[@id="captcha_verify_image"]/../canvas[1]''')
        verify_image_src = verify_image.get_attribute("src")
        self.driver.save_screenshot(self.screenshot_verify_image)
        # 使用JavaScript的toDataURL方法将canvas元素转换为DataURL
        canvas_base64 = self.driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);",
                                                   verify_canvas)
        # 将base64编码的图片数据解码为字节
        canvas_png = base64.b64decode(canvas_base64)
        # 将图片数据保存为本地文件
        fileutil.write(SLIDER_BACKGROUND_IMG_TEMP, canvas_png)

        r = requests.get(verify_image_src)
        fileutil.write(SLIDER_IMG_TEMP, r.content)

        # 切换回主文档
        self.driver.switch_to.default_content()
        return SLIDER_IMG_TEMP, SLIDER_BACKGROUND_IMG_TEMP

    def prepare_login(self):

        # login_button = self.driver.find_element(By.XPATH, '''//button[text()="
        #         登录
        #         "]''')
        login_button = self.driver.find_element(By.XPATH, '//button[normalize-space(text())="登录"]')

        ActionChains(self.driver).move_to_element(login_button).click().perform()  # 消除弹窗
        ActionChains(self.driver).move_to_element(login_button).click().perform()

        util.wait("点击`登录`按钮", 5)

        # other_login_span = self.driver.find_element(By.XPATH, '''//span[text()="
        #       密码登录
        #     "]''')
        other_login_span = self.driver.find_element(By.XPATH, '//span[normalize-space(text())="密码登录"]')

        ActionChains(self.driver).move_to_element(other_login_span).click().perform()

        username_input = self.driver.find_element(By.XPATH, '//input[@name="loginPhoneOrEmail"]')
        password_input = self.driver.find_element(By.XPATH, '//input[@name="loginPassword"]')
        # 保护用户名密码
        self.driver.execute_script("arguments[0].type = 'password';", username_input)
        username_input.send_keys(self.juejin_username)
        password_input.send_keys(self.juejin_password)

        # login_button = self.driver.find_element(By.XPATH, '''//button[text()="
        #       登录
        #     "]''')
        login_button = self.driver.find_element(By.XPATH,
                                                '//button[@class="btn btn-login" and normalize-space(text())="登录"]')
        ActionChains(self.driver).move_to_element(login_button).click().perform()

    def do_sign(self):
        self.driver.get("https://juejin.cn/user/center/signin")
        util.wait("do_sign goto /user/center/signin", 5)

        try:
            signed_button = self.driver.find_element(By.XPATH, '''//button[text()="
              今日已签到
            "]''')
        except NoSuchElementException:
            signed_button = None
            pass

        if signed_button is not None:
            print("*" * 10 + " 今日已签到！")
            return False

        try:
            sign_button = self.driver.find_element(By.XPATH, '''//button[text()="
              立即签到
            "]''')
        except NoSuchElementException as e:
            raise Exception("签到按钮获取失败，请查看页面是否有变化") from e
        ActionChains(self.driver).move_to_element(sign_button).click().perform()
        ActionChains(self.driver).move_to_element(sign_button).click().perform()
        time.sleep(2)
        print("-" * 10 + " > 签到结束！")
        return True
