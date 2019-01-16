'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.events = exports.NO_PENDING_UPDATES = exports.INSTALLING_MODULE_PROGRESS = exports.INSTALLING_MODULE = exports.INSTALLING_MODULES_FINISHED = exports.DOWNLOADED_MODULE = exports.UPDATE_MANUALLY = exports.DOWNLOADING_MODULES_FINISHED = exports.DOWNLOADING_MODULE_PROGRESS = exports.DOWNLOADING_MODULE = exports.UPDATE_CHECK_FINISHED = exports.INSTALLED_MODULE = exports.CHECKING_FOR_UPDATES = undefined;

var _extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; }; // Manages additional module installation and management.
// We add the module folder path to require() lookup paths here.

// undocumented node API


exports.initPathsOnly = initPathsOnly;
exports.init = init;
exports.checkForUpdates = checkForUpdates;
exports.quitAndInstallUpdates = quitAndInstallUpdates;
exports.isInstalled = isInstalled;
exports.getInstalled = getInstalled;
exports.install = install;
exports.installPendingUpdates = installPendingUpdates;

var _fs = require('fs');

var _fs2 = _interopRequireDefault(_fs);

var _path = require('path');

var _path2 = _interopRequireDefault(_path);

var _module = require('module');

var _module2 = _interopRequireDefault(_module);

var _events = require('events');

var _mkdirp = require('mkdirp');

var _mkdirp2 = _interopRequireDefault(_mkdirp);

var _yauzl = require('yauzl');

var _yauzl2 = _interopRequireDefault(_yauzl);

var _paths = require('./paths');

var paths = _interopRequireWildcard(_paths);

var _Backoff = require('./Backoff');

var _Backoff2 = _interopRequireDefault(_Backoff);

function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } else { var newObj = {}; if (obj != null) { for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) newObj[key] = obj[key]; } } newObj.default = obj; return newObj; } }

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

const originalFs = require('original-fs');

class Events extends _events.EventEmitter {
  emit(...args) {
    process.nextTick(() => super.emit.apply(this, args));
  }
}

class LogStream {
  constructor(logPath) {
    try {
      this.logStream = _fs2.default.createWriteStream(logPath, { flags: 'a' });
    } catch (e) {
      console.error(`Failed to create ${logPath}: ${String(e)}`);
    }
  }

  log(message) {
    message = `[Modules] ${message}`;
    console.log(message);
    if (this.logStream) {
      this.logStream.write(message);
      this.logStream.write('\r\n');
    }
  }

  end() {
    if (this.logStream) {
      this.logStream.end();
      this.logStream = null;
    }
  }
}

// events
const CHECKING_FOR_UPDATES = exports.CHECKING_FOR_UPDATES = 'checking-for-updates';
const INSTALLED_MODULE = exports.INSTALLED_MODULE = 'installed-module';
const UPDATE_CHECK_FINISHED = exports.UPDATE_CHECK_FINISHED = 'update-check-finished';
const DOWNLOADING_MODULE = exports.DOWNLOADING_MODULE = 'downloading-module';
const DOWNLOADING_MODULE_PROGRESS = exports.DOWNLOADING_MODULE_PROGRESS = 'downloading-module-progress';
const DOWNLOADING_MODULES_FINISHED = exports.DOWNLOADING_MODULES_FINISHED = 'downloading-modules-finished';
const UPDATE_MANUALLY = exports.UPDATE_MANUALLY = 'update-manually';
const DOWNLOADED_MODULE = exports.DOWNLOADED_MODULE = 'downloaded-module';
const INSTALLING_MODULES_FINISHED = exports.INSTALLING_MODULES_FINISHED = 'installing-modules-finished';
const INSTALLING_MODULE = exports.INSTALLING_MODULE = 'installing-module';
const INSTALLING_MODULE_PROGRESS = exports.INSTALLING_MODULE_PROGRESS = 'installing-module-progress';
const NO_PENDING_UPDATES = exports.NO_PENDING_UPDATES = 'no-pending-updates';

