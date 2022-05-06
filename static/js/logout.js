// function logoutbtn() {
//     console.log('input_id')
//     $.ajax({
//         type: "GET",
//         url: "/logout",
//         data: {},
//         async:true,
//         success: function(response) {
//             alert(response['msg'])
//             window.location.href = '/'
//         }
//     })
// }

function logoutbtn() {
    alert('로그아웃 되었습니다!');
    $.removeCookie('mytoken', {path: '/'});
    window.location.href = '/';
}

