# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase


class TestCamera(GaiaTestCase):

    _capture_button_locator = ('id', 'capture-button')
    _switch_source_button_locator = ('id', 'switch-button')
    _film_strip_image_locator = (
        'css selector', 'div#film-strip div.image > img')
    _video_timer_locator = ('id', 'video-timer')

    def setUp(self):
        GaiaTestCase.setUp(self)

        self.assertTrue(self.lockscreen.unlock())

        # launch the Camera app
        self.app = self.apps.launch('camera')
        self.assertTrue(self.app.frame_id is not None)

        # switch into the Camera's frame
        self.marionette.switch_to_frame(self.app.frame_id)
        url = self.marionette.get_url()
        self.assertTrue('camera' in url, 'wrong url: %s' % url)

    def test_capture_a_photo(self):
        # https://moztrap.mozilla.org/manage/case/1309/
        self.wait_for_capture_ready()

        self.marionette.find_element(*self._capture_button_locator).click()

        self.wait_for_element_present(*self._film_strip_image_locator)

        # Find the new picture in the film strip
        self.assertTrue(self.marionette.find_element(
            *self._film_strip_image_locator).is_displayed())

    def test_capture_a_video(self):
        self.wait_for_capture_ready()

        self.marionette.find_element(
            *self._switch_source_button_locator).click()

        self.marionette.find_element(*self._capture_button_locator).click()

        self.wait_for_element_displayed(*self._video_timer_locator)
        # Wait for 3 seconds of recording
        self.wait_for_condition(lambda m: m.find_element(
            *self._video_timer_locator).text == '00:03')

        # Stop recording
        self.marionette.find_element(*self._capture_button_locator).click()

        self.wait_for_element_not_displayed(*self._video_timer_locator)

        # TODO
        # Validate the recorded video somehow

    def wait_for_capture_ready(self):
        self.marionette.set_script_timeout(10000)
        self.marionette.execute_async_script("""
        function check_ready_state() {
            if (document.getElementById('viewfinder').readyState > 1) {
                marionetteScriptFinished();
            }
            else {
                setTimeout(check_ready_state, 500);
            }
        }
        setTimeout(check_ready_state, 0);
        """)

    def tearDown(self):

        # close the app
        if hasattr(self, 'app'):
            self.apps.kill(self.app)

        GaiaTestCase.tearDown(self)