// settings
const ALWAYS_ALLOW_UPDATES = 'ALWAYS_ALLOW_UPDATES';
const SKIP_HOST_UPDATE = 'SKIP_HOST_UPDATE';
const SKIP_MODULE_UPDATE = 'SKIP_MODULE_UPDATE';
const ALWAYS_BOOTSTRAP_MODULES = 'ALWAYS_BOOTSTRAP_MODULES';
const USE_LOCAL_MODULE_VERSIONS = 'USE_LOCAL_MODULE_VERSIONS';

const request = require('../app_bootstrap/request');
const REQUEST_TIMEOUT = 15000;
const backoff = new _Backoff2.default(1000, 20000);
const events = exports.events = new Events();

let logger;
let locallyInstalledModules;
let moduleInstallPath;
let installedModulesFilePath;
let moduleDownloadPath;
let bootstrapping;
let hostUpdater;
let hostUpdateAvailable;
let skipHostUpdate;
let skipModuleUpdate;
let checkingForUpdates;
let remoteBaseURL;
let remoteQuery;
let settings;
let remoteModuleVersions;
let installedModules;
let download;
let unzip;
let newInstallInProgress;
let localModuleVersionsFilePath;
let updatable;
let bootstrapManifestFilePath;

function initPathsOnly(_buildInfo) {
  if (locallyInstalledModules || moduleInstallPath) {
    return;
  }

  // If we have `localModulesRoot` in our buildInfo file, we do not fetch modules
  // from remote, and rely on our locally bundled ones.
  // Typically used for development mode, or private builds.
  locallyInstalledModules = _buildInfo.localModulesRoot != null;

  if (locallyInstalledModules) {
    if (_module2.default.globalPaths.indexOf(_buildInfo.localModulesRoot) === -1) {
      _module2.default.globalPaths.push(_buildInfo.localModulesRoot);
    }
  } else {
    moduleInstallPath = _path2.default.join(paths.getUserDataVersioned(), 'modules');
    if (_module2.default.globalPaths.indexOf(moduleInstallPath) === -1) {
      _module2.default.globalPaths.push(moduleInstallPath);
    }
  }
}

