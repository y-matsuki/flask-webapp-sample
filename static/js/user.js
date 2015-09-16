function delete_user(username) {
  $('.ui.modal').modal({
    closable: false,
    onDeny: function() {
    },
    onApprove: function() {
      $.ajax({
  			"url" : '/user/' + username,
  			"type" : "DELETE",
        "success": function() {
          window.location.reload(true);
        }
  		});
    }
  }).modal('show');
};
