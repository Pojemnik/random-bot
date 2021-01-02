log = require('../logger.js');

module.exports = {
	name: 'setcustommul',
	description: 'Set bot\'s custom multipler (frequency of custom emoji reactions is: number of custim emojis * multipler / number of all emojis) to arg',
	execute(message, args) {
		if (args.length != 1) {
			log.log(`Wrong arguments for command setcustommul: ${args}`);
			message.channel.send('Wrong arguments for command setcustommul!');
		}
		try {
			randMultipler = parseFloat(args[0]);
			log.log(`Custom emoji multipler set to: ${args[0]}`);
			message.channel.send(`Custom emoji multipler set to: ${args[0]}`);
			config_object.set('custommul', randMultipler);
		} catch (err) {
			log.log(`Incorrect custom emoji multipler value!: ${args[0]}`);
			log.log(`Error: ${err}`);
			message.channel.send('Incorrect custom emoji multipler value!');
		}
	},
};