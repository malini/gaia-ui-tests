# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
import time
import unittest
from marionette.keys import Keys


class TestMarketplace(GaiaTestCase):

    _login_button = ('css selector', 'a.button.browserid')
    _persona_frame = ('css selector', "iframe[name='__persona_dialog']")

    _throbber_locator = ('id', 'throbber')

    _search_button = ('css selector', '.header-button.icon.search.right')
    _search = ('id', 'search-q')

    _search_results_area = ('id', 'search-results')
    _search_result = ('css selector', '#search-results li.item')

    def setUp(self):
        GaiaTestCase.setUp(self)

        # unlock the lockscreen if it's locked
        self.assertTrue(self.lockscreen.unlock())

        # launch the app
        self.app = self.apps.launch('Marketplace')
        self.assertTrue(self.app.frame_id is not None)

        # switch into the app's frame
        self.marionette.switch_to_frame(self.app.frame_id)

        url = self.marionette.get_url()
        self.assertTrue('marketplace' in url, 'wrong url: %s' % url)

    @unittest.skip("Don't want to run this on CI")
    def test_load_marketplace(self):

        self.wait_for_element_displayed(*self._login_button)
        self.marionette.find_element(*self._login_button).click()

        # switch to top level frame
        self.marionette.switch_to_frame()

        #switch to persona frame

        self.wait_for_element_present(*self._persona_frame)
        #persona_frame = self.marionette.find_element(*self._persona_frame)
        #self.marionette.switch_to_frame(persona_frame)

        #TODO switch to Persona frame and wait for throbber to clear

        #TODO complete Persona login
        #self.testvars['marketplace_username']
        #self.testvars['marketplace_password']
        #TODO Switch back to marketplace and verify that user is logged in

    def test_that_searches_for_a_app(self):
        self.wait_for_element_displayed(*self._search_button)
        self.marionette.find_element(*self._search_button).click()

        self.wait_for_element_displayed(*self._search)
        search_box = self.marionette.find_element(*self._search)
        search_box.send_keys('Hypno')
        search_box.send_keys(Keys.RETURN)

        self.wait_for_element_displayed(*self._search_results_area)

        results = self.marionette.find_elements(*self._search_result)

        self.assertGreater(len(results), 0, 'no results found')

    def tearDown(self):

        # close the app
        if self.app:
            self.apps.kill(self.app)

        GaiaTestCase.tearDown(self)

    def is_throbber_visible(self):
        return self.marionette.find_element(*self._throbber_locator).size['height'] == 4
