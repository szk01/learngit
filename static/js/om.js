/*用来显示弹窗的js代码*/
    // 将时间格式化显示
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

    // 计时器计时出时间
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

    // 生成通话记录模板
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

    // 生成来电弹窗模板
    function add_note() {
        console.log('加上来电通知...')
        var note = `
            <div class="call-note-container" style="position:fixed; width:500px; height:250px; top:300px; left: 500px; background-color: antiquewhite ">
                <button class="close">关闭</button>
                <div class="call-number" style="font-size: 20px; text-align:center; margin: 30px 30px; color:red;">来电号码</div>
                <div class="time" style="font-size: 20px; text-align:center; margin: 30px 30px;">通话时间</div>
                <div class="status" style="font-size: 20px; text-align:center; margin: 30px 30px;">状态</div>
		    </div>
        `
        return note
    }

    // 获取到cookie
    function getCookie(cname) {
        var name = cname + "=";
        var ca = document.cookie.split(';');
        for(var i=0; i<ca.length; i++) {
            var c = ca[i].trim();
            if (c.indexOf(name)===0) return c.substring(name.length,c.length);
        }
      return "";
    }

//  var url = "http://106.15.44.224:80"
    var url = "/"                                   // 使用相对路径
    console.log(url);
    var socket = io.connect(url);
    // 告诉服务器是谁登陆
    socket.on('connect', function() {
        var cookie = getCookie('session')
        console.log('js获取的cookie是', cookie)   // 找到工号，判断相应的分机号
        // if (cookie === '10087') {
        //     console.log('true or false', cookie === '10087')
        //     var userid = '213'                  // 本地开发
        //     // var userid = '221'               // 给上海使用
        // }else if (cookie === '10088') {
        //     var userid = '214'                   //本地开发
        //     // var userid = '222'                      //给上海使用
        // }
        console.log('发送给应用服务器的id是', cookie)
        socket.emit('login', cookie);
    });                                                          // 这些都是套路函数，建立通道，发送提示消息

    socket.on("test_room", function(data) {
        console.log(data)
    });

    // 服务器通知有来电
    socket.on("ring", function(data) {                         // 有电话拨打进来，显示来电号码
        var t = add_note()                                              // 加上新版弹窗
        console.log('有来电...')
        $('.class-note').append(t)

        $('.call-number').text('来电号码'+data["number"])
        $('.status').text('呼叫中')

    });

    // 服务器通知分机已接电话
    socket.on("anwser", function(data) {                          // 分机应答，显示状态
            $('.status').text('通话已建立')

            var d = timing('start');                                 //开始计时
            window.inter = d["i"]                                   // 将inter声明为全局变量
            console.log('开始计时')
    });

    // 服务器通知通话挂断,清除弹窗计时数
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


    // 来电弹窗上的满意度调查按钮                使用jquery的事件委托的方式，委托给父节点
    $('.class-note').on('click', '.satisfy', function () {
        console.log('点击满意度调查按钮...')
        socket.emit('satisfy', {'data': 'satisfy'})
    })



    // 来电弹窗上的关闭按钮，清除计时
    $(document.body).on('click', '.close', function () {                    // 没有起作用
        console.log('点击来电弹窗的关闭按钮')
        $('.call-note-container').hide()                           // 隐藏弹窗
        clearInterval(window.inter)
        window.count = 0
    })

    // 首页测试的满意度调查按钮
    $('.satisfy').click(function() {                //按钮点击
        console.log('点击满意度调查按钮')
        socket.emit('satisfy', {'data': 'satisfy'})     // 只传递数据，不需要返回的数据。使用websocket协议
    })