$(document).ready(function(){
			// namespace = '/'; // change to an empty string to use the global namespace
			// var socket;
			// function connect()
			// {
			//	socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
			// }
			// the socket.io documentation recommends sending an explicit package upon connection
			// this is specially important when using the global namespace
			
			

			// handlers for the different forms in the page
			// these send data to the server in a variety of ways
			$('form#emit').submit(function(event) {
				socket.emit('my event', {data: $('#emit_data').val()});
				return false;
			});
			$('form#broadcast').submit(function(event) {
				socket.emit('my broadcast event', {data: $('#broadcast_data').val()});
				return false;
			});
			$('form#join').submit(function(event) {
				socket.emit('join', {room: $('#join_room').val()});
				return false;
			});
			$('form#leave').submit(function(event) {
				socket.emit('leave', {room: $('#leave_room').val()});
				return false;
			});
			$('form#send_room').submit(function(event) {
				socket.emit('my room event', {room: $('#room_name').val(), data: $('#room_data').val()});
				return false;
			});
			$('form#close').submit(function(event) {
				socket.emit('close room', {room: $('#close_room').val()});
				return false;
			});
			$('form#disconnect').submit(function(event) {
				socket.emit('disconnect request');
				return false;
			});

			var App = (function(){
				var instance;
				var el;
				var token;
				var namespace = '/';
				function createInstance()
				{
					var app = {};
					el = {};
					
					cacheElements();
					bind();
					return app;
				}
				function cacheElements()
				{
					el.login_btn  = $("#login_btn");
					el.login_username = $("#login_username");
					el.login_pass = $("#login_pass");
					el.login_container = $("#login_container");
					el.game_container = $("#game_container");
					el.gameTypes = $("#gameTypes");
					el.gameTypeListBtn = $("#gameType_list_btn");

					}
				function bind()
				{
					$(el.login_btn).on("click",login);
					$(el.gameTypeListBtn).on("click",setGameType);
					
				}
				function login()
				{
					user =el.login_username.val();
					pass =el.login_pass.val();
					$.ajax({
						method: "POST",
						url: 'http://' + document.domain + ':' + location.port+'/login',
						data: { user:user, password:pass},
						dataType: "json"
					})
						.done(function( msg ) {
						console.log(msg.error);
						if(!msg.error)
						{
							token=msg.token;
							IOconnect();
						}
						else
						{
							//todo: msg login error
						}
						
						});
				}
				function setGameType()
				{
					type= parseInt(el.gameTypes.val());
					console.log(type);
					socket.emit('gametype', {type: type,token: token});
				}
				function IOconnect()
				{
					socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
					bindConnection();
					el.login_container.css("display","none");
					el.game_container.css("display","block");
				}
				function bindConnection()
				{
					// event handler for server sent data
					// the data is displayed in the "Received" section of the page
					socket.on('list rooms',function(msg)
					{
						console.log(msg);
						msg.rooms.forEach(function(entry) {
							console.log(entry);
							el.gameTypes.append($('<option>', {
								value: entry.value,
								text : entry.name
							}));
						});
					});
					
					socket.on('response error', function(msg) {
						console.log(msg);
						$('#log').append('<br>' + $('<div/>').text('error en  #' + msg.data + ': ' + msg.total).html());
					});
					socket.on('join room', function(msg) {
						console.log(msg);
						$('#log').append('<br>' + $('<div/>').text('you joined #' + msg.data + ' in ' + msg.gametype).html());
					});
					socket.on('user connect', function(msg) {
						console.log(msg);
						$('#log').append('<br>' + $('<div/>').text('Waiting ' + msg.users + '/ ' + msg.total).html());
					});
					socket.on('init game', function(msg) {
						console.log(msg);
						switch(msg.game)
						{
							case 'BINGO': InitBingo(msg.items);
							break;
						}
						$('#log').append('<br>' + $('<div/>').text('Start  ' + msg.game ).html());
					});

					
					socket.on('broadcast', function(msg) {
						$('#log').append('<br>' + $('<div/>').text('Received #' + msg.count + ': ' + msg.data).html());
					});

					// event handler for new connections
					socket.on('connect', function() {
						console.log("token");
						socket.emit('set token', {token: token});
					});
				}
				function initBingo()
				{

				}
				return{
					init: function()
					{
						if (!instance)
						{
							instance = createInstance();
						}
						return instance;
					}
				};
			})();

			var app = App.init();
		});