# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
import time

class TestMarketplace(GaiaTestCase):

    _login_button = ('css selector', 'a.button.browserid')

    _persona_frame = ('css selector',"iframe[name='__persona_dialog']")

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


    @unittest.skip("Don't want to run this on Jenkins")
    def test_load_marketplace(self):

        # TODO replace this with an appropriate wait
        time.sleep(10)
        #print self.marionette.page_source

        self.marionette.find_element(*self._login_button).click()

        # switch to top level frame
        self.marionette.switch_to_frame()

        #switch to persona frame

        self.marionette.wait_for_element_displayed(*self._persona_frame)
        persona_frame = self.marionette.find_element(*self._persona_frame)
        self.marionette.switch_to_frame(persona_frame)

        #TODO switch to Persona frame


        #TODO complete Persona login
        #self.testvars['marketplace_username']
        #self.testvars['marketplace_password']

        #TODO Switch back to marketplace and verify that user is logged in


    def tearDown(self):

        # close the app
        if self.app:
            self.apps.kill(self.app)

        GaiaTestCase.tearDown(self)
