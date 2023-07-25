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
    "Khe Sanh",             // CDLC - SOGPF
    "Livonia",              // DLC  - Contact
    "Maksniemi",            // Mod  - Maksniemi
    "Malden",               // Vanilla
    "Mutambara",            // Mod  - Mutambara
	"Normandy",				// CDLC - Spearhead 1944
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
var frameworks = {
    "Modern FA3 (>= 3.5)": {
        "uiPriority": 0, // order to appear in dropdown, 0 being closet to top
        "versions": [    // order in dropdowns, so newer at top makes sense. Needs to be exhaustive for search to work
            "FA3 3.5.7",
            "FA3 3.5.6",
            "FA3 3.5.5",
            "FA3 3.5.4",
            "FA3 3.5.3",
            "FA3 3.5.2",
            "F3 3.5.1",
            "F3 3.5.0",
            "F3 3.5"
        ]
    },
    "Legacy F3 (3.4.x)": {
        "uiPriority": 1,
        "versions": [
            "F3 3.4.1",
            "F3 3.4.0",
        ]
    },
    "Ancient F3 (<= 3.3.0)": {
        "uiPriority": 2,
        "versions": [
            "F3 3.3.x or older", // Values from database (after db_migrate_framework_prefix_old_f3 cleanup)
            "F3 3.3.0",
            "F3 3.2.2",
            "F3 3.2.1",
            "F3 3.2.0",
            "F3 3.1.x or older"
        ]
    },
    "Unknown framework": {
        "uiPriority": 3,
        "versions": ["Unknown"]
    }
}

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

function PopulateFrameworkCategoryList(parent) {
    "use strict";

    let orderedCategories = Object.keys(frameworks)
        .sort((a,b) => {return frameworks[a].uiPriority - frameworks[b].uiPriority} )

    $.each(orderedCategories, function (key, value) {
        $(parent).append($("<option/>", {
            value: value,
            text: value
        }));
    });
}

function PopulateFrameworkVersionList(parent) {
    "use strict";

    let orderedVersions = Object.keys(frameworks)
        .sort((a,b) => {return frameworks[a].uiPriority - frameworks[b].uiPriority} )
        .flatMap(name => frameworks[name].versions)

    $.each(orderedVersions, function (key, value) {
        $(parent).append($("<option/>", {
            value: value,
            text: value
        }));
    });
}