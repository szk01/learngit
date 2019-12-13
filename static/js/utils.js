
var ajax = function (url, type, data, callback) {
    $.ajax({
        type: type,
        url: url,
        data: data,
        success: callback,
    });
}

var log = console.log.bind(console)

var ajax_with_session = function (url, type, data, callback) {
    $.ajax({
        url: url,
        type: type,
        data: data,
        xhrFields: { withCredentials: true },
        success: callback,
    })
}

// 请求后台得到用户信息，写入localStorage
var get_userInfo = function () {
    $.ajax({
        url: '/user/token',
        type: 'post',
        data : {},
        xhrFields: { withCredentials: true },
        success: function (r) {
            log("success", r, typeof r)
            // 将其写入token中
            for (var k in r) {
                log('k, t', k , r[k])
                sessionStorage.setItem(k, r[k])
            }
            // log(sessionStorage.getItem("user_name"))
            set_info()
        },
    })
}

// 拿到localStorage中的数据
var set_info = function () {
    $("#name").text(sessionStorage.getItem("user_name"))
    $("#role").text(sessionStorage.getItem("user_role"))
    $("#seat span").text(sessionStorage.getItem("seat_number"))
    log("设置token")
}

get_userInfo()
