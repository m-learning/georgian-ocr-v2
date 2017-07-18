$(document).ready(function(){
  $("#get_file").on('click', function(){
    $("#my_file").trigger('click');
  });
  $("#my_file").change(function(){
    $("#read").submit();
  });
});
