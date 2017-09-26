$.templates("sessionMissionTmpl", `<div class="sessionMission">
    <div class="missionNameDiv" style="display:inline-block;">{{>missionName}}</div>
    <button style="display:inline-block;float:right" onclick="removeMission(this)">Remove</button>
</div>`);