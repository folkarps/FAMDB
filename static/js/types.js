var missionTypes = ["Adversarial","Coop","Coop (ZEUS)","Afterparty", "Race"];
var statuses = ["Broken", "WIP", "Ready", "Testing", "Transfer", "Testing & Transfer"];
var islands = [
    "Altis",                // Vanilla
    "Cam Lao Nam",          // CDLC - SOGPF
    "Cham",                 // Mod  - Cham
    "Cham (Winter)",        // Mod  - Cham
    "Gabreta",              // CDLC - CSLA
    "Hellanmaa",            // Mod  - Hellanmaa
    "Hellanmaa (Winter)",   // Mod  - Hellanmaa
    "Khe Sanh",             // CDLC - CSLA
    "Livonia",              // DLC  - Contact
    "Maksniemi",            // Mod  - Maksniemi
    "Malden",               // Vanilla
    "Mutambara",            // Mod  - Mutambara
    "Pulau",                // Mod  - Pulau
    "Sefrou-Ramal",         // CDLC - WS
    "Stratis",              // Vanilla
    "Suursaari",            // Mod  - Suursaari
    "Tanoa",                // DLC  - Apex
    "The Bra",              // CDLC - SOGPF
    "Vinjesvingen",         // Mod  - Vinjesvingen
    "Weferlingen (Summer)", // CDLC - GM
    "Weferlingen (Winter)", // CDLC - GM
    "Virtual Reality"       // Vanilla
];


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

