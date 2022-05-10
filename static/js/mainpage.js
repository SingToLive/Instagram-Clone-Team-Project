// Element 에 style 한번에 오브젝트로 설정하는 함수 추가
    Element.prototype.setStyle = function (styles) {
        for (var k in styles) this.style[k] = styles[k];
        return this;
    };

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

function post_modal(id, feed_id) {

    let feed = feed_id
    console.log(feed)
    $.ajax({
        type: "POST",
        url: "/api/modal",
        data: {feedID_give: feed},

    })


    var zIndex
    if (id == "option_modal") {
        zIndex = 9999;
    } else {
        zIndex = 9000;
    }

    var modal = document.getElementById(id);

    // 모달 div 뒤에 희끄무레한 레이어
    var bg = document.createElement('div');
    bg.setStyle({
        position: 'fixed',
        zIndex: zIndex,
        left: '0px',
        top: '0px',
        width: '100%',
        height: '100%',
        overflow: 'auto',
        // 레이어 색갈은 여기서 바꾸면 됨
        backgroundColor: 'rgba(0,0,0,0.4)'
    });
    document.body.append(bg);

    // 닫기 버튼 처리, 시꺼먼 레이어와 모달 div 지우기
    close_modal_event = document.getElementsByClassName('modal_close_btn');
    for (var i = 0; i < close_modal_event.length; i++) {
        close_modal_event[i].addEventListener('click', function () {
            bg.remove();
            modal.style.display = 'none';
        });
    }

    modal.setStyle({
        position: 'fixed',
        display: 'block',
        boxShadow: '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',

        // 시꺼먼 레이어 보다 한칸 위에 보이기
        zIndex: zIndex + 1,

        // div center 정렬
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        msTransform: 'translate(-50%, -50%)',
        webkitTransform: 'translate(-50%, -50%)'
    });
}


function modal(id) {
    var zIndex
    if (id == "option_modal") {
        zIndex = 9999;
    } else {
        zIndex = 9000;
    }

    var modal = document.getElementById(id);

    // 모달 div 뒤에 희끄무레한 레이어
    var bg = document.createElement('div');
    bg.setStyle({
        position: 'fixed',
        zIndex: zIndex,
        left: '0px',
        top: '0px',
        width: '100%',
        height: '100%',
        overflow: 'auto',
        // 레이어 색갈은 여기서 바꾸면 됨
        backgroundColor: 'rgba(0,0,0,0.4)'
    });
    document.body.append(bg);

    // 닫기 버튼 처리, 시꺼먼 레이어와 모달 div 지우기
    close_modal_event = document.getElementsByClassName('modal_close_btn');
    for (var i = 0; i < close_modal_event.length; i++) {
        close_modal_event[i].addEventListener('click', function () {
            bg.remove();
            modal.style.display = 'none';
        });
    }

    modal.setStyle({
        position: 'fixed',
        display: 'block',
        boxShadow: '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',

        // 시꺼먼 레이어 보다 한칸 위에 보이기
        zIndex: zIndex + 1,

        // div center 정렬
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        msTransform: 'translate(-50%, -50%)',
        webkitTransform: 'translate(-50%, -50%)'
    });
}

function feed__modal(id) {
    var zIndex = 9999;
    var modal = document.getElementById(id);

    // 모달 div 뒤에 희끄무레한 레이어
    var bg = document.createElement('div');
    bg.setStyle({
        position: 'fixed',
        zIndex: zIndex,
        left: '0px',
        top: '0px',
        width: '100%',
        height: '100%',
        overflow: 'auto',
        // 레이어 색갈은 여기서 바꾸면 됨
        backgroundColor: 'rgba(0,0,0,0.4)'
    });
    document.body.append(bg);

    // 닫기 버튼 처리, 시꺼먼 레이어와 모달 div 지우기
    document.getElementById('feed_close_btn').addEventListener('click', function () {
        bg.remove();
        modal.style.display = 'none';
    });


    modal.setStyle({
        position: 'fixed',
        display: 'block',
        boxShadow: '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',

        // 시꺼먼 레이어 보다 한칸 위에 보이기
        zIndex: zIndex + 1,

        // div center 정렬
        top: '30%',
        left: '80%',
        transform: 'translate(-50%, -50%)',
        msTransform: 'translate(-50%, -50%)',
        webkitTransform: 'translate(-50%, -50%)'
    });

}

