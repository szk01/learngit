/*用来显示弹窗的js代码*/
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
        window.count = 0;                                       // 计数也是全局变量
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

    function add_note() {
        console.log('加上来电通知...')
        var note = `
            <div class="call-note-container" style="position:fixed; width:500px; height:250px; top:300px; left: 500px; background-color: antiquewhite ">
                <button class="close">关闭</button>
                <div class="call-number" style="font-size: 20px; text-align:center; margin: 30px 30px; color:red;">来电号码</div>
                <div class="time" style="font-size: 20px; text-align:center; margin: 30px 30px;">通话时间</div>
                <div class="status" style="font-size: 20px; text-align:center; margin: 30px 30px;">状态</div>
                <button class="satisfy" style="font-size: 20px; text-align:center; margin: 30px 30px;">满意度调查按钮</button>
		    </div>
        `
        return note
    }

//  var url = "http://106.15.44.224:80"
    var url = "/"                                   // 使用相对路径
    console.log(url);
    var socket = io.connect(url);
    socket.on('connect', function() {
        var rid = $('#mini').attr('class')          // 找到工号，判断相应的分机号
        if (rid == '10087') {
            // var userid = '212'
            var userid = '221'
        }
        if (rid == '10088') {
            // var userid = '213'                   //本地开发
            var userid = '222'                      //给上海使用
        }
        console.log('发送给应用服务器的id',userid)
        socket.emit('login', userid);
    });                                                          // 这些都是套路函数，建立通道，发送提示消息

    socket.on("test_room", function(data) {
        console.log(data)
    });

    socket.on("ring", function(data) {                         // 有电话拨打进来，显示来电号码
        var t = add_note()                                              // 加上新版弹窗
        console.log('有来电...')
        $(document.body).append(t)

        $('.call-number').text('来电号码'+data["number"])
        $('.status').text('呼叫中')

    });

    socket.on("anwser", function(data) {                          // 分机应答，显示状态
            $('.status').text('通话已建立')
            <!--计时器-->
            var d = timing('start');                                 //开始计时
            window.inter = d["i"]                                   // 将inter声明为全局变量
            console.log('开始计时')
    });

    socket.on("off", function(data) {                             // 分机或者来访者挂断
        console.log('结束通话...')
        if (data["status"] === 'Cdr') {
            $('.status').text('通话已结束');
            $('.call-note-container').hide()                           // 隐藏弹窗
            clearInterval(window.inter)
            window.count = 0                                            //计数清零
            var s = show(count)
            console.log(s)
//          var r = template(data["number"], s, data["downPath"], data["play_path"])
//          $("#call-record-container").append(r)
        }
    });


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

    $('.close').click(function(){                   // 点击关闭按钮的时候，隐藏弹窗
        $('.call-note-container').hide()
    })

    $('.satisfy').click(function() {                //按钮点击
        console.log('点击满意度调查按钮')
        socket.emit('satisfy', {'data': 'satisfy'})     // 只传递数据，不需要返回的数据。使用websocket协议
    })