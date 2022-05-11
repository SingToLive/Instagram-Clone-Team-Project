function loginbtn() {
    const input_id = document.getElementById('user_email').value;
    const input_pw = document.getElementById('user_pw').value;


    $.ajax({
        type: "POST",
        url: "/signin",
        data: {user_id : input_id, user_password : input_pw},
        async:true,
        success: function(response) {
            if (response['result'] == 'fail') {
                        alert(response['msg'])
                        window.location.href = '/'
                    } else {
                alert(response['msg'])
                $.cookie('mytoken', response['token'], {path: '/'});
                window.location.replace("/")
                // window.location.href = '/MainPage'
            }
        }
    })
}

function joinbtn() {
    window.location.href = "/SignUpPage"
}
