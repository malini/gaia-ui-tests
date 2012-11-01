# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from gaiatest.mocks.mock_contact import MockContact
import time


class TestContacts(GaiaTestCase):

    _add_new_contact_button_locator = ('id', 'add-contact-button')

    _given_name_field_locator = ('id', 'givenName')
    _family_name_field_locator = ('id', 'familyName')
    _email_field_locator = ('id', "email_0")
    _phone_field_locator = ('id', "number_0")
    _street_field_locator = ('id', "streetAddress_0")
    _zip_code_field_locator = ('id', "postalCode_0")
    _city_field_locator = ('id', 'locality_0')
    _country_field_locator = ('id', 'countryName_0')
    _comment_field_locator = ('id', 'note_0')

    _done_button_locator = ('id', 'save-button')

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

    def test_add_new_contact(self):
        # https://moztrap.mozilla.org/manage/case/1309/

        self.wait_for_element_displayed(*self._add_new_contact_button_locator)

        #click Create new contact
        self.marionette.find_element(
            *self._add_new_contact_button_locator).click()
        self.wait_for_element_displayed(*self._given_name_field_locator)

        # Enter data into fields
        self.marionette.find_element(*self._given_name_field_locator).send_keys(self.contact['givenName'])
        self.marionette.find_element(*self._family_name_field_locator).send_keys(self.contact['familyName'])

        self.marionette.find_element(
            *self._phone_field_locator).send_keys(self.contact['tel'])
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

    def tearDown(self):

        # close the app
        if hasattr(self, 'app'):
            self.apps.kill(self.app)
            GaiaTestCase.tearDown(self)