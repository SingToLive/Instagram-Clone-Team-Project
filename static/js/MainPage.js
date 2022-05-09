$(document).ready(function () {
});

function feedup() {
    let picture = $('#feed_picture').val()
    let contents = $('#feed_contents').val()



    $.ajax({
        type: "POST",
        url: "/api/feedup",
        data: {picture_give: picture, contents_give: contents},
        success: function (response) {
            if (response['result'] == 'success') {
                alert('게시물이 업로드 되었습니다.')
                window.location.href = '/'
            }
        }
    })
}