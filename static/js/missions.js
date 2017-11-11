// Functions used to populate the main table
var blah = false;

function LoadData() {
    var mapVal = $("#islandSelected").val();
    var authorVal = $("#authorSelected").val();
    var searchVal = $("#searchText").val();
    var params = {};
    params["map"] = mapVal;
    params["status"] = $("#status").val();
    params["author"] = authorVal;


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


    jQuery.get("missions", params, function (data, status, jqXHR)
    {
        //clear out the table
        $("#missionTable > tbody").html("");

        var missions = eval(data);


        var contents = $.render.missionTmpl(missions);
        $("#missionTable > tbody").html(contents);


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
            cssChildRow: "descRow",
            emptyTo: 'emptyMin',
            cssAsc           : 'fa fa-sort-asc',
            cssDesc          : 'fa fa-sort-desc',
            cssNone          : 'fa fa-sort',
        });
        if (getQueryDict()['missionId'] != null && !blah) {
            blah = true;
            table = $("#missionTable > tbody");
            children = table.children("[data-missionid=" +getQueryDict()['missionId'] + "] ");
            item = children[0];
            cellMissions = $($(item).prev().children()[0]).find("i")[0];
            $(cellMissions).toggleClass("fa-chevron-down fa-chevron-up")
            $(item).toggle();
            $('html, body').animate({
                scrollTop: $(cellMissions).offset().top
            }, 500);


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
    data.missionId = $(mission).data("missionid");
    data.versionId = $(mission).data("versionid");
    data.origin = origin;
    jQuery.post("archive", JSON.stringify(data), function (data, status, jqXHR) {
        if(status == "success") {
                $(mission).siblings(".deleteButton").remove()
                $(mission).remove()
            }
        });
}
function deleteVersion(mission, origin) {
    var data = {}
    data.missionId = $(mission).data("missionid");
    data.versionId = $(mission).data("versionid");
    data.origin = origin;
    jQuery.post("deleteVersion", JSON.stringify(data), function (data, status, jqXHR) {
            if(status == "success") {
                $(mission).remove()
            }

        });
}

function moveVersion(mission) {
    var data = {}
    data.missionId = $(mission).data("missionid");
    data.versionId = $(mission).data("versionid");
    jQuery.post("move", JSON.stringify(data), function (data, status, jqXHR) {
            if(status == "success") {
                $(mission).remove()
            }
        });
}

function requestTransfer(mission) {
    var data = {}
    data.missionId = $(mission).data("missionid");
    data.versionId = $(mission).data("versionid");
    jQuery.post("requestTransfer", JSON.stringify(data), function (data, status, jqXHR) {
            if(status == "success") {
                $(mission).remove()
            }

        });
}

function requestTesting(mission) {
    var data = {}
    data.missionId = $(mission).data("missionid");
    data.versionId = $(mission).data("versionid");
    jQuery.post("requestTesting", JSON.stringify(data), function (data, status, jqXHR) {
        if (status == "success") {
            $(mission).remove()
        }

    });
}

function editMission(button) {
        window.location.href = "missionForm.html?missionId=" + $(button).data("missionid");
}

function comment(button) {

    var object ={missionId:$(button).data("missionid"), showReject:(getPermissionLevel() > 1)}
    var contents = $.render.commentTmpl([object]);
    $(button).parents(".buttons").after(contents);
}

function submitComment(button) {
    var data = {}
    data.missionId = $(button).data("missionid");
    data.comment = $("#comment" + data.missionId).val();
    data.rejection = $("#reject" + data.missionId).prop("checked");
    jQuery.post("comment", JSON.stringify(data), function (returnData, status, jqXHR) {
            if(status == "success") {
                window.location.href = "index.html?missionId=" + data.missionId;
            }

        });
}

function uploadFile(submitButton){
    var button = $(submitButton).siblings("input")[0];
    var files = button.files;
    for(var i=0; i<files.length; i++){
        var file = files[i];
        var missionId = $(button).data("missionid");
        var url = 'upload?missionId=' + missionId;
        var xhr = new XMLHttpRequest();
        var fd = new FormData();
        xhr.open("POST", url, true);
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4 && xhr.status == 200) {
                // Every thing ok, file uploaded
                window.location.href = "index.html?missionId=" + missionId;
            }else {
                if(xhr.status == 500) {
                    var span = $($(submitButton).siblings(".uploadErrorMessage")[0])[0];
                    span.innerText = xhr.responseText;
                }
            }
        };
        fd.append("upload_file", file);
        xhr.send(fd);
    }
}

function downloadVersion(button) {
        window.location.href = "download?versionId=" + $(button).data("versionid");
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
function openDeletePopup(button) {
    window.delMissionId = $(button).data("missionid");
    OpenPopup("#deleteWindow");
}

function deleteMission() {
    var missionId = window.delMissionId;
    var data = {missionId:missionId};
    jQuery.post("deleteMission", JSON.stringify(data), function(data, status, jqXHR) {
            window.location.href = "index.html";
    });

}
