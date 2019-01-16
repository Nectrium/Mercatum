'use strict';

const electron = require('electron');
const desktopCapturer = electron.desktopCapturer;

function getDesktopCaptureSources(options) {
  return new Promise((resolve, reject) => {
    desktopCapturer.getSources(options, (err, sources) => {
      if (err != null) {
        return reject(err);
      }
      return resolve(sources.map(source => {
        return {
          id: source.id,
          name: source.name,
          url: source.thumbnail.toDataURL()
        };
      }));
    });
  });
}

module.exports = {
  getDesktopCaptureSources
};