function submitLogin() {
    var data = {
        username: $('#username')[0].value,
        password: $('#password')[0].value
    }

    $.ajax({
        type: 'post',
        url: '/api/login',
        data: JSON.stringify(data),
        contentType: 'application/json',
        complete: function(ret) {
            localStorage.setItem("token", ret.responseJSON.token)
            window.location.href = "/bills"
        }
    })
}

$(document).ready(function () {
    $("#submit").click(submitLogin)
})