function init(_endpoint, _settings, _buildInfo) {
  const endpoint = _endpoint;
  settings = _settings;
  const buildInfo = _buildInfo;
  updatable = buildInfo.version != '0.0.0' && !buildInfo.debug || settings.get(ALWAYS_ALLOW_UPDATES);

  initPathsOnly(buildInfo);

  logger = new LogStream(_path2.default.join(paths.getUserData(), 'modules.log'));
  bootstrapping = false;
  hostUpdateAvailable = false;
  checkingForUpdates = false;
  skipHostUpdate = settings.get(SKIP_HOST_UPDATE) || !updatable;
  skipModuleUpdate = settings.get(SKIP_MODULE_UPDATE) || locallyInstalledModules || !updatable;
  localModuleVersionsFilePath = _path2.default.join(paths.getUserData(), 'local_module_versions.json');
  bootstrapManifestFilePath = _path2.default.join(paths.getResources(), 'bootstrap', 'manifest.json');
  installedModules = {};
  remoteModuleVersions = {};
  newInstallInProgress = {};

  download = {
    // currently downloading
    active: false,
    // {name, version}
    queue: [],
    // current queue index being downloaded
    next: 0,
    // download failure count
    failures: 0
  };

  unzip = {
    // currently unzipping
    active: false,
    // {name, version, zipfile}
    queue: [],
    // current queue index being unzipped
    next: 0,
    // unzip failure count
    failures: 0
  };

  logger.log(`Modules initializing`);
  logger.log(`Distribution: ${locallyInstalledModules ? 'local' : 'remote'}`);
  logger.log(`Host updates: ${skipHostUpdate ? 'disabled' : 'enabled'}`);
  logger.log(`Module updates: ${skipModuleUpdate ? 'disabled' : 'enabled'}`);

  if (!locallyInstalledModules) {
    installedModulesFilePath = _path2.default.join(moduleInstallPath, 'installed.json');
    moduleDownloadPath = _path2.default.join(moduleInstallPath, 'pending');
    _mkdirp2.default.sync(moduleDownloadPath);

    logger.log(`Module install path: ${moduleInstallPath}`);
    logger.log(`Module installed file path: ${installedModulesFilePath}`);
    logger.log(`Module download path: ${moduleDownloadPath}`);

    let failedLoadingInstalledModules = false;
    try {
      installedModules = JSON.parse(_fs2.default.readFileSync(installedModulesFilePath));
    } catch (err) {
      failedLoadingInstalledModules = true;
    }

    cleanDownloadedModules(installedModules);

    bootstrapping = failedLoadingInstalledModules || settings.get(ALWAYS_BOOTSTRAP_MODULES);
  }

  hostUpdater = require('../app_bootstrap/hostUpdater');
  // TODO: hostUpdater constants
  hostUpdater.on('checking-for-update', () => events.emit(CHECKING_FOR_UPDATES));
  hostUpdater.on('update-available', () => hostOnUpdateAvailable());
  hostUpdater.on('update-progress', progress => hostOnUpdateProgress(progress));
  hostUpdater.on('update-not-available', () => hostOnUpdateNotAvailable());
  hostUpdater.on('update-manually', newVersion => hostOnUpdateManually(newVersion));
  hostUpdater.on('update-downloaded', () => hostOnUpdateDownloaded());
  hostUpdater.on('error', err => hostOnError(err));
  let setFeedURL = hostUpdater.setFeedURL.bind(hostUpdater);

  remoteBaseURL = `${endpoint}/modules/${buildInfo.releaseChannel}`;
  // eslint-disable-next-line camelcase
  remoteQuery = { host_version: buildInfo.version };

  switch (process.platform) {
    case 'darwin':
      setFeedURL(`${endpoint}/updates/${buildInfo.releaseChannel}?platform=osx&version=${buildInfo.version}`);
      remoteQuery.platform = 'osx';
      break;
    case 'win32':
      // Squirrel for Windows can't handle query params
      // https://github.com/Squirrel/Squirrel.Windows/issues/132
      setFeedURL(`${endpoint}/updates/${buildInfo.releaseChannel}`);
      remoteQuery.platform = 'win';
      break;
    case 'linux':
      setFeedURL(`${endpoint}/updates/${buildInfo.releaseChannel}?platform=linux&version=${buildInfo.version}`);
      remoteQuery.platform = 'linux';
      break;
  }
}

function cleanDownloadedModules(installedModules) {
  try {
    const entries = _fs2.default.readdirSync(moduleDownloadPath) || [];
    entries.forEach(entry => {
      const entryPath = _path2.default.join(moduleDownloadPath, entry);
      let isStale = true;
      for (const moduleName of Object.keys(installedModules)) {
        if (entryPath === installedModules[moduleName].updateZipfile) {
          isStale = false;
          break;
        }
      }

      if (isStale) {
        _fs2.default.unlinkSync(_path2.default.join(moduleDownloadPath, entry));
      }
    });
  } catch (err) {
    logger.log('Could not clean downloaded modules');
    logger.log(err.stack);
  }
}

function hostOnUpdateAvailable() {
  logger.log(`Host update is available.`);
  hostUpdateAvailable = true;
  events.emit(UPDATE_CHECK_FINISHED, true, 1, false);
  events.emit(DOWNLOADING_MODULE, 'host', 1, 1);
}

function hostOnUpdateProgress(progress) {
  logger.log(`Host update progress: ${progress}%`);
  events.emit(DOWNLOADING_MODULE_PROGRESS, 'host', progress);
}

