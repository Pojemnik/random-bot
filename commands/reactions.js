const log = require('../logger.js');

module.exports = {
	name: 'reactions',
	description: 'Enables/disables random emoji reacting',
	execute(message, args) {
		if (args.length == 0) {
			val = !config_object.reactions;
			config_object.set('reactions', val);
			log.log(`reactions set to: ${val}`);
			message.channel.send(`Reactions set to: ${val}`);
		} else {
			val = (args[0] === 'true') || (args[0] === '1');
			config_object.set('reactions', val);
			log.log(`reactions set to: ${val}`);
			message.channel.send(`Reactions set to: ${val}`);
		}
	},
};