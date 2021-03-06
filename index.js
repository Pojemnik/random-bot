const { RSA_NO_PADDING } = require('constants');
const Discord = require('discord.js');
const emojis = require('emojis-list');
const cfg = require('./config.js');
const log = require('./logger.js');
const fs = require('fs');

const { config } = require('process');
const client = new Discord.Client();
client.commands = new Discord.Collection();

const { prefix: default_prefix, token, randmul: default_randmul, reactions: default_reactions, custommul: default_custommul } = require('./config.json');
config_object = new cfg.config(default_prefix, token, default_randmul, default_reactions);

const VERSION = '0.6.4';

function init() {
  loadCommands();
  log.log(`Random bot version ${VERSION}`);
  log.log(`randMultipler set to: ${default_randmul}`);
  log.log(`prefix set to: ${default_prefix}`);
  log.log(`Logged in as ${client.user.tag}`);
  log.log(`Emoji n = ${emojis.length + client.emojis.cache.size}`);
  log.log(`Reactions: ${default_reactions}`);
  log.log(`Custom emoji multipler: ${default_custommul}`);
  log.log('Fetching Storkman docs');
  client.commands.forEach(command => {
    if (typeof command.init === "function") {
      command.init();
    }
  });
}

function executeCommand(msg) {
  cmd = msg.content.substr(1).trim().split(/ +/);
  log.log('--User input--');
  cmd.forEach(element => {
    log.log(element);
  });
  try {
    client.commands.get(cmd[0]).execute(msg, cmd.slice(1));
  } catch {
    msg.channel.send('Incorrect command!');
    log.log(`Incorrect command ${cmd[0]}`);
  }
}

function checkAndRespondToKeywords(msg) {
  let smieszy = ['Mnie śmieszy', 'mnie śmieszy', 'mnie smieszy'];
  let xd = ['XD', 'xd', 'Xd', 'xD'];
  if (smieszy.includes(msg.content.trim())) {
    msg.channel.send('Mnie też').catch((error) => { log.log(error); });
  }
  if (xd.some(x => msg.content.includes(x))) {
    if (Math.floor(Math.random() * config_object.randmul) == 0) {
      msg.channel.send('XD').catch((error) => { log.log(error); });
    }
  }
}

function reactToMessage(msg) {
  let stork = ['Stork', 'stork'];
  if (stork.some(x => msg.content.includes(x))) {
    if (Math.floor(Math.random() * config_object.randmul) == 0) {
      msg.react('788087096845533184').catch((error) => { log.log(error); });
      return;
    }
  }
  let totalEmojis = emojis.length + client.emojis.cache.size * config_object.custommul;
  let randomValue = Math.floor(Math.random() * totalEmojis);
  if (randomValue < emojis.length) {
    msg.react(emojis[randomValue]).catch((error) => {
      log.log(error);
    })
  }
  else {
    msg.react(client.emojis.cache.random()).catch((error) => {
      log.log(error);
    });
  }
}

function loadCommands() {
  const commandFiles = fs.readdirSync('./commands').filter(file => file.endsWith('.js'));
  for (const file of commandFiles) {
    const command = require(`./commands/${file}`);
    client.commands.set(command.name, command);
  }
}

client.login(token);

client.on('ready', () => {
  init();
});

client.on('message', msg => {
  if (msg.author.bot) {
    return;
  }
  if (msg.content[0] == config_object.prefix) {
    try {
      executeCommand(msg);
    } catch (err) {
      log.log(`Unknown error while executing command: ${err}`);
    }
  }
  if (!config_object.reactions) {
    return;
  }
  if (Math.floor(Math.random() * config_object.randmul) == 0) {
    reactToMessage(msg);
  }
  checkAndRespondToKeywords(msg);
});
