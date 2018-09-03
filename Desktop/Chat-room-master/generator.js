let count=0
module.exports = {
       //必選，創建連接後要做的事情
       onConnect : function(client, done) {
       //向服務器發送消息
       //client為客户端的連接實例
       client.emit('new user',count);
       //回調函數
       done();
       },
       //必選，向服務器發送消息時運行的代碼
       sendMessage : function(client, done) {
       client.emit('send message',{"msg": "hi hi","nick": count++});
       done();
       },

       options : {
         // realm: 'chat'
       }
};