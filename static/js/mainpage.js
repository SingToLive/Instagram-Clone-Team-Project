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

function commentup(id, time) {
    let contents = document.getElementById(time).value
    console.log(contents)

    let feed_id = id



    $.ajax({
        type: "POST",
        url: "/api/commentup",
        data: {contents_give: contents, feedID_give: feed_id},
        success: function (response) {
            if (response['result'] == 'success') {
                alert('댓글이 등록되었습니다.')
                window.location.href = '/'
            }
        }
    })
}