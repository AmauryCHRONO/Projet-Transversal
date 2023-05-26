$(document).ready(function() {
  $(document).keydown(function(event) {
    if (event.key === "z" || event.key === "Z") {
      $.ajax({
        url: '/light_up',
        type: 'POST',
        data: { key: event.key },
        success: function(response) {
          if (response === 'success') {
            $('#square1').css('background-color', 'darkblue');
          }
        }
      });
    }
    else if (event.key === "q" || event.key === "Q") {
      $.ajax({
        url: '/light_up',
        type: 'POST',
        data: { key: event.key },
        success: function(response) {
          if (response === 'success') {
            $('#square2').css('background-color', 'darkblue');
          }
        }
      });
    }
    else if (event.key === "s" || event.key === "S") {
      $.ajax({
        url: '/light_up',
        type: 'POST',
        data: { key: event.key },
        success: function(response) {
          if (response === 'success') {
            $('#square3').css('background-color', 'darkblue');
          }
        }
      });
    }
    else if (event.key === "d" || event.key === "D") {
      $.ajax({
        url: '/light_up',
        type: 'POST',
        data: { key: event.key },
        success: function(response) {
          if (response === 'success') {
            $('#square4').css('background-color', 'darkblue');
          }
        }
      });
    }
    else if (event.key === " " || event.key === "Space") {
      $.ajax({
        url: '/light_up',
        type: 'POST',
        data: { key: event.key },
        success: function(response) {
          if (response === 'success') {
            $('#spacebar').css('background-color', 'red');
          }
        }
      });
    }
  });

  $(document).keyup(function(event) {
    if (event.key === "z" || event.key === "Z") {
      $('#square1').css('background-color', '#25aae1');
    }
  });
  $(document).keyup(function(event) {
    if (event.key === "q" || event.key === "Q") {
      $('#square2').css('background-color', '#25aae1');
    }
  });
  $(document).keyup(function(event) {
    if (event.key === "s" || event.key === "S") {
      $('#square3').css('background-color', '#25aae1');
    }
  });
  $(document).keyup(function(event) {
    if (event.key === "d" || event.key === "D") {
      $('#square4').css('background-color', '#25aae1');
    }
  });
  $(document).keyup(function(event) {
    if (event.key === " " || event.key === "Space") {
      $('#spacebar').css('background-color', '#25aae1');
    }
  });
});