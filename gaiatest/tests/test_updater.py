# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
import unittest


class TestUpdater(GaiaTestCase):

    _device_info_link = ('css selector', "a[data-l10n-id='deviceInfo']")

    def setUp(self):
        GaiaTestCase.setUp(self)

        # unlock the lockscreen if it's locked
        self.assertTrue(self.lockscreen.unlock())

        # launch the Settings app
        self.app = self.apps.launch('Settings')
        self.assertTrue(self.app.frame_id is not None)

        self.marionette.switch_to_frame(self.app.frame_id)
        url = self.marionette.get_url()
        self.assertTrue('settings' in url, 'wrong url: %s' % url)

    # TODO finish this test as per https://github.com/zacc/gaia-ui-tests/issues/5
    @unittest.skip("Don't want to run this on CI")
    def test_ota_update(self):

        # Device information
        self.marionette.find_element(*self._device_info_link).click()

        # Click check now

        # wait for 'Checking for updates' to clear

        # Confirm that ui journey is complete

    def tearDown(self):

        # close the app
        if hasattr(self, 'app'):
            self.apps.kill(self.app)

        GaiaTestCase.tearDown(self)
