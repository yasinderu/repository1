$(document).ready(function() {
  var panelOne = $('.form-panel.two').scrollHeight;
  var panelTwo = $('.form-panel.two').scrollHeight;

  $('.form-panel.two').not('.form-panel.two.active').on('click', function(e) {
    e.preventDefault();

    $('.form-toggle').addClass('visible');
    $('.form-panel.one').addClass('hidden');
    $('.form-panel.two').addClass('active');
    $('.form').animate({
      'height': panelTwo
    }, 200);
  });

  $('.form-toggle').on('click', function(e) {
    e.preventDefault();
    $(this).removeClass('visible');
    $('.form-panel.one').removeClass('hidden');
    $('.form-panel.two').removeClass('active');
    $('.form').animate({
      'height': panelOne
    }, 200);
  });

  function setRemovebtn(){
    $('.remove-btn').click(function () {
      var destinations = $('.destinations > div');
      if (destinations.length > 1) {
        $(this).parents('.destination-list').remove();
      }
    });
  }
  setRemovebtn();
  var input_destination = $('.destinations > div').first();
  // var input_destination_box = input_destination.find('.select-destination');

  $('#add-destination').click(function(){
    // input_destination_box.remove();
    var new_destination = input_destination.clone(true);
    // var inputEl = new_destination.find('.select-destination')
    $('.destinations').append(new_destination);
    setRemovebtn();
  });
});