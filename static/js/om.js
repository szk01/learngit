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


    // 浏览器通知消息
    var notification = function (body) {
            console.log('浏览器通知消息!!!');
            const NotificationInstance = Notification || window.Notification;
            if (!!NotificationInstance) {
                const permissionNow = NotificationInstance.permission;
                if (permissionNow === 'granted') {              //允许通知
                    CreatNotification();
                } else if (permissionNow === 'denied') {
                    console.log('用户拒绝了你!!!');
                } else {
                    setPermission();
                }
                function setPermission() {
                    //请求获取通知权限
                    NotificationInstance.requestPermission(function (PERMISSION) {
                        if (PERMISSION === 'granted') {
                            CreatNotification();
                        } else {
                            console.log('用户无情残忍的拒绝了你!!!');
                        }
                    });
                }
                function CreatNotification() {
                    const n = new NotificationInstance('来电通知', {
                        body:  body
                    });

                    n.onshow = function () {
                        console.log('通知显示了！');
                    }
                    n.onclick = function (e) {
                        //可以直接通过实例的方式获取data内自定义的数据
                        //也可以通过访问回调参数e来获取data的数据
                        window.open(n.data.url, '_blank');
                        n.close();
                    }
                    n.onclose = function () {
                        console.log('你墙壁了我！！！');
                    }
                    n.onerror = function (err) {
                        console.log('出错了，小伙子在检查一下吧');
                        throw err;
                    }
                    //setTimeout(() => {
                    //    n.close();
                    //}, 10000);
                }
            }

        }



                                       // 使用相对路径
    // var url = '/'
    var url = 'wss://crm.dadaex.cn/socket.io/'
    console.log(url);
    var socket = io.connect(url);
    // 告诉服务器是谁登陆
    socket.on('connect', function() {
        socket.emit('login', '登录');
    });                                                          // 这些都是套路函数，建立通道，发送提示消息

    socket.on("test_room", function(data) {
        console.log(data)
    });

    // 服务器通知有来电
    socket.on("ring", function(data) {                         // 有电话拨打进来，显示来电号码
        console.log('有来电...')
        var body = '有客户来电'+data["number"]
        notification(body)
        $('.class-note').show()

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
