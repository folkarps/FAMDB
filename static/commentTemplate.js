$.templates("commentTmpl", `
<div class='commentBlock'>
    <textArea class='editMissionsContainer' id='comment{{:missionId}}'/>
    <div class='commentBlockButtons'>
    {{if showReject}}
        <input class='rejectVersionCheckbox' id='reject{{:missionId}}' type='checkbox'/>
        <label for='reject{:missionId}}'>Rejection</label>
    {{/if}}
    <a class='submitCommentButton' data-missionId='{{:missionId}}' onclick='submitComment(this)'>Submit</a>
    </div>
</div>

    `);