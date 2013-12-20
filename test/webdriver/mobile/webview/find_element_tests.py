#!/usr/bin/python

# Copyright 2011 Software Freedom Conservancy.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
from selenium import webdriver


class FindElementTest(unittest.TestCase):
    """
    Defines the find element tests that should be supported in a web view.

    In order to run the test class start a mobile web driver implementation
    on the port 4444.

    The Mobile WebDriver for supporting web views on Android is selendroid
    and can be started via:
    java -jar selendroid-standalone-0.6.0-with-dependencies.jar -aut ApiDemos.apk  -port 4444

    More details you find: http://selendroid.io/setup.html
    """


    @classmethod
    def setUpClass(cls):
        desired_capabilities = {'aut': 'com.example.android.apis:', 'emulator': False}

        cls.driver = webdriver.Remote(
            desired_capabilities=desired_capabilities
        )
        cls.driver.implicitly_wait(30)
        cls.driver.get('and-activity://com.example.android.apis.view.WebViewSelenium1')
        cls.driver.switch_to_window("WEBVIEW")

    def test_should_find_element_by_id(self):
        self._load_form_page()
        web_element = self.driver.find_element_by_id('checky')
        self.assertFalse(web_element.is_selected(), "element should not be selected.")

    def test_should_find_and_click_element_by_css(self):
        self._load_xhtml_test_page()
        self.driver.find_element_by_css_selector("a[id='linkId']").click()
        self.assertEqual(self.driver.title, "We Arrive Here")

    def test_should_find_and_click_element_by_xpath(self):
        self._load_xhtml_test_page()
        self.driver.find_element_by_xpath("//a[@id='linkId']").click()
        self.assertEqual(self.driver.title, "We Arrive Here")

    def test_should_find_and_click_element_by_tag_name(self):
        self._load_xhtml_test_page()
        self.driver.find_element_by_tag_name("a").click()
        self.assertEqual(self.driver.title, "We Arrive Here")

    def test_should_find_element_by_class(self):
        self._load_xhtml_test_page()
        element = self.driver.find_element_by_class_name("myTestClass")
        self.assertEqual(element.text, "click me")

    def test_should_find_element_by_name(self):
        self._load_xhtml_test_page()
        element = self.driver.find_element_by_name("nameTest")
        self.assertEqual(element.text, "click me")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def _load_form_page(self):
        self._load_page("file:///android_asset/www/formPage.html")

    def _load_xhtml_test_page(self):
        self._load_page("file:///android_asset/www/xhtmlTest.html")

    def _load_selectable_items_page(self):
        self._load_page("file:///android_asset/www/selectableItems.html")

    def _load_nested_elements_page(self):
        self._load_page("file:///android_asset/www/nestedElements.html")

    def _load_javascript_page(self):
        self._load_page("file:///android_asset/www/javascriptPage.html")

    def _load_missed_js_reference_page(self):
        self._load_page("file:///android_asset/www/missedJsReference.html")

    def _load_actual_xhtml_page(self):
        self._load_page("file:///android_asset/www/actualXhtmlPage.xhtml")

    def _load_page(self, name):
        self.driver.get(name)


if __name__ == '__main__':
    unittest.main()