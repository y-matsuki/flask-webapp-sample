function delete_event(event_id) {
  $('.ui.modal').modal({
    closable: false,
    onDeny: function() {
    },
    onApprove: function() {
      $.ajax({
  			"url" : '/event/' + event_id,
  			"type" : "DELETE",
        "success": function() {
          window.location.reload(true);
        }
  		});
    }
  }).modal('show');
};
