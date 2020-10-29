log = require('../logger.js');
cfg = require('../config.js');

module.exports = {
	name: 'setrand',
	description: 'Set bot\'s random multipler (frequency of reactions is 1/multipler) to arg',
	execute(message, args) {
		if (args.length != 1) {
			log.log(`Wrong arguments for command setrand: ${args}`);
			message.channel.send('Wrong arguments for command setrand!');
		}
		try {
			randMultipler = parseFloat(args[0]);
			log.log(`randMultipler set to: ${args[0]}`);
			message.channel.send(`randMultipler set to: ${args[0]}`);
			cfg.update('randmul', randMultipler);
		} catch {
			log.log(`Incorrect randMultipler value!: ${args[0]}`);
			message.channel.send('Incorrect randMultipler value!');
		}
	},
};