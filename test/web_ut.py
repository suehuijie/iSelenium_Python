# _*_coding:utf-8_*_
import allure
import configparser
import os
import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


@allure.feature('Test Baidu WebUI')
class ISelenium(unittest.TestCase):
    # 读入配置文件
    def get_config(self):
        config = configparser.ConfigParser()
#         config.read(os.path.join(os.environ['USERPROFILE'], 'iselenium.ini'))
        config.read("C:\\Users\Sue\iselenium.ini")
        print("---------")
        print(config)
        print("+++++++++")
        return config

    def tearDown(self):
        self.driver.quit()

    def setUp(self):
        config = self.get_config()

        # 控制是否采用无界面形式运行自动化测试
        try:
            using_headless = os.environ["using_headless"]
        except KeyError:
            using_headless = None
            print(u'没有配置环境变量 using_headless, 按照有界面方式运行自动化测试')

        chrome_options = Options()
        if using_headless is not None and using_headless.lower() == 'true':
            print(u'使用无界面方式运行')
            chrome_options.add_argument("--headless")
#         chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

        self.driver = webdriver.Chrome(executable_path=config.get('driver', 'chrome_driver'),
                                       options=chrome_options)

    @allure.story(u'Test key word 今日头条')
    def test_webui_1(self):
        """ 测试用例1，验证'今日头条'关键词在百度上的搜索结果
        """

        self._test_baidu(u'今日头条', 'test_webui_1')

    @allure.story(u'Test key word 王者荣耀')
    def test_webui_2(self):
        """ 测试用例2， 验证'王者荣耀'关键词在百度上的搜索结果
        """

        self._test_baidu(u'王者荣耀', 'test_webui_2')

    def _test_baidu(self, search_keyword, testcase_name):
        """ 测试百度搜索子函数

        :param search_keyword: 搜索关键词 (str)
        :param testcase_name: 测试用例名 (str)
        """

        self.driver.get("https://www.baidu.com")
        print(u'打开浏览器，访问 www.baidu.com .')
        time.sleep(5)
        assert u'百度一下' in self.driver.title

        elem = self.driver.find_element_by_name("wd")
        elem.send_keys(search_keyword)
        time.sleep(3)
        elem.send_keys(webdriver.common.keys.Keys.RETURN)
        # print(f"搜索关键词~{search_keyword}")
        time.sleep(5)
        self.assertTrue(search_keyword in self.driver.title, msg=testcase_name + u"校验点 pass")
