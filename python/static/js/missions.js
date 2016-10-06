// Functions used to populate the main table


//getMissions
//uploadMission
//move mission
//saveMission

function LoadData() {
    var sessionVal = $("#sessionSelected").val();
    var mapVal = $("#islandSelected").val();
    var authorVal = $("#authorSelected").val();
    var gameVal = $("#gameSelected").val();
    var MissionObject = Parse.Object.extend("Missions");
    var searchVal = $("#searchText").val();
    var params = {};
    params["map"] = mapVal;
    params["author"] = authorVal;
    params["isBroken"] = $("#missionBroken:checked").val();
    params["needsRevision"] = $("#missionNeedsRevision:checked").val();


    var checkboxes = $("#missionTypes").find(':checkbox');
    var typeString = [];
    for(var x = 0;x<checkboxes.length;x++) {
        var checkbox = checkboxes[x];
        if(checkbox.checked === true) {
            typeString.push(checkbox.id);
        }
    }

    params["missionTypes"] = typeString;
    params["playerMax"] = Number($("#slotsMax").val());
    params["playerMin"] = Number($("#slotsMin").val());
    params["name"] = searchVal;
    params["countMax"] = Number($("#playcountMax").val());
    params["countMin"] = Number($("#playcountMin").val());
    params["session"] = sessionVal;
    params["game"] = gameVal;


    jQuery.get("/missions", params, function (data, status, jqXHR)
    {
        //clear out the table
        $("#missionTable > tbody").html("");

        var missions = eval(data);
        missions.forEach(function(item) {
            //format data for template
            if(item.isBroken == 0) {
                item.brokenClass = ''
            }else {
                item.brokenClass = 'fa fa-exclamation-triangle'
            }
            if(item.needsRevision == 0) {
                item.revisionClass = ''
            }else {
                item.revisionClass = 'fa fa-exclamation-circle'
            }
        })

        $("#missionTable > tbody").loadTemplate("missionTemplate.html",
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

function archiveVersion(mission) {
    jQuery.post("/archive", [
        $(mission).data("missionId")]);
    //\ refresh or just mark the archive button as unavailable
}
function deleteVersion(mission) {
    jQuery.post("/delete", [
        $(mission).data("missionId")]);
    //\ refresh or just mark the delete button as unavailable
}