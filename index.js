const { RSA_NO_PADDING } = require('constants');
const Discord = require('discord.js');
const emojis = require('emojis-list');
const cfg = require('./config.js');
const log = require('./logger.js');
const fs = require('fs');

const { default_prefix, token, randmul } = require('./config.json');
const { config } = require('process');
const client = new Discord.Client();
client.commands = new Discord.Collection();

randMultipler = randmul;
prefix = default_prefix;
levelDocs = '';
commandsDocs = '';
const VER = '0.5';

function init() {
  log.log(`Random bot version ${VER}`);
  log.log(`randMultipler set to: ${randMultipler}`);
  log.log(`prefix set to: ${prefix}`);
  log.log(`Logged in as ${client.user.tag}`);
  log.log(`Emoji n=${emojis.length}`);
  cfg.create(prefix, token, randMultipler);
  log.log('Fetching Storkman docs');
  client.commands.forEach(command => {
    if(typeof command.init === "function"){
      command.init();
    }
  });
  //levelDocs = getter.getFileHttps('https://raw.githubusercontent.com/Pojemnik/StorkMan/master/docs/xml%20opisu%20poziomu.txt');
  //commandsDocs = getter.getFileHttps('https://raw.githubusercontent.com/Pojemnik/StorkMan/master/docs/komendy.txt');
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

client.on('ready', () => {
  init();
});

client.on('message', msg => {
  if (msg.author.bot) {
    return;
  }
  if (Math.floor(Math.random() * randMultipler) == 0) {
    msg.react(emojis[Math.floor(Math.random() * emojis.length)]).catch((error) => {
      log.log(error);
    })
  }
  if (msg.content[0] === prefix) {
    try {
      executeCommand(msg);
    } catch (err) {
      log.log(`Unknown error while executing command: ${err}`);
    }
  }
});

const commandFiles = fs.readdirSync('./commands').filter(file => file.endsWith('.js'));
for (const file of commandFiles) {
  const command = require(`./commands/${file}`);
  client.commands.set(command.name, command);
}

client.login(token);