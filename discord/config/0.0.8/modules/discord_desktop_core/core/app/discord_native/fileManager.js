'use strict';

const electron = require('electron');
const fs = require('fs');
const os = require('os');
const path = require('path');
const originalFs = require('original-fs');
const remoteDialog = electron.remote.dialog;
const remoteShell = electron.remote.shell;

const INVALID_FILENAME_CHAR_REGEX = /[^a-zA-Z0-9-_.]/g;

function saveWithDialog(fileContents, fileName) {
  if (INVALID_FILENAME_CHAR_REGEX.test(fileName)) {
    throw new Error(`fileName has invalid characters`);
  }
  const defaultPath = path.join(os.homedir(), fileName);

  remoteDialog.showSaveDialog({ defaultPath }, selectedFileName => {
    selectedFileName && fs.writeFileSync(selectedFileName, fileContents);
  });
}

function showOpenDialog(dialogOptions) {
  return new Promise(resolve => remoteDialog.showOpenDialog(dialogOptions, resolve));
}

function showItemInFolder(path) {
  return remoteShell.showItemInFolder(path);
}

function openFiles(dialogOptions, maxSize, makeFile) {
  return showOpenDialog(dialogOptions).then(filenames => {
    if (filenames == null) return;

    return Promise.all(filenames.map(filename => new Promise((resolve, reject) => {
      originalFs.stat(filename, (err, stats) => {
        if (err) return reject(err);

        if (stats.size > maxSize) {
          const err = new Error('upload too large');
          // used to help determine why openFiles failed
          err.code = 'ETOOLARGE';
          return reject(err);
        }

        originalFs.readFile(filename, (err, data) => {
          if (err) return reject(err);
          return resolve(makeFile(data.buffer, path.basename(filename)));
        });
      });
    })));
  });
}

module.exports = {
  saveWithDialog,
  openFiles,
  showOpenDialog,
  showItemInFolder,
  extname: path.extname,
  basename: path.basename,
  dirname: path.dirname,
  join: path.join
};