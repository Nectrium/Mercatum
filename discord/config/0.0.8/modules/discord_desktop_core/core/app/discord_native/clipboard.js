'use strict';

const electron = require('electron');
const remote = electron.remote;

function copy(text) {
  if (text) {
    remote.clipboard.writeText(text);
  } else {
    remote.getCurrentWebContents().copy();
  }
}

function cut() {
  remote.getCurrentWebContents().cut();
}

function paste() {
  remote.getCurrentWebContents().paste();
}

module.exports = {
  copy,
  cut,
  paste
};