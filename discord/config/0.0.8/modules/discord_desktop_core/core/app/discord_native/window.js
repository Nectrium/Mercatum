'use strict';

const electron = require('electron');
const EventEmitter = require('events');
const process = require('process');
const common = require('./_common');
const remoteMenu = electron.remote.Menu;
const webFrame = electron.webFrame;

function flashFrame(flag) {
  const currentWindow = common.getCurrentWindow();
  if (currentWindow == null || currentWindow.flashFrame == null) return;
  currentWindow.flashFrame(!currentWindow.isFocused() && flag);
}

function minimize() {
  const win = common.getCurrentWindow();
  if (win == null) return;
  win.minimize();
}

function restore() {
  const win = common.getCurrentWindow();
  if (win == null) return;
  win.restore();
}

function maximize() {
  const win = common.getCurrentWindow();
  if (win == null) return;
  if (win.isMaximized()) {
    win.unmaximize();
  } else {
    win.maximize();
  }
}

function focus(hack) {
  const win = common.getCurrentWindow();
  // Windows does not respect the focus call always.
  // This uses a hack defined in https://github.com/electron/electron/issues/2867
  // Should be used sparingly because it can effect window managers.
  if (hack && process.platform === 'win32') {
    win.setAlwaysOnTop(true);
    win.focus();
    win.setAlwaysOnTop(false);
  } else {
    win.focus();
  }
}

function blur() {
  const win = common.getCurrentWindow();
  if (win != null && !win.isDestroyed()) {
    win.blur();
  }
}

function setProgressBar(progress) {
  const win = common.getCurrentWindow();
  if (win == null) return;
  win.setProgressBar(progress);
}

function fullscreen() {
  const currentWindow = common.getCurrentWindow();
  currentWindow.setFullScreen(!currentWindow.isFullScreen());
}

function close() {
  if (process.platform === 'darwin') {
    remoteMenu.sendActionToFirstResponder('hide:');
  } else {
    common.getCurrentWindow().close();
  }
}

function setZoomFactor(factor) {
  if (!webFrame.setZoomFactor) return;
  webFrame.setZoomFactor(factor / 100);
}

const webContents = common.getCurrentWindow().webContents;
class WebContents extends EventEmitter {
  constructor() {
    super();

    webContents.removeAllListeners('devtools-opened');
    webContents.on('devtools-opened', () => {
      this.emit('devtools-opened');
    });
  }

  setBackgroundThrottling(enabled) {
    if (webContents.setBackgroundThrottling != null) {
      webContents.setBackgroundThrottling(enabled);
    }
  }
}

module.exports = {
  flashFrame,
  minimize,
  restore,
  maximize,
  focus,
  blur,
  fullscreen,
  close,
  setZoomFactor,
  webContents: new WebContents(),
  setProgressBar
};