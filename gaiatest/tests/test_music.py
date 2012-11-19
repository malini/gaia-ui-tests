# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
import time

class TestMusic(GaiaTestCase):

  _album_tile_locator = ('xpath', ".//*[@id='views-list']/li/a")
  _player_seek_elapsed_locator = ('id', 'player-seek-elapsed')
  _player_controls_play_locator = ('id', 'player-controls-play')
  _tab_albums_locator = ('id', 'tabs-albums')
  _throbber_locator = ('id', 'throbber')
  _views_player_locator = ('id', 'views-player')
  _views_sublist_controls_play_locator = ('id', 'views-sublist-controls-play')

  def setUp(self):
      GaiaTestCase.setUp(self)

      self.assertTrue(self.lockscreen.unlock())

      # launch the Music application
      self.app = self.apps.launch("music")

  def test_select_album_play(self):

      # wait for loaded music
      self.wait_for_element_not_displayed(*self._throbber_locator)

      # switch to albums view
      self.marionette.find_element(*self._tab_albums_locator).click()

      # check that an album is displayed
      self.wait_for_element_displayed(*self._album_tile_locator)
      self.assertTrue(
          self.marionette.find_element(*self._album_tile_locator).is_displayed())

      # select an album
      self.marionette.find_element(*self._album_tile_locator).click()

      # select play
      self.marionette.find_element(*self._views_sublist_controls_play_locator).click()

      # play for a short duration
      self.wait_for_condition(lambda m: m.find_element(
          *self._player_seek_elapsed_locator).text == '00:05')

      # select stop
      self.marionette.find_element(*self._player_controls_play_locator).click()

      # TODO
      # Validate audio playback

  def tearDown(self):
      # close the app
      if hasattr(self, 'app'):
          self.apps.kill(self.app)

      GaiaTestCase.tearDown(self)
