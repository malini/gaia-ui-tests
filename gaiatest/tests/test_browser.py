# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
import time


class TestBrowser(GaiaTestCase):

    # Browser locators
    _awesome_bar_locator = ("id", "url-input")
    _url_button_locator = ("id", "url-button")
    _throbber_locator = ("id", "throbber")
    _browser_frame_locator = ('css selector', 'iframe[mozbrowser]')

    # Mcom locators
    _mcom_main_locator = ('id', 'main-content')

    def setUp(self):
        GaiaTestCase.setUp(self)

        # unlock the lockscreen if it's locked
        self.assertTrue(self.lockscreen.unlock())

        # launch the app
        self.app = self.apps.launch('Browser')
        self.assertTrue(self.app.frame_id is not None)

        # switch into the app's frame
        self.marionette.switch_to_frame(self.app.frame_id)
        url = self.marionette.get_url()
        self.assertTrue('browser' in url, 'wrong url: %s' % url)

    @unittest.skip("Requires WiFi setup after flash Issue #2")
    def test_browser_basic(self):

        awesome_bar = self.marionette.find_element(*self._awesome_bar_locator)
        awesome_bar.click()
        awesome_bar.send_keys("www.mozilla.org")

        self.marionette.find_element(*self._url_button_locator).click()

        self.wait_for_condition(lambda m: self.is_throbber_visible() == False)

        browser_frame = self.marionette.find_element(
            *self._browser_frame_locator)

        time.sleep(5)
        self.marionette.switch_to_frame(browser_frame)

        mcom_body = self.marionette.find_element(*self._mcom_main_locator)

        self.assertTrue(mcom_body.is_displayed(), "Element in browser is not displayed")

    def tearDown(self):

        # close the app
        if hasattr(self, 'app'):
            self.apps.kill(self.app)

        GaiaTestCase.tearDown(self)

    def is_throbber_visible(self):
        return self.marionette.find_element(*self._throbber_locator).size['height'] == 4
