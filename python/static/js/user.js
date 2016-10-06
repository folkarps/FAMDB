function UpdateLoginButton() {
    if(document.cookie.includes("sessionId")) {
        $("#LogoutButton").html("<i class='fa fa-sign-out'></i>Logout");
        $("#AddButton").show();
    }
    else {
        $("#LogoutButton").html("<i class='fa fa-sign-in'></i>Login");
        $("#AddButton").hide();
    }
}

function Login() {
    $("#errorLogin").text("");
    var data = $("#loginName").val() +"\n" + $("#PasswordInput").val();
    jQuery.post("/login", data, function( data ) {
            //refresh current page with new cookies so that the buttons are correct
            //if cookie is set, login was accepted, else display data as error message
            if(document.cookie.includes("sessionId")) {
                HidePopup("#loginWindow");
                UpdateLoginButton();
                RefreshPage();
            }else {
                $("#errorLogin").text(data);
            }
    })
}

function SignUp() {
    $("#errorSignup").text("");
    var data = $("#signupName").val() + "\n" + $("#signupEmail").val() + "\n" + $("#signupPassword").val();
    jQuery.post("/signup", data, function (data) {

            //refresh current page with new cookies so that the buttons are correct
            //if cookie is set, login was accepted, else display data as error message
            if(document.cookie.includes("sessionId")) {
                HidePopup("#loginWindow");
                $("#signupScreen").hide();
                $("#loginScreen").show();
                UpdateLoginButton();
            }else {
                $("#errorSignup").text(data);
            }
    });
}

// Refresh page. If user is on index.html it'll only reload the data
function RefreshPage() {
    if (location.href.split(location.host)[1].indexOf("index") === -1) {
        return window.location.href = "index.html";
    } else {
        LoadData();
    }
}

$('#LogoutButton').click(function() {
    if (isLoggedIn()) {
        //delete session cookie
        UpdateLoginButton();
        RefreshPage();
    }
    else {
        OpenPopup("#loginWindow");
    }
});
$("#forgottonPassword").click(function() {
    $("#forgottenScreen").show();
    $("#loginScreen").hide();
});
$("#forgottenWindowOk").click(function() {
	$("#errorForgot").text("");

	jQuery.post("/forgotPass", data, function (data) {
        //if data returned anything it would be an error message
    });

    var val = $("#forgottonUsername").val();
    Parse.User.requestPasswordReset(val, {
        success: function() {
            $("#forgottenScreen").hide();
            $("#loginScreen").show();
        },
		error: function(error) {
			$("#errorForgot").text(error.message);
		}
    });
});
$('#forgottenWindowCancel').click(function() {
	$("#errorForgot").text("");
    $("#forgottenScreen").hide();
    $("#loginScreen").show();
});
$('#signupWindowOk').click(function() {
    SignUp();
});
$('#loginWindowOk').click(function() {
    Login();
});
$('#loginWindowSignup').click(function() {
    $("#signupScreen").show();
    $("#loginScreen").hide();
});
$('#signupWindowCancel').click(function() {
    $("#signupScreen").hide();
    $("#loginScreen").show();
});
$('#loginWindowCancel').click(function() {
    HidePopup("#loginWindow");
    $("#signupScreen").hide();
    $("#loginScreen").show();
});
