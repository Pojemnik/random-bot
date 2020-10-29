const log = require('../logger.js');
const fs = require('fs');
const path = require('path')
const help = fs.readFileSync(path.join(__dirname, '..', 'help.txt')).toString();

module.exports = {
	name: 'help',
	description: 'Display help',
	execute(message, args) {
		log.log('Help sent');
		message.channel.send(help);
	},
};