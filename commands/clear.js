log = require('../logger.js');

module.exports = {
	name: 'clear',
	description: 'Clear bot\'s log',
	execute(message, args) {
	    log.clear();
    	message.channel.send('Log cleared');
	},
};