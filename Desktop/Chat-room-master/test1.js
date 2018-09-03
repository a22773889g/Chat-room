var express = require('express'),
     app = express(),
     server = require('http').createServer(app),
     io = require('socket.io').listen(server),
     nicknames = [];
server.listen(1111);
app.get('/', function(req, res){
     res.sendfile(__dirname + '/index.html');
});
app.use('/public', express.static(__dirname + '/public'));
var led ,buzzer;
io.sockets.on('connection', function(socket) {
  console.log(socket.id)
     socket.on('new user', function(data){
          console.log(data);
          if (nicknames.indexOf(data) != -1) {
          } else {
               socket.emit('chat', 'SERVER', '歡迎光臨 ' + data);
               socket.nickname = data;
               nicknames.push(socket.nickname);
               io.sockets.emit('usernames', nicknames);
               updateNicknames();
          }
     });
  function updateNicknames(){
          io.sockets.emit('usernames', nicknames,broadcast=true);
     }
  socket.on('send message', function(data){
          io.sockets.emit('new message', { 'msg': data, 'nick': socket.nickname},broadcast=true );
     });
  socket.on('disconnect', function(data){
          if (!socket.nickname) return;
          io.sockets.emit('chat', 'SERVER', socket.nickname + ' 離開了聊天室～');
          nicknames.splice(nicknames.indexOf(socket.nickname), 1);
          updateNicknames();
     });
  });
app.locals = {
 test: 'Extended Express Example'
};


