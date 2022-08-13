function LoadUsers()
{
  $("#missionTable > tbody").html("");

    jQuery.get("users", "", function (data, status, jqXHR)
    {

        var users = eval(data);
        var contents = $.render.userTmpl(users);
        $("#missionTable > tbody").html(contents);
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
    jQuery.post("setPermissionLevel", JSON.stringify(user), function (data, status, jqXHR) {
    }).fail(function(data, status, jqXHR) {
        alert(data.responseText);
  });
}

function cleanup() {
    HidePopup("#deleteWindow")
    jQuery.post("cleanup", {}, function(data, status, jqXHR) {
        var parsed = JSON.parse(data)

        // Debug logging
        for(const deleted of parsed.result.deleted) {
            console.log(`Deleted ${deleted.filename} from server ${deleted.from}`)
        }
        for(const broken of parsed.result.broken) {
            console.log(`Mission ${broken} had no versions/files, marking as Broken`)
        }

        alert('Cleanup complete! See browser debug console log')
    });
}

function sync() {
    jQuery.post("sync", {}, function(data, status, jqXHR) {
        alert('Sync complete!')
    });
}
$("#getout").hide();
UpdateLoginButton();
LoadUsers();
