var username = $('title').text();
console.log('hello, ' + username + '!');
$.get('/user/api', function(data){
  console.log(data);
});
