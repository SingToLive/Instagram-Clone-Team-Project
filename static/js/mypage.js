//MyPage 이동 함수
function  GoToIndividualPage(id){
    let user_id = id;
    $.ajax({
        type: "POST",
        url: "/page",
        data: {IndiviualID_give: user_id},
        success: function (response) {
             $.cookie('Indivtoken', response['token'], {path: '/'});
             window.location.href = '/MyPage'
        }
    })


}