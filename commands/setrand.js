log = require('../logger.js');

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
			config_object.set('randmul', randMultipler);
		} catch (err) {
			log.log(`Incorrect randMultipler value!: ${args[0]}`);
			log.log(`Error: ${err}`);
			message.channel.send('Incorrect randMultipler value!');
		}
	},
};