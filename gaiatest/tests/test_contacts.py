# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from gaiatest.mocks.mock_contact import MockContact

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

    def aatest_add_new_contact(self):
        # https://moztrap.mozilla.org/manage/case/1309/

        self.assertTrue(self.lockscreen.unlock())

        contact = MockContact()

        # launch the Contacts app
        app = self.apps.launch('Contacts')
        self.assertTrue(app.frame_id is not None)

        # switch into the Contact's frame
        self.marionette.switch_to_frame(app.frame_id)
        url = self.marionette.get_url()
        self.assertTrue('communications' in url, 'wrong url: %s' % url)

        self.wait_for_element_displayed(*self._add_new_contact_button_locator)

        #click Create new contact
        self.marionette.find_element(*self._add_new_contact_button_locator).click()
        self.wait_for_element_displayed(*self._given_name_field_locator)

        # Enter data into fields
        self.marionette.find_element(*self._given_name_field_locator).send_keys(contact['first_name'])
        self.marionette.find_element(*self._family_name_field_locator).send_keys(contact['last_name'])

        self.marionette.find_element(*self._phone_field_locator).send_keys(contact['phone_no'])
        self.marionette.find_element(*self._email_field_locator).send_keys(contact['email'])

        self.marionette.find_element(*self._street_field_locator).send_keys(contact['street'])
        self.marionette.find_element(*self._zip_code_field_locator).send_keys(contact['zip'])
        self.marionette.find_element(*self._city_field_locator).send_keys(contact['city'])
        self.marionette.find_element(*self._country_field_locator).send_keys(contact['country'])

        self.marionette.find_element(*self._comment_field_locator).send_keys(contact['comment'])

        done_button = self.marionette.find_element(*self._done_button_locator)
        done_button.click()

        contact_locator = ('xpath',"//strong/b[text()='%s']" % contact['first_name'])
        self.wait_for_element_displayed(*contact_locator)

        # close the app
        self.apps.kill(app)


    def test_call_contact(self):

        contact = MockContact()
        self.data.insert_contact(contact)

        import time
        time.sleep(5)

        self.assertTrue(self.lockscreen.unlock())

        # launch the Contacts app
        app = self.apps.launch('Contacts')
        self.assertTrue(app.frame_id is not None)

        # switch into the Contact's frame
        self.marionette.switch_to_frame(app.frame_id)
        url = self.marionette.get_url()
        self.assertTrue('communications' in url, 'wrong url: %s' % url)

        time.sleep(10)

        # close the app
        self.apps.kill(app)