function hostOnUpdateNotAvailable() {
  logger.log(`Host is up to date.`);
  if (!skipModuleUpdate) {
    checkForModuleUpdates();
  } else {
    events.emit(UPDATE_CHECK_FINISHED, true, 0, false);
  }
}

function hostOnUpdateManually(newVersion) {
  logger.log(`Host update is available. Manual update required!`);
  hostUpdateAvailable = true;
  checkingForUpdates = false;
  events.emit(UPDATE_MANUALLY, newVersion);
  events.emit(UPDATE_CHECK_FINISHED, true, 1, true);
}

function hostOnUpdateDownloaded() {
  logger.log(`Host update downloaded.`);
  checkingForUpdates = false;
  events.emit(DOWNLOADED_MODULE, 'host', 1, 1, true);
  events.emit(DOWNLOADING_MODULES_FINISHED, 1, 0);
}

function hostOnError(err) {
  logger.log(`Host update failed: ${err}`);

  // [adill] osx unsigned builds will fire this code signing error inside setFeedURL and
  // if we don't do anything about it hostUpdater.checkForUpdates() will never respond.
  if (err && String(err).indexOf('Could not get code signature for running application') !== -1) {
    console.warn('Skipping host updates due to code signing failure.');
    skipHostUpdate = true;
  }

  checkingForUpdates = false;
  if (!hostUpdateAvailable) {
    events.emit(UPDATE_CHECK_FINISHED, false, 0, false);
  } else {
    events.emit(DOWNLOADED_MODULE, 'host', 1, 1, false);
    events.emit(DOWNLOADING_MODULES_FINISHED, 0, 1);
  }
}

function checkForUpdates() {
  if (checkingForUpdates) return;

  checkingForUpdates = true;
  hostUpdateAvailable = false;
  if (skipHostUpdate) {
    events.emit(CHECKING_FOR_UPDATES);
    hostOnUpdateNotAvailable();
  } else {
    logger.log('Checking for host updates.');
    hostUpdater.checkForUpdates();
  }
}

function getRemoteModuleName(name) {
  if (process.platform === 'win32' && process.arch === 'x64') {
    return `${name}.x64`;
  }

  return name;
}

function checkForModuleUpdates() {
  const query = _extends({}, remoteQuery, { _: Math.floor(Date.now() / 1000 / 60 / 5) });
  const url = `${remoteBaseURL}/versions.json`;
  logger.log(`Checking for module updates at ${url}`);

  request.get({
    url,
    agent: false,
    encoding: null,
    qs: query,
    timeout: REQUEST_TIMEOUT,
    strictSSL: false
  }, (err, response, body) => {
    checkingForUpdates = false;

    if (!err && response.statusCode !== 200) {
      err = new Error(`Non-200 response code: ${response.statusCode}`);
    }

    if (err) {
      logger.log(`Failed fetching module versions: ${String(err)}`);
      events.emit(UPDATE_CHECK_FINISHED, false, 0, false);
      return;
    }

    remoteModuleVersions = JSON.parse(body);
    if (settings.get(USE_LOCAL_MODULE_VERSIONS)) {
      try {
        remoteModuleVersions = JSON.parse(_fs2.default.readFileSync(localModuleVersionsFilePath));
        console.log('Using local module versions: ', remoteModuleVersions);
      } catch (err) {
        console.warn('Failed to parse local module versions: ', err);
      }
    }

    const updatesToDownload = [];
    for (const moduleName of Object.keys(installedModules)) {
      const installedModule = installedModules[moduleName];
      const installed = installedModule.installedVersion;
      if (installed === null) {
        continue;
      }

      const update = installedModule.updateVersion || 0;
      const remote = remoteModuleVersions[getRemoteModuleName(moduleName)] || 0;
      // TODO: strict equality?
      if (installed != remote && update != remote) {
        logger.log(`Module update available: ${moduleName}@${remote} [installed: ${installed}]`);
        updatesToDownload.push({ name: moduleName, version: remote });
      }
    }

    events.emit(UPDATE_CHECK_FINISHED, true, updatesToDownload.length, false);
    if (updatesToDownload.length === 0) {
      logger.log(`No module updates available.`);
    } else {
      updatesToDownload.forEach(e => addModuleToDownloadQueue(e.name, e.version));
    }
  });
}

