var curPage = 1; //当前页码 

var total, pageSize, totalPage; //总记录数，每页显示数，总页数

//获取数据 

function getData(page) {

	$.ajax({

		type: 'GET',

		url: '/fjieguo/',

		data: {
			'pageNum': page
		},

		dataType: 'json',

		beforeSend: function() {

			$('#table').empty('')
			$('#table').html('加载中...')

		},

		success: function(data) {
			$('#table').html('<table id="tab"  cellspacing="0"></table>')

			var item = ''
			item += '<tr> <th> 分类 </th> <th colspan="4"> 事件 </th> <th> 提交时间 </th> <th> 受理结果 </th> <th> 受理时间 </th></tr>'
			for(var i = 0; i < data.length; i++) {
				total = data[0].total;
				pageSize = data[0].size;
				curPage = data[0].pages
				totalPage = data[0].current

				var data1 = data[i]
				var data2 = data1.data;
				var result;
				if(data2.chulijieguo == 0) {
					result = '已下线'
				} else if(data2.chulijieguo == 1) {
					result = '已恢复'
				} else {
					result = '未处理'
				}
				if(data2.chuli_time == null) {
					data2.chuli_time = ''
				};
				var unixtime = data2.mat_time;
				var unixTimestamp = new Date(unixtime * 1000);
				commonTime = unixTimestamp.toLocaleString('zh', {
					hour12: false
				});

				item += "<tr><td>" + data2.leixing + "</td><td>" + data2.match_name + "</td><td>" + commonTime + "</td><td>" + data2.team_a + "</td><td>" + data2.team_b + "</td><td>" + data2.tijiao_time + "</td><td attr=" + result + ">" + result + "</td><td>" + data2.chuli_time + "</td></tr>";
			}
			$('#tab').append(item);
		},
		complete: function() { //生成分页条 
			console.log('生成分页条')
			getPageBar();　　　　　　　　　　　
			//当点击分页条中的分页链接时， 调用getData(page) 加载对应页码的数据。　　					　　
			$("#pagecount span a").on('click', function() {　　　　　　
				var rel = $(this).attr("rel"); //拿到被点击的a的rel,也就是a的值
				　　　　　　
				if(rel) { //如果rel存在,调用getData方法,传入rel
					　　　　
					getData(rel);　　　　　　
				}　　　　　　　　
			});　　
		},

		error: function() {

			$('#table').html('加载失败,请稍后再试')

		}

	});

}

//获取分页条 

function getPageBar() {
	console.log('getPageBar执行了')
	//页码大于最大页数 

	if(curPage > totalPage) curPage = totalPage; //当前页码大于总页数,那么当前页码等于总页数

	//页码小于1 

	if(curPage < 1) curPage = 1; //当前页码小于1,那么当前页码等于1

	pageStr = "<span>共" + total + "条</span><span>" + curPage + "/" + totalPage + "</span>";

	//如果是第一页 

	if(curPage == 1) {

		pageStr += "<span>首页</span><span>上一页</span>"; //写了个上一页,但是不让点

	} else {

		pageStr += "<span><a href='javascript:void(0)' rel='1'>首页</a></span><span> <a href = 'javascript:void(0)'rel= '" + (curPage - 1) + "' > 上一页 </a></span> ";

	}

	//如果是最后页 

	if(curPage >= totalPage) {

		pageStr += "<span>下一页</span><span>尾页</span>"; //写了个下一页,但是不让点

	} else {

		pageStr += "<span><a href='javascript:void(0)' rel='" + (parseInt(curPage) + 1) + "'>下一页 </a></span><span> <a href = 'javascript:void(0)' rel= '" + totalPage + "' > 尾页 </a></span>";
	}

	$("#pagecount").html(pageStr);

}
$(function() {

	getData(1);

});