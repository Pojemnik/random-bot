const fs = require('fs');
log = require('./logger.js')

exports.config = class Config {
  constructor(prefix, token, randmul, reactions) {
    this.prefix = prefix;
    this.token = token;
    this.randmul = randmul;
    this.reactions = reactions;
  }

  save() {
    try {
      fs.writeFileSync('config.json', JSON.stringify(this));
    } catch (err) {
      log.log(`Error while saving JSON: ${err}`);
    }
  }

  set(element, value){
    this[element] = value;
    this.save();
  }
}