function GetMissionAuthor() {
    var MissionObject = Parse.Object.extend("Missions");
    var query = new Parse.Query(MissionObject);
    query.limit(1000);
    query.find({
        success: function(results) {
           // $("#authorSelected").empty();
            //$("#authorSelected").append(
            //    "<option>All Authors</option>");
            var arr = [];
            var authors = [];
            for (var x = 0; x < results.length; x++) {
                var obj = results[x];
                authors = authors.concat(obj.get("missionAuthor").split(','));
            }

            for(var y = 0; y < authors.length;y++) {
                var author = authors[y].trim();
                if (arr.indexOf(author) == -1) {
                    arr.push(author);
                }
            }

            arr.sort();
            for (var y = 0;y < arr.length;y++) {
                $("#authorSelected").append("<option>" +
                arr[y] +
                "</option>");
            }

            if (arr.indexOf(Parse.User.current().get("username")) != -1) {
                $("#authorSelected").val(Parse.User.current().get("username"));
            };
        },
        error: function(error) {
            alert("Error: " + error.code + " " + error.message);
        }
    });
}

function MissionSaveError(string) {
    $("#errorEdit").text(string);
}

function toggleAuthors() {
    $("#authorSelected").toggle();
    $("#missionAuthors").toggle(); 
}