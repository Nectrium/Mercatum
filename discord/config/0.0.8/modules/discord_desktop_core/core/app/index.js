'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.startup = startup;
exports.handleSingleInstance = handleSingleInstance;
exports.setMainWindowVisible = setMainWindowVisible;
const { Menu } = require('electron');

let mainScreen;
function startup(bootstrapModules) {
  // below modules are required and initted
  // in this order to prevent dependency conflicts
  // please don't tamper with the order unless you know what you're doing
  require('./bootstrapModules').init(bootstrapModules);

  require('./paths');
  require('./splashScreen');
  const moduleUpdater = require('./moduleUpdater');
  require('./autoStart');
  require('./buildInfo');
  const appSettings = require('./appSettings');

  const Constants = require('./Constants');
  Constants.init(bootstrapModules.Constants);

  const errorReporting = require('./errorReporting');
  errorReporting.init();

  const appFeatures = require('./appFeatures');
  appFeatures.init();

  const GPUSettings = require('./GPUSettings');
  bootstrapModules.GPUSettings.replace(GPUSettings);

  const rootCertificates = require('./rootCertificates');
  rootCertificates.init();

  // expose globals that will be imported by the webapp
  // global.releaseChannel is set in bootstrap
  global.crashReporterMetadata = errorReporting.metadata;
  global.mainAppDirname = Constants.MAIN_APP_DIRNAME;
  global.features = appFeatures.getFeatures();
  global.appSettings = appSettings.getSettings();
  // this gets updated when launching a new main app window
  global.mainWindowId = Constants.DEFAULT_MAIN_WINDOW_ID;
  global.moduleUpdater = moduleUpdater;

  const applicationMenu = require('./applicationMenu');
  Menu.setApplicationMenu(applicationMenu);

  mainScreen = require('./mainScreen');
  mainScreen.init();
}

function handleSingleInstance(args) {
  mainScreen.handleSingleInstance(args);
}

function setMainWindowVisible(visible) {
  mainScreen.setMainWindowVisible(visible);
}