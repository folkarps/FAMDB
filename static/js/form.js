// Functions for the add/edit form


if (!isLoggedIn()) {
    window.location.href = "index.html";
}

UpdateLoginButton();
$("#missionAuthors").hide();
$("#editMissionsAuthorToggle").hide();

function LoadMission() {
    //load mission if exists
    var queryDict = getQueryDict();

    if(queryDict['missionId'] != null) {
        jQuery.get("/missions", queryDict, function (data, status, jqXHR) {
            var missions = eval(data);
            if(missions.length > 0) {
                var mission = missions[0]
                $("#loading").show();
                $('.editMissionsTitle').append(' Edit Mission');
                $('#editMissionsHeader').children().append('Edit Mission');
                $("#authorSelected").hide();
                $("#missionAuthors").show();
                $("#missionName").val(mission.missionName);
                $("#missionIsland").val(mission.missionMap);
                $("#missionType").val(mission.missionType);
                $("#missionSlots").val(mission.missionPlayers);
                $("#missionPlaycount").val(mission.playedCounter);
                $("#authorSelected").val(mission.missionAuthor);
                $("#missionAuthors").val(mission.missionAuthor);
                $("#missionDescription").val(mission.missionDesc);
                $("#missionNotes").val(mission.missionNotes);

                if (mission.isBroken == 1) {
                    $("#missionBroken").prop('checked',true);
                }
                if (mission.needsRevision == 1) {
                    $("#missionNeedsRevision").prop('checked',true);
                }
                $("#loading").hide();
            }else {
                setNewMission();
            }
        });
    }else {
        setNewMission();
    }

    
    $('#missionSave').click({}, function(event) {
        WriteMission();
    });
}

function setNewMission() {
        $('.editMissionsTitle').append(' Add Mission');
        $('#editMissionsHeader').children().append('Add Mission');
        $("#editMissionsAuthorToggle").show();
}

function WriteMission() {
    
    var missionName = $("#missionName").val();
    var missionGame = $("#missionGame").val();
    var missionIsland = $("#missionIsland").val();
    var missionSession = $("#missionSession").val();
    var missionType = $("#missionType").val();
    var missionSlots = Number($("#missionSlots").val());
    var missionPlaycount = Number($('#missionPlaycount').val());
    var missionAuthor = "";
    
    // Only if the missionAuthors field is visible and not empty it is used to pass the author's name
    if ($("#missionAuthors").is(":visible") && $("#missionAuthors") !== "") {
        missionAuthor = $("#missionAuthors").val();
    } else {
        missionAuthor = $("#authorSelected").val();
    }
    
    var missionDescription = $("#missionDescription").val();
    var missionNotes = $("#missionNotes").val();
    var isBroken = $('#missionBroken').prop('checked');
    var needsRevision = $('#missionNeedsRevision').prop('checked');

    if ( !(missionName.match(/^[a-zA-Z0-9'-_][a-zA-Z0-9'-_ ]+$/)) || missionName === "" || missionName === null) {
        MissionSaveError("Enter a mission name!");
        return false;
    }
    if (missionIsland === "" || missionIsland === null) {
        MissionSaveError("Select an island!");
        return false;
    }
    if (missionType === "" || missionType === null) {
        MissionSaveError("Select a mission type!");
        return false;
    }

    if (isNaN(missionSlots)  || missionSlots <= 0 || missionSlots === null) {
        MissionSaveError("Slots must be a number > 0");
        return false;
    }

    if (isNaN(missionPlaycount)  || missionPlaycount < 0 || missionPlaycount === null) {
        MissionSaveError("Playcount must be a number at least 0");
        return false;
    }

    if (missionAuthor === "" || missionAuthor === null) {
        MissionSaveError("Select or enter an author!");
        return false;
    }
    
    if (missionDescription.trim().length < 1  || missionDescription === null) {
        MissionSaveError("Enter a description for your mission!");
        return false;
    }
    if (isBroken || needsRevision) {
        if (missionNotes.trim().length < 1 || missionNotes ===
            null) {
            MissionSaveError("Please enter notes on the state of the mission!");
            return false;
        }
    }
    var data = {}
    data.missionName = missionName;
    data.missionMap = missionIsland;
    data.missionType = missionType;
    data.missionPlayers = missionSlots;
    data.playedCounter = missionPlaycount;
    data.missionAuthor = missionAuthor;
    data.missionDesc = missionDescription;
    data.isBroken = isBroken;
    data.needsRevision = needsRevision;
    data.missionNotes = missionNotes;
    data.framework = $("#framework").val();
    if(getQueryDict()['missionId'] != null) {

        data.missionId = getQueryDict()['missionId'];
    }

    jQuery.post("/saveMission", JSON.stringify(data),  function (data, status, jqXHR) {
        data = data.replace("location=", "");
        data = data.replace(/(?:\r\n|\r|\n).*/g, "");
        if(status == "success") {
            window.location.href = "index.html?missionId="+data;
        }else {
            MissionSaveError(data.responseText);
        }
    }).fail(function(data, status, jqXHR) {
        MissionSaveError(data.responseText);
  });

    
    return false;
}

function MissionSaveError(string) {
    $("#errorEdit").text(string);
}

LoadMission();
GetMissionAuthor();