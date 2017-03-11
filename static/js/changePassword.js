
$("#updatePassword").click(function() {
    var val = $("#passwordInput").val();

    var data = JSON.stringify({password:val, link:getQueryDict()['link']});


	jQuery.post("changePasswordInternal", data, function (data) {
        //if data returned anything it would be an error message
        if(data == null || data == '') {
            $("#serverError").html("successfully changed password, <a href=\"/index.html\".>go log in</a>");
        }else {
			$("#serverError").text(data);
        }
    });
});