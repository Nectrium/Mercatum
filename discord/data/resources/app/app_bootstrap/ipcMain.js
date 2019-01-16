'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _electron = require('electron');

exports.default = {
  on: function on(event, callback) {
    return _electron.ipcMain.on('DISCORD_' + event, callback);
  },
  removeListener: function removeListener(event, callback) {
    return _electron.ipcMain.removeListener('DISCORD_' + event, callback);
  }
};
module.exports = exports['default'];