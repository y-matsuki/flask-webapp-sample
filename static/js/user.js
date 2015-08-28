var username = $('title').text();
console.log('hello, ' + username + '!');
$.get('/api/user', function(data){
  console.log(data);
});
