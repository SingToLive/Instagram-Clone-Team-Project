function loginbtn() {
    const input_id = document.getElementById('user_email').value;
    console.log(JSON.stringify(input_id))
    const input_pw = document.getElementById('user_pw').value;
    console.log(JSON.stringify(input_pw))


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
                console.log(response)
                console.log(response['token'])
                console.log($.cookie('mytoken', response['token'], {path: '/'}))
                $.cookie('mytoken', response['token'], {path: '/'});
                console.log('hah')
                window.location.replace("/")
                // window.location.href = '/MainPage'
            }
        }
    })
}

function joinbtn() {
    window.location.href = "/SignUpPage"
}
