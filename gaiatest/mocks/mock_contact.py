#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json


class MockContact(dict):

    def __init__(self, **kwargs):
        # set your default values
        import time
        self['givenName'] = 'gaia%s' % repr(time.time()).replace('.', '')[10:]
        self['familyName'] = "test"
        self['name'] = self['givenName'] + " " + self['familyName']
        self['email'] = '%s@restmail.net' % self['givenName']
        self['tel'] = "07011111111"
        self['street'] = "101 Testing street"
        self['zip'] = "90210"
        self['city'] = "London"
        self['country'] = "UK"
        self['comment'] = "Gaia automated test"

        # update with any keyword arguments passed
        self.update(**kwargs)

    # allow getting items as if they were attributes
    def __getattr__(self, attr):
        return self[attr]

    def json(self):
        return json.dumps(self)
