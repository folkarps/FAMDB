// noinspection JSAnnotator
$.templates("versionTmpl", `
{{if isComment}}
<div class="missionVersionOuter">

    <br/>
    <div style="border-bottom:"> {{>user}}:</div>
    <div class="commentContents"> {{>contents}}
    
        {{if isMissingVersion}}
        <div style="border-bottom:" class="versionDeleted">The version for this comment has been deleted</div>
        {{/if}}
    </div>
</div>

{{else}}
<div class="missionVersionOuter">

    <div class="toolTipContainer" style="display:inline-block">
        <img src="images/download.png" alt="Download" data-missionId={{:missionId}} data-versionId={{:id}}
             class="moveButton" onclick="downloadVersion(this)"/>
        <span class="tooltiptext">Download</span>
    </div>

    {{if existsOnMM}}
        {{if requestedTesting}}
        <img src="images/requestedTransfer.png"/>
        {{/if}}

            <div class="fileNameContainer">{{>name}}</div>
            {{if allowedToEdit && !toBeDeletedMM}}
                <div class="toolTipContainer">
                
                    <img src="images/delete.png" alt="Delete" class='deleteButton'  data-missionId={{:missionId}} data-versionId={{:id}}
                         onclick="deleteVersion(this, 'missionMaking')"/>
                     
                    <span class="tooltiptext">Delete on next cleanup</span>
                </div>
            {{/if}}
    {{else}}
        <div class="fileNameContainer"></div>
    {{/if}}
    {{if !existsOnMain && !requestedTransfer && !requestedTesting && allowedToEdit}}
        <div class="moveButtonContainer toolTipContainer">
            <img src="images/moveSat.png" alt="RT"  data-missionId={{:missionId}} data-versionId={{:id}}
                 class="moveButton" onclick="requestTesting(this)"/>
             <span class="tooltiptext">Request testing</span>
        </div>
    {{/if}}
    {{if !existsOnMain && allowedToMove}}
        <div class="moveButtonContainer toolTipContainer">
            <img src="images/moveNow.png" alt="Move"  data-missionId={{:missionId}} data-versionId={{:id}}
                 class="moveButton" onclick="moveVersion(this)"/>
             <span class="tooltiptext">Move now</span>
        </div>
    {{/if}}
    {{if !existsOnMain && !requestedTesting && !allowedToMove && allowedToEdit}}
        <div class="moveButtonContainer toolTipContainer">
            <img src="images/moveNow.png" alt="Move"  data-missionId={{:missionId}} data-versionId={{:id}}
                 class="moveButton" onclick="requestTransfer(this)"/>
             <span class="tooltiptext">Request transfer now</span>
        </div>
    {{/if}}
    {{if existsOnMain}}
            <div class="fileNameContainer">{{>name}}</div>
            {{if allowedToEdit && !toBeDeletedMain}}
                <div class="toolTipContainer">
                    <img src="images/delete.png" alt="Delete" class="deleteButton"  data-missionId={{:missionId}} data-versionId={{:id}}
                         onclick="deleteVersion(this, 'main')"/>
                    <span class="tooltiptext">Delete on next cleanup</span>
                </div>
             {{/if}}

    {{/if}}


</div>
{{/if}}`);