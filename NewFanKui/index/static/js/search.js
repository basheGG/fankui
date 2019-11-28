//存储搜索关键字
var keyword;
var curPage1 = 1; //当前页码 

var total1, pageSize1, totalPage1; //总记录数，每页显示数，总页数
/*放大镜点击后，搜索框获得焦点*/
$('.search_sousuo').click(function() {
	$('.search_input').focus();
});

//搜索按钮点击后判断是否为空
$('.search_btn').click(function() {
	if($('.search_input').val() == '') {
		alert('请输入内容')
	} else {
		keyword = $('.search_input').val();
		curPage1 = 1;
		console.log('发起搜索请求')
		search('/sousuo/', pingtai, keyword, curPage1)

	};
})

function search(url, pingtai, keyword, page) {

	console.log('search触发了')
	var data = {
		"pingtai": pingtai,
		"keywords": keyword,
		"pageNum": page
	}
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

			var item = ''
			for(var i = 0; i < data.length; i++) {
				var data1 = data[i].data;

				total1 = data[0].total;

				pageSize1 = data[0].size;

				curPage1 = data[0].pages

				totalPage1 = data[0].current

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
		complete: function() {
			getPageBar1();
			$('#pagecount1 span a').on('click', function() {
				console.log('search分页被点了');
				var rel1 = $(this).attr('rel');
				if(rel1) {
					search('/sousuo/', pingtai, keyword, rel1)
				}
			})
		},
		error:function(){
			$('#qingkong').html('加载失败,请稍后再试')
		}
	});
};

function getPageBar1() {

	if(curPage1 > totalPage1) curPage1 = totalPage1;

	if(curPage1 < 1) curPage1 = 1;

	pageStr = "<span>共" + total1 + "条</span><span>" + curPage1 + "/" + totalPage1 + "</span>";

	if(curPage1 == 1) {

		pageStr += "<span>首页</span><span>上一页</span>";

	} else {

		pageStr += "<span><a href='javascript:void(0)' rel='1'>首页</a></span><span> <a href = 'javascript:void(0)'rel= '" + (curPage1 - 1) + "' > 上一页 </a></span> ";

	}

	if(curPage1 >= totalPage1) {

		pageStr += "<span>下一页</span><span>尾页</span>";

	} else {

		pageStr += "<span><a href='javascript:void(0)' rel='" + (parseInt(curPage1) + 1) + "'>下一页 </a></span><span> <a href = 'javascript:void(0)' rel= '" + totalPage1 + "' > 尾页 </a></span>";
	}
	$("#pagecount").css('display', 'none')
	$("#pagecount1").css('display', 'block');
	$("#pagecount1").empty();
	$("#pagecount1").html(pageStr);

}