const log = require('../logger.js');
const https = require('https');

module.exports = {
    name: 'getleveldocs',
    description: `Displays documentation of Storkman's level`,
    execute(message, args) {
        log.log(`Displaying info about: ${args[0]}`);
        if (args[0] == 'all') {
            message.channel.send(exports.mapDocs);
        }
        else {
            let startRegex = new RegExp(`${args[0]}:*\\s`);
            let str = exports.mapDocs.substr(exports.mapDocs.search('Często używane atrybuty:'));
            let posStart = str.search(startRegex);
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
        let url = 'https://raw.githubusercontent.com/Pojemnik/StorkMan/master/docs/xml%20opisu%20poziomu.txt';
        log.log(`Getting file form ${url}`);
        https.get(url, (resp) => {

            resp.on('data', (chunk) => {
                data += chunk;
            });

            resp.on('end', () => {
                log.log('level docs loaded');
                exports.mapDocs = data;
            });

        }).on("error", (err) => {
            log.log(`Storkman docs loading error.\n Error: ${err.message}\nFile: ${url}`);
        });
    },
};