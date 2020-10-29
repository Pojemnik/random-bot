logContent = '';

exports.getLog = function(){
    return logContent;
}

exports.log = function(o){
    console.log(o);
    logContent += o + '\n';
}

exports.clear = function(){
    logContent = '';
    this.log('Log cleared by user');
}