function get_all_points() {
  $('div.clickable').each(function() {
    var event = $(this).data('event');
    var user = $(this).data('user');
    var type = $(this).data('type');
    $.get('/point/api/'+event+'/'+user+'/'+type, function(data) {
      $('span.'+event+'.'+user+'.'+type).text(JSON.parse(data).count);
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
