log = require('../logger.js');

module.exports = {
	name: 'log',
	description: 'Show bot\'s log',
	execute(message, args) {
	    log.log("Log shown");
        message.channel.send(log.getLog());
	},
};