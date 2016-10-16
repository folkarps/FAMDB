
function LoadData() {


    jQuery.get("/sessions", [], function (data, status, jqXHR)
    {
        //clear out the table
        $("#missionTable > tbody").html("");

        var missions = eval(data);
        missions.forEach(function(item) {
            //format data for template
            if(!item.allowedToEdit) {
                item.editClass = 'hideMe';
            }
        })
        $.addTemplateFormatter("missionNameListFormatter",
            function(value, template) {
                var stringValue = "";
                value.forEach(function(name) {stringValue += name + "<br/>"});
                return stringValue;
            });
        $("#missionTable > tbody").loadTemplate("sessionTemplate.html",
            missions);



        // Hide all description rows
        $('.descRow').hide();

        // Setup hide/show toggle on clicking the mission name
        $(".cellMissions").click(function() {
            $(this).find("#chevron").toggleClass("fa-chevron-down fa-chevron-up");
            $(this).parent().next('#descRow').toggle();
            return false;
        });

        // Sort the table
        $("#missionTable").tablesorter({
            // sort on the first column and third column, order asc
            widgets: ["zebra"], // initialize zebra striping of the table
            sortList: [[0,0]], // Sort table alphabetically by default
            widgetZebra: {
                css: ["normal-row", "odd"]
            },
            cssChildRow: "descRow"
        });
        if(getQueryDict()['sessionId'] != null) {
            table = $("#missionTable > tbody");
            children = table.children("[data-sessionid=" +getQueryDict()['sessionId'] + "] ");
            item = children[0];
            cellMissions = $($(item).prev().children()[0]).find("i")[0];
            $(cellMissions).toggleClass("fa-chevron-down fa-chevron-up")
            $(item).toggle();

        }

        if(!isLoggedIn()) {
            $(".buttons").css("display", "none");
        }

        setTimeout(function() {
            var resort = false, // re-apply the current sort
                callback = function(table) {};
            // let the plugin know that we made a update, then the plugin will
            // automatically sort the table based on the header settings
            $("table").trigger("updateAll", [resort,
                callback
            ]);

        }, 100);
    });
}

function editSession(button) {
        window.location.href = "sessionForm.html?sessionId=" + $(button).data("sessionid");
}


function openDeletePopup(button) {
    window.delMissionId = $(button).data("sessionid");
    OpenPopup("#deleteWindow");
}

function deleteSession() {
    var sessionId = window.delSessionId;
    var data = {sessionId:sessionId};
    jQuery.post("/deleteSession", JSON.stringify(data), function(data, status, jqXHR) {
            window.location.href = "index.html";
    });

}
if(getPermissionLevel() < 2) {
    $("#AddButton").hide()
}

