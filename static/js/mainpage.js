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

//팔로우 post 함수
function follow(follower_id){
    let follower = follower_id
    $.ajax({
        type: "POST",
        url: "/api/follow",
        traditional: true,
        data: {follower_give: follower},
        success: function (response) {
            if (response['result'] == 'success') {
                window.location.href = '/'
            }
        }
    })
}

function feedup() {
    let picture =[]
    if($('#feed_picture_1').val()!=''){
        picture.push($('#feed_picture_1').val())
    }
    if($('#feed_picture_2').val()!=''){
        picture.push($('#feed_picture_2').val())
    }
    if($('#feed_picture_3').val()!=''){
        picture.push($('#feed_picture_3').val())
    }
    if($('#feed_picture_4').val()!=''){
        picture.push($('#feed_picture_4').val())
    }
    if($('#feed_picture_5').val()!=''){
        picture.push($('#feed_picture_5').val())
    }
    let contents = $('#feed_contents').val()
    $.ajax({
        type: "POST",
        url: "/api/feedup",
        traditional: true,
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

function post_modal(id) {

    var zIndex
    if (id == "option_modal") {
        zIndex = 9999;
    } else {
        zIndex = 9000;
    }

    var modal = document.getElementById(id);

    var bg = document.createElement('div');
    bg.setStyle({
        position: 'fixed',
        zIndex: zIndex,
        left: '0px',
        top: '0px',
        width: '100%',
        height: '100%',
        overflow: 'auto',
        backgroundColor: 'rgba(0,0,0,0.4)'
    });
    document.body.append(bg);

    $.ajax({
        type: "POST",
        url: "/api/modal",
        data: {feedID_give: id},
        success: function (response) {
            if (response['result'] == 'success') {
                alert('1111.')
            }
        }
    })

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

        zIndex: zIndex + 1,

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

    var bg = document.createElement('div');
    bg.setStyle({
        position: 'fixed',
        zIndex: zIndex,
        left: '0px',
        top: '0px',
        width: '100%',
        height: '100%',
        overflow: 'auto',
        backgroundColor: 'rgba(0,0,0,0.4)'
    });
    document.body.append(bg);

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

        zIndex: zIndex + 1,

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

    var bg = document.createElement('div');
    bg.setStyle({
        position: 'fixed',
        zIndex: zIndex,
        left: '0px',
        top: '0px',
        width: '100%',
        height: '100%',
        overflow: 'auto',
        backgroundColor: 'rgba(0,0,0,0.4)'
    });
    document.body.append(bg);

    document.getElementById('feed_close_btn').addEventListener('click', function () {
        bg.remove();
        modal.style.display = 'none';
    });

    modal.setStyle({
        position: 'fixed',
        display: 'block',
        boxShadow: '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',

        zIndex: zIndex + 1,

        top: '30%',
        left: '80%',
        transform: 'translate(-50%, -50%)',
        msTransform: 'translate(-50%, -50%)',
        webkitTransform: 'translate(-50%, -50%)'
    });

}

Element.prototype.setStyle = function (styles) {
    for (var k in styles) this.style[k] = styles[k];
    return this;
};

