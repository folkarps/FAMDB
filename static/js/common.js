// Functions used by both form.js and missions.js

// Function to populate #authorsSelected dropdown field with all authors from the DB
function GetMissionAuthor(preSelect) {
    jQuery.get("authors", null, function (data, status, jqXHR) {
        arr = eval(data);
        for (var y = 0;y < arr.length;y++) {
            $("#authorSelected").append("<option>" +
            arr[y] +
            "</option>");
        }
    });
}


function ToggleAuthors() {
    $("#authorSelected").toggle();
    $("#missionAuthors").toggle(); 
}

function getQueryDict() {
    queryDict = {}
   location.search.substr(1).split("&").forEach(function(item) {queryDict[item.split("=")[0]] = item.split("=")[1]})
   return queryDict;
}