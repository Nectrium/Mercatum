'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _path = require('path');

var _path2 = _interopRequireDefault(_path);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var buildInfo = require(_path2.default.join(process.resourcesPath, 'build_info.json'));

exports.default = buildInfo;
module.exports = exports['default'];