function addModuleToDownloadQueue(name, version, authToken) {
  download.queue.push({ name, version, authToken });
  process.nextTick(() => processDownloadQueue());
}

function processDownloadQueue() {
  if (download.active) return;
  if (download.queue.length === 0) return;

  download.active = true;

  const queuedModule = download.queue[download.next];
  download.next += 1;

  events.emit(DOWNLOADING_MODULE, queuedModule.name, download.next, download.queue.length);

  let totalBytes = 1;
  let receivedBytes = 0;
  let progress = 0;
  let hasErrored = false;

  const url = `${remoteBaseURL}/${getRemoteModuleName(queuedModule.name)}/${queuedModule.version}`;
  logger.log(`Fetching ${queuedModule.name}@${queuedModule.version} from ${url}`);
  const headers = {};
  if (queuedModule.authToken) {
    headers['Authorization'] = queuedModule.authToken;
  }
  request.get({
    url,
    agent: false,
    encoding: null,
    followAllRedirects: true,
    qs: remoteQuery,
    timeout: REQUEST_TIMEOUT,
    strictSSL: false,
    headers
  }).on('error', err => {
    if (hasErrored) return;
    hasErrored = true;
    logger.log(`Failed fetching ${queuedModule.name}@${queuedModule.version}: ${String(err)}`);
    finishModuleDownload(queuedModule.name, queuedModule.version, null, false);
  }).on('response', response => {
    totalBytes = response.headers['content-length'] || 1;

    const moduleZipPath = _path2.default.join(moduleDownloadPath, `${queuedModule.name}-${queuedModule.version}.zip`);
    logger.log(`Streaming ${queuedModule.name}@${queuedModule.version} [${totalBytes} bytes] to ${moduleZipPath}`);

    const stream = _fs2.default.createWriteStream(moduleZipPath);
    stream.on('finish', () => finishModuleDownload(queuedModule.name, queuedModule.version, moduleZipPath, response.statusCode === 200));

    response.on('data', chunk => {
      receivedBytes += chunk.length;
      stream.write(chunk);

      const fraction = receivedBytes / totalBytes;
      const newProgress = Math.min(Math.floor(100 * fraction), 100);
      if (progress != newProgress) {
        progress = newProgress;
        events.emit(DOWNLOADING_MODULE_PROGRESS, queuedModule.name, progress);
      }
    });

    // TODO: on response error
    // TODO: on stream error

    response.on('end', () => stream.end());
  });
}

function commitInstalledModules() {
  const data = JSON.stringify(installedModules, null, 2);
  _fs2.default.writeFileSync(installedModulesFilePath, data);
}

function finishModuleDownload(name, version, zipfile, succeeded) {
  if (!installedModules[name]) {
    installedModules[name] = {};
  }

  if (succeeded) {
    installedModules[name].updateVersion = version;
    installedModules[name].updateZipfile = zipfile;
    commitInstalledModules();
  } else {
    download.failures += 1;
  }

  events.emit(DOWNLOADED_MODULE, name, download.next, download.queue.length, succeeded);

  if (download.next >= download.queue.length) {
    const successes = download.queue.length - download.failures;
    logger.log(`Finished module downloads. [success: ${successes}] [failure: ${download.failures}]`);
    events.emit(DOWNLOADING_MODULES_FINISHED, successes, download.failures);
    download.queue = [];
    download.next = 0;
    download.failures = 0;
    download.active = false;
  } else {
    const continueDownloads = () => {
      download.active = false;
      processDownloadQueue();
    };

    if (succeeded) {
      backoff.succeed();
      process.nextTick(continueDownloads);
    } else {
      logger.log(`Waiting ${Math.floor(backoff.current)}ms before next download.`);
      backoff.fail(continueDownloads);
    }
  }

  if (newInstallInProgress[name]) {
    addModuleToUnzipQueue(name, version, zipfile);
  }
}

