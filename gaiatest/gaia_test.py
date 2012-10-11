# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette import MarionetteTestCase
from marionette.errors import NoSuchElementException
import os
import time

class LockScreen(object):

    def __init__(self, marionette):
        self.marionette = marionette

    def unlock(self):
        success = self.marionette.execute_async_script("""
let setlock = window.wrappedJSObject.SettingsListener.getSettingsLock();
let obj = {'screen.timeout': 0};
setlock.set(obj);
waitFor(
    function() {
        window.wrappedJSObject.LockScreen.unlock();
        waitFor(
            function() {
                finish(window.wrappedJSObject.LockScreen.locked);
            },
            function() {
                return !window.wrappedJSObject.LockScreen.locked;
            }
        );
    },
    function() {
        return !!window.wrappedJSObject.LockScreen;
    }
);
""")
        return success


class GaiaApp(object):

    def __init__(self, origin=None, name=None, frame_id=None, src=None):
        self.frame_id = frame_id
        self.src = src
        self.name = name
        self.origin = origin


class GaiaApps(object):

    def __init__(self, marionette):
        self.marionette = marionette
        js = os.path.abspath(os.path.join(__file__, os.path.pardir, "gaia_apps.js"))
        self.marionette.import_script(js)

    def launch(self, name):
        result = self.marionette.execute_async_script("launchAppWithName('%s')" % name)
        app = GaiaApp(frame_id=result.get('frame'),
                      src=result.get('src'),
                      name=result.get('name'),
                      origin=result.get('origin'))
        return app

    def kill(self, app):
        self.marionette.switch_to_frame()
        js = os.path.abspath(os.path.join(__file__, os.path.pardir, "gaia_apps.js"))
        self.marionette.import_script(js)
        self.marionette.execute_script("window.wrappedJSObject.WindowManager.kill('%s');"
                                        % app.origin)


class GaiaTestCase(MarionetteTestCase):

    def setUp(self):
        MarionetteTestCase.setUp(self)
        # the emulator can be really slow!
        self.marionette.set_script_timeout(60000)
        self.lockscreen = LockScreen(self.marionette)
        self.apps = GaiaApps(self.marionette)

    def wait_for_element_present(self, by, locator, timeout=10):
        timeout = float(timeout) + time.time()

        while time.time() < timeout:
            time.sleep(0.5)
            try:
                self.marionette.find_element(by, locator)
                break
            except NoSuchElementException:
                pass
        else:
            raise Exception('Element %s not found before timeout' % locator)


    def wait_for_element_not_present(self, by, locator, timeout=10):
        timeout = float(timeout) + time.time()

        while time.time() < timeout:
            time.sleep(0.5)
            try:
                self.marionette.find_element(by, locator)
            except NoSuchElementException:
                break
        else:
            raise Exception('Element %s not found before timeout' % locator)


    def tearDown(self):
        self.lockscreen = None
        self.apps = None
        MarionetteTestCase.tearDown(self)