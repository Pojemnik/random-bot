const fs = require('fs');
log = require('./logger.js')
let o = {}

exports.create = function createConfig(prefix, token, randmul) {
    o['default_prefix'] = prefix;
    o['token'] = token;
    o['randmul'] = randmul;
    log.log('Config object created');
  }

exports.update = function update(key, val) {
    o[key] = val;
    try {
        fs.writeFileSync('config.json', JSON.stringify(o))
      } catch (err) {
        log.log(`Error while saving JSON: ${err}`);
      }
}