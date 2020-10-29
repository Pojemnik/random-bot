const log = require('../logger.js');
const cfg = require('../config.js');

module.exports = {
	name: 'setprefix',
	description: 'Set bot\'s command prefix to arg (default one in\"!\")',
	execute(message, args) {
		if (args.length != 1 || args[0].length != 1) {
			log.log(`Wrong arguments for command setprefix: ${args}`);
			message.channel.send('Wrong arguments for command setprefix!');
		  }
		  try {
			prefix = args[0];
			log.log(`prefix set to: ${args[0]}`);
			message.channel.send(`Prefix set to: ${args[0]}`);
			cfg.update('default_prefix', prefix);
		  } catch {
			log.log(`Incorrect prefix value!: ${args[0]}`);
			message.channel.send('Incorrect prefix value!');
		  }
	},
};