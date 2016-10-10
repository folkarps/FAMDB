function LoadUsers()
{
  $("#missionTable > tbody").html("");

    jQuery.get("/users", "", function (data, status, jqXHR)
    {

        var users = eval(data);
        $("#missionTable > tbody").loadTemplate("userTemplate.html",
            users);
    });
}
function HideAll()
{
  $("#missionsList").hide();
  $("#getout").show();
  $("#getout").append('                <iframe width="560" height="315" src="http://www.youtube.com/embed/gvdf5n-zI14?autoplay=1" frameborder="0" allowfullscreen></iframe>');
}

function setPermissionLevel(select) {
    var user = {};
    user.permissionLevel = $(select).val();
    user.id = $(select).data("userid");
    jQuery.post("/setPermissionLevel", JSON.stringify(user), function (data, status, jqXHR) {
    }).fail(function(data, status, jqXHR) {
        alert(data.responseText);
  });
}

$("#getout").hide();
UpdateLoginButton();
LoadUsers();
