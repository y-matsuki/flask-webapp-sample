function get_all_points() {
  $('div.clickable').each(function() {
    var event = $(this).data('event');
    var user = $(this).data('user');
    var type = $(this).data('type');
    $.get('/point/api/'+event+'/'+user+'/'+type, function(data) {
      user = user.replace('.', '-');
      $('span.'+event+'.'+user+'.'+type).text(data.count);
    });
  });
};

$(document).ready(function() {
  $('div.clickable').click(function() {
    if (!$(this).hasClass('inverted')) {
      var event = $(this).data('event');
      var user = $(this).data('user');
      var type = $(this).data('type');
      $.post('/point/api/'+event+'/'+user+'/'+type);
      //自分が投票した内容はすぐに反映するように変更
      get_all_points();
      $(this).addClass('inverted');
      $(this).delay(1000).queue(function() {
        $(this).removeClass('inverted');
        $(this).dequeue();
      });
    }
  });
  get_all_points();
  var factorial = function cron_task() {
    $(document).delay(10000).queue(function() {
      get_all_points();
      $(this).dequeue();
      cron_task();
    });
  };
  factorial();
});
