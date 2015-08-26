var username = $('title').text();
console.log('hello, ' + username + '!');
$.get('/api/hoge', function(data){
  console.log(data);
});
