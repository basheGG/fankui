$('#help a').click(function() {

	$('#login').slideDown(500);

	return false
});
$('#login').click(function() {

	$('#login').slideUp(500);

	return false
})
$('#form').click(function() {

	event.stopPropagation();

});

$('#button').click(function() {
	//	console.log($('#uname').val())
	//	console.log($('#upwd').val())
	var uname = $.trim($("#uname").val());
	var upwd = $.trim($("#upwd").val());
	if(uname == "") {
		$('#password').css('display', 'block')
		return false;
	} else if(upwd == "") {
		$('#password').css('display', 'block')
		return false;
	} else {
		$('#password').css('display', 'none')
	}
	//ajax去服务器端校验
	var data = {
		uname: uname,
		upwd: upwd
	};
	// console.log(data)
	$.ajax({

		url: "/index/",
		type: "POST",
		data: data,
		//contentType: "application/json;charset=utf-8",
		async: false,
		success: function(data) {
			console.log(data)
			if(data==0){
				$("#tishi").css('display', 'block')
			}else{
				window.location.href=data;
			}


				}
	});
})