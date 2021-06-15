$(document).ready(function () {
    $('.form-login').on('submit', function (event) {
        $.ajax({
            data: {
                emailId: $('#emailId').val(),
                passwd: $('#passwd').val()
            },

            type: 'POST',
            url: '/login',
            headers: {
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                Pragma: 'no-cache',
                Expires: '0'
            },
            success: function () {},
            error: function () {
                alert('ajax error');
            }
        }).done(function (data) {
            if (data.response == 1) {
                window.location.href = '/upload';
            } else if (data.response == 0) {
                $('#message-login').text('Invalid email or password!').css({'color':'red'});
                alert('Invalid email or password!');
            }
        });
        event.preventDefault();
    });
});

// create account page script

$(document).ready(function () {
    $('.form-createaccount').on('submit', function (event) {
        $.ajax({
            data: {
                createEmailId: $('#createEmailId').val(),
                userName: $('#userName').val(),
                createPasswd: $('#createPasswd').val(),
                phoneNumber: $('#phoneNumber').val()
            },
            type: 'POST',
            url: '/updatedetails',
            headers: {
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                Pragma: 'no-cache',
                Expires: '0'
            },
            success: function () {},
            error: function () {
                alert('ajax error');
            }
        }).done(function (data) {
            if (data.response == 2) {
                window.location.href = '/';
            } else if (data.response == 0) {
                $('#message-create').text(
                    'Email ID already exist! Try with different email').css({'color':'red'});
            }
             else if (data.response == 1) {
                $('#message-create').text(
                    'username already exist! Try with different username').css({'color':'red'});
            }
        });

        event.preventDefault();
    });
});
