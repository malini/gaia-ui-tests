# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from gaiatest.mocks.mock_contact import MockContact
import unittest
import time


class TestContacts(GaiaTestCase):

    _loading_overlay = ('id', 'loading-overlay')

    _sms_app_iframe_locator = ('css selector', 'iframe[src="app://sms.gaiamobile.org/index.html"]')

    # Header buttons
    _add_new_contact_button_locator = ('id', 'add-contact-button')
    _done_button_locator = ('id', 'save-button')
    _edit_contact_button_locator = ('id', 'edit-contact-button')
    _details_back_button_locator = ('id', 'details-back')

    # Contact details panel
    _contact_name_title = ('id', 'contact-name-title')
    _send_sms_button_locator = ('id', 'send-sms-button-0')
    _call_phone_number_button_locator = ('id', 'call-or-pick-0')

    # New/Edit contact fields
    _given_name_field_locator = ('id', 'givenName')
    _family_name_field_locator = ('id', 'familyName')
    _email_field_locator = ('id', "email_0")
    _phone_field_locator = ('id', "number_0")
    _street_field_locator = ('id', "streetAddress_0")
    _zip_code_field_locator = ('id', "postalCode_0")
    _city_field_locator = ('id', 'locality_0')
    _country_field_locator = ('id', 'countryName_0')
    _comment_field_locator = ('id', 'note_0')

    #SMS app locators
    _sms_app_header_locator = ('id', 'header-text')

    def setUp(self):
        GaiaTestCase.setUp(self)

        self.assertTrue(self.lockscreen.unlock())

        self.contact = MockContact()

        # launch the Contacts app
        self.app = self.apps.launch('Contacts')
        self.assertTrue(self.app.frame_id is not None)

        # switch into the Contact's frame
        self.marionette.switch_to_frame(self.app.frame_id)
        url = self.marionette.get_url()
        self.assertTrue('communications' in url, 'wrong url: %s' % url)

        self.wait_for_element_not_displayed(*self._loading_overlay)


    def test_add_new_contact(self):
        # https://moztrap.mozilla.org/manage/case/1309/
        #click Create new contact

        self.marionette.find_element(
            *self._add_new_contact_button_locator).click()
        self.wait_for_element_displayed(*self._given_name_field_locator)

        # Enter data into fields
        self.marionette.find_element(*self._given_name_field_locator).send_keys(self.contact['givenName'])
        self.marionette.find_element(*self._family_name_field_locator).send_keys(self.contact['familyName'])

        self.marionette.find_element(
            *self._phone_field_locator).send_keys(self.contact['tel']['value'])
        self.marionette.find_element(
            *self._email_field_locator).send_keys(self.contact['email'])

        self.marionette.find_element(
            *self._street_field_locator).send_keys(self.contact['street'])
        self.marionette.find_element(
            *self._zip_code_field_locator).send_keys(self.contact['zip'])
        self.marionette.find_element(
            *self._city_field_locator).send_keys(self.contact['city'])
        self.marionette.find_element(
            *self._country_field_locator).send_keys(self.contact['country'])

        self.marionette.find_element(
            *self._comment_field_locator).send_keys(self.contact['comment'])

        done_button = self.marionette.find_element(*self._done_button_locator)
        done_button.click()

        contact_locator = (
            'xpath', "//strong/b[text()='%s']" % self.contact['givenName'])
        self.wait_for_element_displayed(*contact_locator)


    def test_edit_contact(self):
        # https://moztrap.mozilla.org/manage/case/1310/
        # First insert a new contact to edit

        self.data_layer.insert_contact(self.contact)
        self.marionette.refresh()

        contact_locator = ('xpath',"//li[@class='block-item'][descendant::b[text()='%s']]"
            % self.contact['givenName'])
        self.wait_for_element_displayed(*contact_locator)

        self.marionette.find_element(*contact_locator).click()

        self.wait_for_element_displayed(*self._edit_contact_button_locator)
        self.marionette.find_element(*self._edit_contact_button_locator).click()

        # Now we'll update the mock contact and then insert the new values into the UI
        self.contact['givenName'] = 'gaia%s' % repr(time.time()).replace('.', '')[10:]
        self.contact['familyName'] = "testedit"
        self.contact['tel']['value'] = "02011111111"

        given_name_field = self.marionette.find_element(*self._given_name_field_locator)
        given_name_field.clear()
        given_name_field.send_keys(self.contact['givenName'])

        family_name_field = self.marionette.find_element(*self._family_name_field_locator)
        family_name_field.clear()
        family_name_field.send_keys(self.contact['familyName'])

        tel_field = self.marionette.find_element(*self._phone_field_locator)
        tel_field.clear()
        tel_field.send_keys(self.contact['tel']['value'])

        self.marionette.find_element(*self._done_button_locator).click()

        self.marionette.find_element(*self._details_back_button_locator).click()

        contact_locator = ('xpath',"//li[@class='block-item'][descendant::b[text()='%s']]"
            % self.contact['givenName'])

        # click back into the contact
        edited_contact = self.wait_for_element_present(*contact_locator)
        edited_contact.click()

        # Now assert that the values have updated
        full_name = self.contact['givenName'] + " " + self.contact['familyName']

        self.assertEqual(self.marionette.find_element(*self._contact_name_title).text,
            full_name)
        self.assertEqual(self.marionette.find_element(*self._call_phone_number_button_locator).text,
            self.contact['tel']['value'])


    @unittest.skip("Scheduled for deletion as this makes a call")
    def test_call_contact(self):
        # Setup text message from a contact
        # We can use the mock phone number because we don't
        # want to actually make the call

        self.data_layer.insert_contact(self.contact)
        self.marionette.refresh()

        contact_locator = ('xpath',"//li[@class='block-item'][descendant::b[text()='%s']]" % self.contact['givenName'])
        self.wait_for_element_displayed(*contact_locator)

        self.marionette.find_element(*contact_locator).click()
        time.sleep(2)
        self.marionette.find_element(*self._call_phone_number_button_locator).click()

        self.marionette.switch_to_frame()

        #print self.marionette.page_source
        #self.marionette.switch_to_frame(dialer)
        # TODO Verify the dialer has opened and displays the phone number in dialer


    def test_sms_contact(self):
        # https://moztrap.mozilla.org/manage/case/1314/
        # Setup a text message from a contact

        self.data_layer.insert_contact(self.contact)
        self.marionette.refresh()

        contact_locator = ('xpath',"//li[@class='block-item'][descendant::b[text()='%s']]" % self.contact['givenName'])
        self.wait_for_element_displayed(*contact_locator)

        self.marionette.find_element(*contact_locator).click()

        self.wait_for_element_displayed(*self._send_sms_button_locator)
        self.marionette.find_element(*self._send_sms_button_locator).click()

        self.marionette.switch_to_frame()

        sms_iframe = self.marionette.find_element(*self._sms_app_iframe_locator)
        self.marionette.switch_to_frame(sms_iframe)

        self.wait_for_element_displayed(*self._sms_app_header_locator)

        header_element = self.marionette.find_element(*self._sms_app_header_locator)
        expected_name = self.contact['givenName'] + " " + self.contact['familyName']
        expected_tel = self.contact['tel']['value']

        self.assertEqual(header_element.text, expected_name)
        self.assertEqual(header_element.get_attribute('data-phone-number'),
            expected_tel)

    def tearDown(self):

        if hasattr(self, 'contact'):
            # Have to switch back to Contacts frame to remove the contact
            self.marionette.switch_to_frame()
            self.marionette.switch_to_frame(self.app.frame_id)
            self.data_layer.remove_contact(self.contact)

        # close all apps
        self.apps.kill_all()
