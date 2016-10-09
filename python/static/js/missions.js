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
            if(item.isBroken == 1) {
                item.brokenClass = 'fa fa-exclamation-triangle'
            }else {
                item.brokenClass = ''
            }
            if(item.needsRevision == 1) {
                item.revisionClass = 'fa fa-exclamation-circle'
            }else {
                item.revisionClass = ''
            }
        })

        $("#missionTable > tbody").loadTemplate("missionTemplate.html",
            missions);

        missions.forEach(function(item) {
            if(item.versions != null) {
                item.versions.forEach(function(version) {
                    if(version.existsOnMain == 0) {
                        version.mainExistsClass = 'hideMe';
                    }
                    if(version.existsOnMM == 0) {
                        version.mmExistsClass = 'hideMe';
                    }
                    if(!(version.existsOnMM == 1 && version.existsOnMain == 0)) {
                        version.mmExistsMainDoesNotClass = 'hideMe';
                    }
                });
                $($("#missionTable").find("[data-missionIdBlah=" + item.id + "]")).loadTemplate("missionFileTemplate.html", item.versions);
            }
        })


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
        if(getQueryDict()['missionId'] != null) {
            table = $("#missionTable > tbody");
            children = table.children("[data-missionid=" +getQueryDict()['missionId'] + "] ");
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

function archiveVersion(mission, origin) {
    var data = {}
    data.missionId = $(mission).data("missionId");
    data.versionId = $(mission).data("versionId");
    data.origin = origin;
    jQuery.post("/archive", JSON.stringify(data), function (data, status, jqXHR) {
            window.location.href = "index.html?missionId=" + $(mission).data("missionId");
        });
}
function deleteVersion(mission, origin) {
    var data = {}
    data.missionId = $(mission).data("missionId");
    data.versionId = $(mission).data("versionId");
    data.origin = origin;
    jQuery.post("/delete", JSON.stringify(data), function (data, status, jqXHR) {
            window.location.href = "index.html?missionId=" + $(mission).data("missionId");
        });
}

function moveVersion(mission) {
    var data = {}
    data.missionId = $(mission).data("missionId");
    data.versionId = $(mission).data("versionId");
    jQuery.post("/move", JSON.stringify(data), function (data, status, jqXHR) {
            window.location.href = "index.html?missionId=" + $(mission).data("missionId");
        });
}

function editMission(button) {
        window.location.href = "form.html?missionId=" + $(button).data("missionid");
}

function uploadFile(submitButton){
    var button = $(submitButton).siblings("#fileinput")[0];
    var files = button.files;
    for(var i=0; i<files.length; i++){
        var file = files[i];
        var url = '/upload?missionId=' + $(button).data("missionid");
        var xhr = new XMLHttpRequest();
        var fd = new FormData();
        xhr.open("POST", url, true);
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4 && xhr.status == 200) {
                // Every thing ok, file uploaded
                console.log(xhr.responseText); // handle response.
            }
        };
        fd.append("upload_file", file);
        xhr.send(fd);
    }
}

function updateFileLabel(uploadSystem) {
    var div = $(uploadSystem).siblings("span")[0];
    var files = uploadSystem.files;
    var text = ""
    for(var i=0; i < files.length; i++) {
        text += files[i].name + ",";
    }
    div.innerHTML = (text)
}
function getQueryDict() {
    queryDict = {}
   location.search.substr(1).split("&").forEach(function(item) {queryDict[item.split("=")[0]] = item.split("=")[1]})
   return queryDict;
}