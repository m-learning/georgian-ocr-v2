$(document).ready(function() {
    $("#get_file").on('click', function() {
        $("#my_file").trigger('click');
    });
    $("#my_file").change(function() {
        if($('.loader-error').length) $('.loader-error').remove()
        var form_data = new FormData($('#read')[0]);
        $.ajax({
            type: 'POST',
            url: '/read',
            processData: false,
            contentType: false,
            cache: false,
            data: form_data,
            timeout: 300000,
            success: function(response) {
                downloadFromUrl(response)
                $('.loader').remove();
                $('.loader-text').remove();
            },
            error: function() {
                $('.loader').remove();
                $('.loader-text').remove();
                $("#read").append('<p class="loader-error" style="color:red;font-size:small;">ფაილის დამუშავებისას მოხდა შეცდომა.</p>');
            }
        });
        $("#read").append('<div class="loader"></div>');
        $("#read").append('<p class="loader-text" style="color:red;font-size:small;">მიმდინარეობს წაკითხვა და pdf ფაილად გარდაქმნა</p>');
    });
});

function downloadFromUrl(url) {
    var a = document.createElement("a");
    document.body.appendChild(a);
    a.style = "display: none";
    a.href = url;
    a.download = url.split('/')[3];
    a.click();
    document.body.removeChild(a);
}
