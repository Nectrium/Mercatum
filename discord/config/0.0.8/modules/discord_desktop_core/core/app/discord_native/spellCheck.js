'use strict';

const electron = require('electron');

function setSpellCheckProvider(locale, autoCorrectWord, provider) {
  electron.webFrame.setSpellCheckProvider(locale, autoCorrectWord, provider);
}

function replaceMisspelling(word) {
  electron.remote.getCurrentWebContents().replaceMisspelling(word);
}

module.exports = {
  setSpellCheckProvider,
  replaceMisspelling
};