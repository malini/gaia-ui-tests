# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
import time
import unittest


class TestSms(GaiaTestCase):

    _summary_header_locator = ('xpath', "//h1[text()='Messages']")
    _message_list_locator = ('id', 'header-text')

    _create_new_message_locator = ('id', 'icon-add')
    _receiver_input_locator = ('id', 'receiver-input')
    _message_field_locator = ('id', 'message-to-send')
    _send_message_button_locator = ('id', 'send-message')
    _back_header_link_locator = ('xpath', '//header/a[1]')
    _message_sending_spinner_locator = ('css selector', "img[src='style/images/spinningwheel_small_animation.gif']")
    _received_message_content_locator = (
        'css selector', 'div.message-block span.received')

    def setUp(self):
        GaiaTestCase.setUp(self)

        # unlock the lockscreen if it's locked
        self.assertTrue(self.lockscreen.unlock())

        # launch the app
        self.app = self.apps.launch('Messages')
        self.assertTrue(self.app.frame_id is not None)

        # switch into the frame
        self.marionette.switch_to_frame(self.app.frame_id)
        url = self.marionette.get_url()
        self.assertTrue('gaiamobile' in url, 'wrong url: %s' % url)

    @unittest.skip("Don't want to run this on CI")
    @unittest.skipIf(GaiaTestCase.is_emulator is True, "Cannot run this test on emulator")
    def test_sms_send(self):
        '''
        This test depends upon an external/device emulator to return the text message
        For this I use an Android phone with Tasker installed that automatically responds
        to the FirefoxOS text message with "Reply + msg_content"
        '''

        _text_message_content = "Automated Test %s" % str(time.time())

        self.wait_for_element_displayed(*self._summary_header_locator)

        # click new message
        self.marionette.find_element(*self._create_new_message_locator).click()

        self.wait_for_element_present(*self._receiver_input_locator)
        # type phone number
        contact_field = self.marionette.find_element(
            *self._receiver_input_locator)
        contact_field.send_keys(self.testvars['remote_phone_number'])

        message_field = self.marionette.find_element(
            *self._message_field_locator)
        message_field.send_keys(_text_message_content)

        #click send
        self.marionette.find_element(
            *self._send_message_button_locator).click()

        self.wait_for_element_displayed(*self._message_list_locator)
        self.wait_for_element_not_present(
            *self._message_sending_spinner_locator, timeout=120)

        # go back
        self.marionette.find_element(*self._back_header_link_locator).click()

        self.wait_for_element_displayed(*self._summary_header_locator)

        _new_message_locator = (
            'xpath', "//a[@class='unread']/div[text()='Reply ']")

        # now wait for the return message to arrive.
        self.wait_for_element_present(*_new_message_locator, timeout=180)

        # go into the new message
        self.marionette.find_element(*_new_message_locator).click()
        self.wait_for_element_displayed(*self._message_list_locator)

        # verify the last listed received text message
        _received_message = self.marionette.find_elements(
            *self._received_message_content_locator)[-1]

        self.assertIn(
            "Reply\n" + _text_message_content, _received_message.text)

    def tearDown(self):

        # close the app
        if self.app:
            self.apps.kill(self.app)

        GaiaTestCase.tearDown(self)
