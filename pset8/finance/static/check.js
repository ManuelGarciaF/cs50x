$('#submit').click(function (e) { 
    e.preventDefault();
    u_name = $('#username').val();
    $.getJSON("/check", {username: u_name}, function (data) {
        if (data) {
            $('#name_alert').css('display', 'block');
        } else {
            $('#submit').parent().submit();
        }
        console.log(data + ' ' + u_name);
    });
    
});