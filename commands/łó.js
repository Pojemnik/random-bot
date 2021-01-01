log = require('../logger.js');

module.exports = {
	name: 'łó',
	description: 'Łóóóó',
	execute(message, args) {
		if (message.author.id == 'wojtek.367009175688970250') {
			log.log("nie");
			message.channel.send('Nie.');
		}
		else {
			log.log("Łóó");
			message.channel.send('ŁóóÓÓÓÓóÓóÓÓÓóÓóÓÓÓÓóóóóóóÓóóóóóÓÓóÓÓÓÓÓÓóóÓóóÓ');
		}
	},
};