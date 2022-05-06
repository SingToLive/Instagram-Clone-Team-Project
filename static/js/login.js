function loginbtn() {
    const input_id = document.getElementById('user_email').value;
    console.log(JSON.stringify(input_id))
    const input_pw = document.getElementById('user_pw').value;
    console.log(JSON.stringify(input_pw))

    $.ajax({
        type: "POST",
        url: "/login",
        data: {user_id : input_id, user_password : input_pw},
        async:true,
        success: function(response) {
            if (response['result'] == 'fail') {
                        alert(response['msg'])
                        window.location.href = '/'
                    } else {
                alert(response['msg'])
                window.location.href = '/MainPage'
            }
        }
    })
}

function joinbtn() {
    window.location.href = "/SignInPage"
}
