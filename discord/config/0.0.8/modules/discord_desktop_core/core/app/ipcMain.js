'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _electron = require('electron');

exports.default = {
  on: (event, callback) => _electron.ipcMain.on(`DISCORD_${event}`, callback),
  removeListener: (event, callback) => _electron.ipcMain.removeListener(`DISCORD_${event}`, callback)
};
module.exports = exports['default'];