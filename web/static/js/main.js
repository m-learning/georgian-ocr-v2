$(document).ready(function() {
    $("#get_file").on('click', function() {
        $("#my_file").trigger('click');
    });
    $("#my_file").change(function() {
        $("#read").submit();
        $("#read").append('<div class="loader"></div>');
        $("#read").append('<p class="loader-text" style="color:red;font-size:small;">მიმდინარეობს წაკითხვა და pdf ფაილად გარდაქმნა</p>');
    });
    $(window).blur(function() {
        if ($('.loader').length) {
            $('.loader').remove();
            $('.loader-text').remove();
        }
    })
});
