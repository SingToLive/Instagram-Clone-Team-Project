function logoutbtn() {
    alert('로그아웃 되었습니다!');
    $.removeCookie('mytoken', {path: '/'});
    window.location.href = '/';
}

