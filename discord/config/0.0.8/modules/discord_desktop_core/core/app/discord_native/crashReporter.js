'use strict';

var _extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; };

const electron = require('electron');
const globals = require('./globals');
const ipcRenderer = require('./ipc');
const crashReporter = electron.crashReporter;

const UPDATE_CRASH_REPORT = 'UPDATE_CRASH_REPORT';

function updateCrashReporter(metadata) {
  const extra = _extends({}, globals.crashReporterMetadata, metadata);
  ipcRenderer.send(UPDATE_CRASH_REPORT, metadata);
  crashReporter.start({
    productName: 'Discord',
    companyName: 'Discord Inc.',
    submitURL: 'http://crash.discordapp.com:1127/post',
    // [adill] remove autoSubmit once all channels are on 2.0.0+
    autoSubmit: true,
    uploadToServer: true,
    ignoreSystemCrashHandler: false,
    extra
  });
}

module.exports = {
  updateCrashReporter
};