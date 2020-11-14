const { RSA_NO_PADDING } = require('constants');
const Discord = require('discord.js');
const emojis = require('emojis-list');
const cfg = require('./config.js');
const log = require('./logger.js');
const fs = require('fs');

const { config } = require('process');
const client = new Discord.Client();
client.commands = new Discord.Collection();

const { prefix: default_prefix, token, randmul: default_randmul, reactions: default_reactions } = require('./config.json');
config_object = new cfg.config(default_prefix, token, default_randmul, default_reactions);

levelDocs = '';
commandsDocs = '';
const VERSION = '0.6';

function init() {
  log.log(`Random bot version ${VERSION}`);
  log.log(`randMultipler set to: ${default_randmul}`);
  log.log(`prefix set to: ${default_prefix}`);
  log.log(`Logged in as ${client.user.tag}`);
  log.log(`Emoji n=${emojis.length}`);
  log.log(`Reactions: ${default_reactions}`);
  log.log('Fetching Storkman docs');
  client.commands.forEach(command => {
    if(typeof command.init === "function"){
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

const commandFiles = fs.readdirSync('./commands').filter(file => file.endsWith('.js'));
for (const file of commandFiles) {
  const command = require(`./commands/${file}`);
  client.commands.set(command.name, command);
}

client.login(token);

client.on('ready', () => {
  init();
});

client.on('message', msg => {
  if (msg.author.bot) {
    return;
  }
  if (config_object.reactions && Math.floor(Math.random() * config_object.randmul) == 0) {
    msg.react(emojis[Math.floor(Math.random() * emojis.length)]).catch((error) => {
      log.log(error);
    })
  }
  if (msg.content[0] == config_object.prefix) {
    try {
      executeCommand(msg);
    } catch (err) {
      log.log(`Unknown error while executing command: ${err}`);
    }
  }
});