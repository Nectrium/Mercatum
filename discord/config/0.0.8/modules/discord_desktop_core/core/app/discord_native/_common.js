'use strict';

// Private utilities for discordNativeAPI.
// Don't expose to the public DiscordNative.

const electron = require('electron');

function getCurrentWindow() {
  return electron.remote.getCurrentWindow();
}

module.exports = {
  getCurrentWindow
};