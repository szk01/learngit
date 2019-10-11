// 功能函数
var log = console.log.bind(console)
	//重新加载所有的客户
    function load_clients(){
    	$('.clients td').remove()			// 清空以前的ajax请求，以免重复显示
    	$.ajax({
    		type:"post",
    		url:"/load_clients",
    		success: function(result){
    			console.log('接收数据成功...')
    			console.log('接受到的数据', result)
    			var data = JSON.parse(result)           // 解析得到的字符串为json对象
    			for(var i=0; i < data.length; i++){
	      			var infos = $('<tr>' +
			      					'<td class="td-cid">'+data[i].id+'</td>'+
			      					'<td>'+data[i].name+'</td>'+
			      					'<td>'+data[i].phone+'</td>'+
			      					'<td>'+data[i].company+'</td>'+
			      					'<td>'+data[i].wechat+'</td>'+
			      					'<td>'+data[i].qq+'</td>'+
			      					'<td>'+data[i].email+'</td>'+
			      					'<td><button class="edit btn btn-info">修改</button></td>'+
								'/tr>')

      				$('table.client').append(infos)
				}
    		}
        	//console.log('是否执行了...')
    	})
    }

    //表格中的数据，生成多个联系方式input模板
    function template_input(name, info){
    var t = `
    <div class="new_ipt">
        <label for="inputPassword3" class="col-sm-2 control-label">${name}</label>
        <div class="input-group col-sm-8">
            <input type="email" class="form-control ipt-${name}" id="inputPassword3" value="${info}" placeholder="">
        </div>
    </div>
    `
    return t
}

	// 有多个信息, 那么就新建多个input标签
	function spilt_infos(str, className){
		var infos = str.split(',')
		if(infos.length > 1){
			$('.ipt-'+className)[0].value = infos[0]					//将第一个信息加到原本的input中
			for (var i = 0; i < infos.length-1; i++){					//将第二个+信息加到新生成的input中
				var ipt = template_input(className, infos[i+1])
				$('.form-'+className).append(ipt)
			}
			return false
		}else if(infos.length === 1){
			return true
		}
	}

	// 恢复编辑弹窗原样
	function reset_edit(){
		log('编辑框的取消按钮')
		$('.new_ipt').remove()						// 去除动态生成的input
		var ipts = $('.form-container input.form-control')				// 清空数据
		for(var i = 0; i < ipts.length; i++){
			ipts[i].value = ""
		}
	}

	// 重置增加客户弹窗编辑框
	function reset_add_edit(){
		var add_ipts = $('.form-add-container input.form-control')
		for(var i = 0; i < add_ipts.length; i++){
			add_ipts[i].value = ""
		}
	}


// 增加客户
	// 点击增加客户按钮btn 显示编辑弹窗
	$('.bt-add-client').click(function () {
		$('.form-add-container').show()
		$('.mask').show()
        reset_add_edit()
	})

	/*点击增加客户的确认按钮，显示编辑弹窗，拿到编辑弹窗中的信息，发送ajax请求，增加一条客户记录，重新加载所有客户*/
	$('.btn-add-confirm').click(function () {
		// var cid = $('.in-ad-cid').val()							// 序列号
		var name = $('.ipt-add-name').val()						// 姓名
		var phone = $('.ipt-add-phone').val()						// 手机号
		var gs = $('.ipt-add-gs').val()							// 公司
		var wechat = $('.ipt-add-wechat').val()					// 微信
		var qq = $('.ipt-add-qq').val()							// qq
		var email = $('.ipt-add-email').val()						// email
		//console.log('确认增加按钮获取的消息', cid, name, phone, gs, wechat, qq, email)
		var add_data = {}
		// add_data.cid = cid
		add_data.name = name
		add_data.phone = phone
		add_data.gs = gs
		add_data.wechat = wechat
		add_data.qq = qq
		add_data.email = email
		 // $.ajax({
      	// 	type:"post",
      	// 	url:"/add_client",
      	// 	data: add_data,
      	// 	success: function(r){
      	// 		console.log('成功增加新客户...', r)
			// 	load_clients()				// 重新加载所有的客户
      	// 	}
      	// });
		log('编辑框中的信息', add_data)
		reset_add_edit()						//
		$('.form-add-container').hide()			// 隐藏增加客户编辑弹窗
		$('.mask').hide()

	})

	/*点击增加客户编辑框的取消功能*/
	$('.btn-add-cancel').click(function () {
		$('.form-add-container').hide()
		$('.mask').hide()
        reset_add_edit()
	})


// 搜索功能

// 动态生成新的输入框
function template(name){
    var t = `
    <div class="new_ipt">
        <label for="inputPassword3" class="col-sm-2 control-label">${name}</label>
        <div class="input-group col-sm-8">
            <input type="email" class="form-control ipt-${name}" id="inputPassword3" placeholder="">
        </div>
    </div>
    `
    return t
}

// 显示整个编辑框
$('.add_new').click(function(){
    log('点击')
    $('.form-container').slideDown(500)
})

// 给span元素加上点击事件，加上新的input输入框
$('span.input-group-addon').click(function(){
    var className = $(this).siblings()[0].classList[1]
    var str_len = className.length
    var name  = className.slice(4, str_len)
    //var name = $(this).parent().siblings().eq(1)[0]
    log('字段名称', name)
    var ipt = template(name)
    $(this).parent().parent().append(ipt)
})

//编辑按钮，弹出编辑框
$('.client').on('click', '.edit', function () {
    log('点击编辑')
})

//取消按钮，还原输入框
$('.cancel').click(function(){
    console.log('点击取消按钮')
    $('.new_ipt').remove()
})

