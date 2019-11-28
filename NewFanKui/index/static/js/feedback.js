//定义全局变量存储平台和分类信息
var fenlei = '足球';
var pingtai;
var curPage = 1; //当前页码 

var total, pageSize, totalPage; //总记录数，每页显示数，总页数
/*页面加载后默认点击第一个分类获得的列表*/
//同时获取当前用户可以查看的平台
$(function() {

	$.ajax({
		type: 'get',
		url: '/quanxian/',
		dataType: 'json',
		success: function(data) { /*渲染内容到页面*/
			var quanxian = ''

			for(var i = 0; i < data.length; i++) {
				for(var key in data[i]) {
					//console.log(data[i][key])
					if(data[i][key] != null) {
						quanxian += "<option value=" + data[i][key] + ">" + data[i][key] + '平台' + "</option>"
					}
				}
			}
			$('.com-opt').append(quanxian)
			$('.com-opt option:first').change();
			//加载完成后点击第一个分类
			$('.classify-box:first').click();
		}

	});
	$('.search_input').bind('keyup', function(event) {
		if(event.keyCode == "13") {
			$('.search_btn').click()
		}
	});
});

//			下拉框事件
$('.com-opt').change(function() {
	pingtai = $(this).val();
	console.log('发起平台请求')
	curPage = 1;
	getjiemu('/pingtaishuju/', pingtai, fenlei, curPage)

})

//每个类型点击后触发ajax方法
$('.classify-box').click(function() {
	console.log('发起分类请求')
	curPage = 1;
	$(this).css('backgroundColor', '#deecff');
	$(this).siblings().css('backgroundColor', ' ');
	fenlei = $(this).text();
	getjiemu('/pingtaishuju/', pingtai, fenlei, curPage);

});

//ajax封装
function getjiemu(url, pingtal, fenlei, page) {
	console.log('getjiemu触发了')
	var data = {
		"pingtai": pingtai,
		"fenlei": fenlei,
		"pageNum": page
	};
	console.log(data)
	$.ajax({
		type: 'get',
		url: url,
		data: data,
		dataType: 'json',
		beforeSend: function() {
			$('#qingkong').empty('')
			$('#qingkong').html('加载中...')
			//						console.log(data)
		},
		success: function(data) {

			$('#qingkong').empty(); //清空数据区 

			//total = data.total; //总记录数 

			//pageSize = data.pageSize; //每页显示条数 

			//curPage = page; //当前页 

			//totalPage = data.totalPage; //总页数 

			var item = ''
			for(var i = 0; i < data.length; i++) {
				var data1 = data[i].data;

				total = data[0].total;
				pageSize = data[0].size;
				curPage = data[0].pages
				totalPage = data[0].current
				var unixtime = data1.start_time;
				var unixTimestamp = new Date(unixtime * 1000);
				commonTime = unixTimestamp.toLocaleString('zh', {
					hour12: false
				});

				item += "<div><label><table class='table'  cellspacing='0'><tr><td rowspan='2'><input name='jiemu' class='jiemu' type='radio' value=" + data1.match_id + "></td><td>" + data1.match_name + "</td><td>" + commonTime + "</td><td>" + data1.team_a + "</td><td>" + data1.team_b + "</td></tr></table></label></div>";

			}
			$('#qingkong').append(item);
			//默认第一条选中
			$('#qingkong .jiemu:first').click();
			$('#check .radio:first').click();

		},
		//		complete: function() { //生成分页条 
		//
		//			getPageBar();　　　　　　　　　　　　　　　
		//			$("#pagecount span a").on('click', function() {　　
		//				console.log('分页被点了')　　　　
		//				var rel = $(this).attr("rel");　　　　　　
		//				if(rel) {　　　　
		//					getjiemu('/pingtaishuju/', pingtai, fenlei, rel);　　　　　　
		//				}　　　　　　　　
		//			});　　
		//		},
		complete: function() {
			getPageBar();
			$('#pagecount span a').on('click', function() {
				console.log('分页被点了');
				var rel = $(this).attr('rel');
				if(rel) {
					getjiemu('/pingtaishuju/', pingtai, fenlei, rel);
				}
			})
		},
		error: function() {

			$('#qingkong').html('加载失败,请稍后再试')

		}
	});
};

function getPageBar() {

	if(curPage > totalPage) curPage = totalPage;

	if(curPage < 1) curPage = 1;

	pageStr = "<span>共" + total + "条</span><span>" + curPage + "/" + totalPage + "</span>";

	if(curPage == 1) {

		pageStr += "<span>首页</span><span>上一页</span>";

	} else {

		pageStr += "<span><a href='javascript:void(0)' rel='1'>首页</a></span><span> <a href = 'javascript:void(0)'rel= '" + (curPage - 1) + "' > 上一页 </a></span> ";

	}

	if(curPage >= totalPage) {

		pageStr += "<span>下一页</span><span>尾页</span>";

	} else {

		pageStr += "<span><a href='javascript:void(0)' rel='" + (parseInt(curPage) + 1) + "'>下一页 </a></span><span> <a href = 'javascript:void(0)' rel= '" + totalPage + "' > 尾页 </a></span>";
	};
	$("#pagecount1").css('display', 'none')
	$("#pagecount").css('display', 'block');
	$("#pagecount").empty();
	$("#pagecount").html(pageStr);

};

//定义变量存储要提交的节目和问题;
var jiemu, problem;
$('form').on('click', '.jiemu', function() {
	jiemu = $(this).val()
	$(this).parent().parent().parent().parent().parent().parent().css('backgroundColor', '#deecff')
	$(this).parent().parent().parent().parent().parent().parent().siblings().css('backgroundColor', ' ')
})
$('form').on('click', '.radio', function() {
	problem = ($(this).val())
	$(this).parent().parent().parent().parent().css('backgroundColor', '#deecff')
	$(this).parent().parent().parent().parent().siblings().css('backgroundColor', '')
})

//提交按钮点击事件
$('#sub-btn').click(function() {
	//console.log(jiemu,problem)
	var data = {
		pingtai: pingtai,
		jiemu: jiemu,
		problem: problem
	}
	console.log(data)
	$.ajax({
		type: 'get',
		url: '/tijiaofankui/',
		data: data,
		dataType: 'json',
		success: function(data) {
			//			$('#success').slideDown();
			//			setTimeout(function() {
			//				$('#success').slideUp();
			//			}, 2000)
			if(data==1){
				$("#success").fadeIn().delay(1000).fadeOut();
			}


		}
	});
});