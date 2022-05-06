function logoutbtn() {
    console.log('input_id')
    $.ajax({
        type: "GET",
        url: "/logout",
        data: {},
        async:true,
        success: function(response) {
            alert(response['msg'])
            window.location.href = '/'
        }
    })
}