function addModuleToUnzipQueue(name, version, zipfile) {
  unzip.queue.push({ name, version, zipfile });
  process.nextTick(() => processUnzipQueue());
}

function processUnzipQueue() {
  if (unzip.active) return;
  if (unzip.queue.length === 0) return;

  unzip.active = true;

  const queuedModule = unzip.queue[unzip.next];
  unzip.next += 1;

  events.emit(INSTALLING_MODULE, queuedModule.name, unzip.next, unzip.queue.length);

  let hasErrored = false;
  const onError = (error, zipfile) => {
    if (hasErrored) return;
    hasErrored = true;

    logger.log(`Failed installing ${queuedModule.name}@${queuedModule.version}: ${String(error)}`);
    succeeded = false;
    if (zipfile) {
      zipfile.close();
    }
    finishModuleUnzip(queuedModule, succeeded);
  };

  let succeeded = true;
  const extractRoot = _path2.default.join(moduleInstallPath, queuedModule.name);
  logger.log(`Installing ${queuedModule.name}@${queuedModule.version} from ${queuedModule.zipfile}`);

  const processZipfile = (err, zipfile) => {
    if (err) {
      onError(err, null);
      return;
    }

    const totalEntries = zipfile.entryCount;
    let processedEntries = 0;

    zipfile.on('entry', entry => {
      processedEntries += 1;
      const percent = Math.min(Math.floor(processedEntries / totalEntries * 100), 100);
      events.emit(INSTALLING_MODULE_PROGRESS, queuedModule.name, percent);

      // skip directories
      if (/\/$/.test(entry.fileName)) {
        zipfile.readEntry();
        return;
      }

      zipfile.openReadStream(entry, (err, stream) => {
        if (err) {
          onError(err, zipfile);
          return;
        }

        stream.on('error', e => onError(e, zipfile));

        (0, _mkdirp2.default)(_path2.default.join(extractRoot, _path2.default.dirname(entry.fileName)), err => {
          if (err) {
            onError(err, zipfile);
            return;
          }

          // [adill] createWriteStream via original-fs is broken in Electron 4.0.0-beta.6 with .asar files
          // so we unzip to a temporary filename and rename it afterwards
          const tempFileName = _path2.default.join(extractRoot, entry.fileName + '.tmp');
          const finalFileName = _path2.default.join(extractRoot, entry.fileName);
          const writeStream = originalFs.createWriteStream(tempFileName);

          writeStream.on('error', e => {
            stream.destroy();
            try {
              originalFs.unlinkSync(tempFileName);
            } catch (err) {}
            onError(e, zipfile);
          });

          writeStream.on('finish', () => {
            try {
              originalFs.unlinkSync(finalFileName);
            } catch (err) {}
            try {
              originalFs.renameSync(tempFileName, finalFileName);
            } catch (err) {
              onError(err, zipfile);
              return;
            }
            zipfile.readEntry();
          });

          stream.pipe(writeStream);
        });
      });
    });

    zipfile.on('error', err => {
      onError(err, zipfile);
    });

    zipfile.on('end', () => {
      if (!succeeded) return;

      installedModules[queuedModule.name].installedVersion = queuedModule.version;
      finishModuleUnzip(queuedModule, succeeded);
    });

    zipfile.readEntry();
  };

  try {
    _yauzl2.default.open(queuedModule.zipfile, { lazyEntries: true, autoClose: true }, processZipfile);
  } catch (err) {
    onError(err, null);
  }
}

