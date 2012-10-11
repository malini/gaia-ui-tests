# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase


class TestCamera(GaiaTestCase):

    _capture_photo_locator = ('name', 'Capture')
    _film_strip_image_locator = ('css selector', 'div#film-strip > img')


    def test_capture_a_photo(self):
        # https://moztrap.mozilla.org/manage/case/1309/

        self.assertTrue(self.lockscreen.unlock())

        # launch the Camera app
        app = self.apps.launch('camera')
        self.assertTrue(app.frame_id is not None)

        # switch into the Camera's frame
        self.marionette.switch_to_frame(app.frame_id)
        url = self.marionette.get_url()
        self.assertTrue('camera' in url, 'wrong url: %s' % url)

        self.marionette.find_element(*self._capture_photo_locator).click()

        self.wait_for_element_present(*self._film_strip_image_locator)

        # Find the new picture in the film strip
        self.assertTrue(self.marionette.find_element(*self._film_strip_image_locator).is_displayed())

        # close the app
        self.apps.kill(app)