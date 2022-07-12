var missionTypes = ["Adversarial","Coop","Coop (ZEUS)","Afterparty", "Race"];
var islands = ["Altis","Cam Lao Nam","Gabreta","Khe Sanh","Livonia","Malden","Sefrou-Ramal","Stratis","Tanoa","The Bra","Weferlingen (Summer)","Weferlingen (Winter)","Virtual Reality"];
var statuses = ["Broken", "WIP", "Ready", "Testing", "Transfer", "Testing & Transfer"];


function GetIslandsList(parent) {
    "use strict";

    $.each(islands, function (key, value) {
        $(parent).append($("<option/>", {
            value: value,
            text: value
        }));
    });
}
function GetMissionTypesList(parent) {
    "use strict";
    $.each(missionTypes, function (key, value) {
        $(parent).append($("<option/>", {
            value: value,
            text: value
        }));
    });
}

function GetStatuses(parent) {
    "use strict";
    $.each(statuses, function (key, value) {
        $(parent).append($("<option/>", {
            value: value,
            text: value
        }));
    });
} 
function GenerateMissionTypesCheckbox(parent) {
    "use strict";
    $.each(missionTypes, function (key, value) {
        $('<input />', { type: 'checkbox', id: value, value: value,name: "missionType",checked:true }).appendTo(parent);
        $('<label />', { 'for': value, text: value }).appendTo(parent);
        $('<br/>',{}).appendTo(parent);
    });
} 

