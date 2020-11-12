const log = require('../logger.js');
const https = require('https');

module.exports = {
    name: 'getcommanddocs',
    description: `Displays documentation of Storkman's commands`,
    execute(message, args) {
        log.log(`Displaying info about: ${args[0]}`);
        if (args[0] == 'all') {
            message.channel.send(exports.mapDocs);
        }
        else {
            let str = exports.mapDocs.substr(exports.mapDocs.search('Wyświetlanie/debug:'));
            let posStart = str.search(args[0]);
            if(posStart == -1){
                log.log(`Incorrect argument: ${args[0]}`);
                message.channel.send(`Incorrect argument: ${args[0]}`);
                return;
            }
            let temp = str.substr(posStart);
            let endRegex = new RegExp(/\\n\w|\n\w|.$/);
            let posEnd = temp.search(endRegex);
            if (posEnd != -1) {
                message.channel.send(temp.substr(0, posEnd));
            }
            else {
                message.channel.send(temp);
            }
        }
    },
    init() {
        exports.mapDocs = 'None';
        let data = '';
        let url = 'https://raw.githubusercontent.com/Pojemnik/StorkMan/master/docs/komendy.txt';
        log.log(`Getting file form ${url}`);
        https.get(url, (resp) => {

            resp.on('data', (chunk) => {
                data += chunk;
            });

            resp.on('end', () => {
                log.log('command docs loaded');
                exports.mapDocs = data;
            });

        }).on("error", (err) => {
            log.log(`Storkman docs loading error.\n Error: ${err.message}\nFile: ${url}`);
        });
    },
};