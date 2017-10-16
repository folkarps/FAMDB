$.templates("versionTmpl", `
{{if isComment}}
<div class="missionVersionOuter">

    <div style="border-bottom:"> {{:user}} Said:</div>
    <div class="commentContents"> {{:contents}}</div>
</div>

{{else}}
<div class="missionVersionOuter">

    <div style="display:inline-block">
        <img src="images/download.png" alt="Download" data-missionId={{:missionId}} data-versionId={{:id}}
             class="moveButton" onclick="downloadVersion(this)"/>
    </div>

    {{if existsOnMM}}
        <div class="missionVersionInner">

            <div style="display:inline-block;width:80%">{{>name}}</div>
            {{if allowedToEdit && !toBeDeletedMM}}
                <img src="images/delete.png" alt="Delete" class='deleteButton'  data-missionId={{:missionId}} data-versionId={{:id}}
                     onclick="deleteVersion(this, 'missionMaking')"/>
            {{/if}}
        </div>
    {{/if}}
    {{if !existsOnMain && !requestedTransfer && allowedToEdit}}
        <div style="display:inline-block">
            <img src="images/requestTransfer.png" alt="RT"  data-missionId={{:missionId}} data-versionId={{:id}}
                 class="moveButton" onclick="requestTransfer(this)"/>
        </div>
    {{/if}}
    {{if !existsOnMain && allowedToMove}}
        <div style="display:inline-block">
            <img src="images/move.png" alt="Move"  data-missionId={{:missionId}} data-versionId={{:id}}
                 class="moveButton" onclick="moveVersion(this)"/>
        </div>
    {{/if}}
    {{if existsOnMain}}
        <div class="missionVersionInner" style="float:right;">

            <div style="display:inline-block;text-align:left;width:80%;">{{>name}}</div>
            {{if allowedToEdit && !toBeDeletedMain}}
                <img src="images/delete.png" alt="Delete" class="deleteButton"  data-missionId={{:missionId}} data-versionId={{:id}}
                     onclick="deleteVersion(this, 'main')"/>
             {{/if}}

        </div>
    {{/if}}


</div>
{{/if}}`);