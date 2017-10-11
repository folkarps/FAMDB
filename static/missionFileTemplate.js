$.templates("versionTmpl", `<div class="missionVersionOuter">

    <div style="display:inline-block">
        <img src="images/download.png" alt="Download" data-missionId={{:missionId}} data-versionId={{:id}}
             class="moveButton" onclick="downloadVersion(this)"/>
    </div>

    <div class="missionVersionInner" class='{{:mmExistsClass}}'>

        <div style="display:inline-block;width:80%">{{>name}}</div>
        <img src="images/delete.png" alt="Delete" class='deleteButton {{:toBeDeletedMMClass}}'  data-missionId={{:missionId}} data-versionId={{:id}}
             onclick="deleteVersion(this, 'missionMaking')"/>
    </div>
    <div style="display:inline-block" class='{{:mmExistsMainDoesNotClass}}'>
        <img src="images/requestTransfer.png" alt="Move"  data-missionId={{:missionId}} data-versionId={{:id}}
             class="moveButton" onclick="requestTransfer(this)"/>
    </div>
    <div style="display:inline-block" class='{{:mmExistsMainDoesNotClass}}'>
        <img src="images/move.png" alt="Move"  data-missionId={{:missionId}} data-versionId={{:id}}
             class="moveButton" onclick="moveVersion(this)"/>
    </div>
    <div class="missionVersionInner {{:mainExistsClass}}" style="float:right;">

        <div style="display:inline-block;text-align:left">{{>name}}</div>
        <img src="images/delete.png" alt="Delete" class="deleteButton {{:toBeDeletedMainClass}}"  data-missionId={{:missionId}} data-versionId={{:id}}
             onclick="deleteVersion(this, 'main')"/>

    </div>


</div>`);