$(document).ready(function() {

  $("#testpost").on('click', function() {
    console.log("testing post");

    $.ajax({
      type: "POST",
      url: "/twitter",
      contentType: "application/json",
      data: JSON.stringify({'data':'sdlfj'}),
      dataType:'json',
      success: function (response) {
        console.log('response', response);
      },
      error: function (err) {
        console.log('error', err);
      }
    });
  });
});