function finishModuleUnzip(unzippedModule, succeeded) {
  delete newInstallInProgress[unzippedModule.name];
  delete installedModules[unzippedModule.name].updateZipfile;
  delete installedModules[unzippedModule.name].updateVersion;
  commitInstalledModules();

  if (!succeeded) {
    unzip.failures += 1;
  }

  events.emit(INSTALLED_MODULE, unzippedModule.name, unzip.next, unzip.queue.length, succeeded);

  if (unzip.next >= unzip.queue.length) {
    const successes = unzip.queue.length - unzip.failures;
    bootstrapping = false;
    logger.log(`Finished module installations. [success: ${successes}] [failure: ${unzip.failures}]`);
    unzip.queue = [];
    unzip.next = 0;
    unzip.failures = 0;
    unzip.active = false;
    events.emit(INSTALLING_MODULES_FINISHED, successes, unzip.failures);
    return;
  }

  process.nextTick(() => {
    unzip.active = false;
    processUnzipQueue();
  });
}

function quitAndInstallUpdates() {
  logger.log(`Relaunching to install ${hostUpdateAvailable ? 'host' : 'module'} updates...`);
  if (hostUpdateAvailable) {
    hostUpdater.quitAndInstall();
  } else {
    relaunch();
  }
}

function relaunch() {
  logger.end();
  const { app } = require('electron');
  app.relaunch();
  app.quit();
}

function isInstalled(name, version) {
  const metadata = installedModules[name];
  if (locallyInstalledModules) return true;
  if (metadata && metadata.installedVersion > 0) {
    if (!version) return true;
    if (metadata.installedVersion === version) return true;
  }
  return false;
}

function getInstalled() {
  return _extends({}, installedModules);
}

function install(name, defer, options) {
  let { version, authToken } = options || {};
  if (isInstalled(name, version)) {
    if (!defer) {
      events.emit(INSTALLED_MODULE, name, 1, 1, true);
    }
    return;
  }

  if (newInstallInProgress[name]) return;

  if (!updatable) {
    logger.log(`Not updatable; ignoring request to install ${name}...`);
    return;
  }

  if (defer) {
    if (version) {
      throw new Error(`Cannot defer install for a specific version module (${name}, ${version})`);
    }
    logger.log(`Deferred install for ${name}...`);
    installedModules[name] = { installedVersion: 0 };
    commitInstalledModules();
  } else {
    logger.log(`Starting to install ${name}...`);
    if (!version) {
      version = remoteModuleVersions[name] || 0;
    }
    newInstallInProgress[name] = version;
    addModuleToDownloadQueue(name, version, authToken);
  }
}

function installPendingUpdates() {
  const updatesToInstall = [];

  if (bootstrapping) {
    let modules = {};
    try {
      modules = JSON.parse(_fs2.default.readFileSync(bootstrapManifestFilePath));
    } catch (err) {}

    for (const moduleName of Object.keys(modules)) {
      installedModules[moduleName] = { installedVersion: 0 };
      const zipfile = _path2.default.join(paths.getResources(), 'bootstrap', `${moduleName}.zip`);
      updatesToInstall.push({ moduleName, update: modules[moduleName], zipfile });
    }
  }

  for (const moduleName of Object.keys(installedModules)) {
    const update = installedModules[moduleName].updateVersion || 0;
    const zipfile = installedModules[moduleName].updateZipfile;
    if (update > 0 && zipfile != null) {
      updatesToInstall.push({ moduleName, update, zipfile });
    }
  }

  if (updatesToInstall.length > 0) {
    logger.log(`${bootstrapping ? 'Bootstrapping' : 'Installing updates'}...`);
    updatesToInstall.forEach(e => addModuleToUnzipQueue(e.moduleName, e.update, e.zipfile));
  } else {
    logger.log('No updates to install');
    events.emit(NO_PENDING_UPDATES);
  }
}