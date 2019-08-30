    function show(count) {                                  // 格式化显示时间
        var timeshow = "00:00";
        if (count < 60 ) {
            if (count < 10) {                              /*小数取整*/
                timeshow = '00'+':'+'0'+count.toString()
            }
            else {
                timeshow = '00:'+count.toString()
            }
        }
        if (count > 60 || count === 60) {
            var min = count / 60
            var sec = count % 60
            if (sec < 10) {
                min = Math.floor(min)                        /*小数取整*/
                timeshow = min.toString()+':'+'0'+sec.toString()
            }
            else {
                min = Math.floor(min)                        /*小数取整*/
                timeshow = min.toString()+':'+sec.toString()
            }

        }
        $('.time').text(timeshow);
        return timeshow
    }

    function timing(status) {
        var interval = null;
        window.count = 0;
        if (status == 'start') {
            console.log('开始计时')
            interval = setInterval(function() {
                count = count + 1
                console.log(count);
                show(count);
            }, 1000)
        }
        var d = {"i":interval, "count":count}              /* 返回多个值*/
        return d
    }

    function template(number, alltme, recordUrl, audioUrl) {
        var t = `
        <ul class="phone-note">
            <li class="cdr">通话记录</li>
            <li class="number"><em>${number}</em></li>
            <li class="all-time">${alltme}</li>
            <li ><a href="${recordUrl}" class="record">录音</a></li>
            <li ><a href="${audioUrl}" class="play">播放</a></li>
        </ul>
        `
        return t
    }
//  var url = "http://106.15.44.224:80"
    var url = "http://127.0.0.1:80"
    console.log(url);
    var socket = io.connect(url);
    socket.on('connect', function() {
        var id = $('.id').text()
        socket.emit('login', {data: id});
    });                                                          // 这些都是套路函数，建立通道，发送提示消息

    socket.on("test_room", function(data) {
        console.log(data)
    });

    socket.on("ring", function(data) {                         // 有电话拨打进来，显示来电号码
        <!--alert(data+'来电');-->
        $('.call-note-container').show();
        $('.call-number').text('来电'+data["number"])
        $('.status').text('呼叫中')
        console.log('有来电')

    });

    socket.on("anwser", function(data) {                          // 分机应答，显示状态
            $('.status').text('通话已建立')
            <!--计时器-->
            var d = timing('start');
            window.inter = d["i"]                                   // 将inter声明为全局变量
            console.log('开始计时')
    });

    socket.on("record", function(data) {                             // 分机或者来访者挂断
        if (data["status"] === 'Cdr') {
            $('.status').text('通话已结束');
            $('.call-note-container').hide()                           // 停止计时
            clearInterval(inter)
            var s = show(count)
            console.log(s)
            var r = template(data["number"], s, data["downPath"], data["play_path"])
            $("#call-record-container").append(r)
            console.log('点击停止计时按钮')
        }
    });

    // 点击关闭显示框
   $(".bt-startTime").click(function(){                // 点击按钮开始计时
    var d  = timing('start');                 // 将inter声明为全局变量
    window.inter = d["i"]
    console.log('点击开始计时')
    });

    $(".bt-stopTime").click(function(){                // 点击按钮停止计时
        clearInterval(inter)
        var s = show(count)
        console.log(s)
        var r = template(17730273676, s, 3, 4)
        $("#call-record-container").append(r)
        console.log('点击停止计时按钮')
    })
