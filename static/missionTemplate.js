// noinspection JSAnnotator
$.templates("missionTmpl", `<tr class='row' id={{:id}}>
    <td class='cellMissions'><a href='#'><i style='float:left' id='chevron' class='fa fa-chevron-up'></i>
        <div>{{>missionName}}</div>
    </a></td>
    <td class='cellType'>
        <div >{{>missionType}}</div>
    </td>
    <td class='cellSlots'>
        <div >{{>missionPlayers}}</div>
    </td>
    <td class='cellIsland'>
        <div >{{>missionMap}}</div>
    </td>

    <td class='cellPlayed'>
        <div>{{>playedCounter}}</div>
    <td class='cellLastPlayed'>
        <div>{{>lastPlayed}}</div>
    </td>
    <td class='cellAuthor'>
        <div>{{>missionAuthor}}</div>
    </td>
    <td class='cellModified'>
        <div>{{>missionModified}}</div>
    </td>
    <td class='cellStatus'
        <div>{{>status}}</div>
</tr>
<tr id='descRow' class='row descRow' data-missionId={{:id}}>
    <td data-id='id' class='cellDropdown' colspan='10'>
        <p class='fullInfo'>
        <div class='cellDropdownSubtitle'>Framework</div>
        <br>
        <div >{{>framework}}</div>
        </p>
        <p class='fullInfo'>
        <div class='cellDropdownSubtitle'>Author</div>
        <br>
        <div >{{>missionAuthorLong}}</div>
        </p>
        <p class='fullInfo'>
        <div class='cellDropdownSubtitle'>Description</div>
        <br>
        <div>{{>missionDesc}}</div>
        </p>
        <p class='fullInfo'>
        <div class='cellDropdownSubtitle'>Mission Notes</div>
        <br>
        <div>{{>missionNotes}}</div>
        </p>

        <ul class='buttons'>
        {{if allowedToEdit}}
            <li><a data-missionId={{:id}} onclick='editMission(this)'>Edit</a></li>

            <li>
                <label for='fileUpload{{:id}}' class='fileInputLabel'>
                    Browse
                </label>
                <span></span>
                <input id='fileUpload{{:id}}' onchange='updateFileLabel(this)' data-missionId='{{:id}}'
                       style='display:none'
                       type='file'
                       multiple='multiple'/>
                <a onclick='uploadFile(this)'>Submit</a>
                <input id='fileUploadMinor{{:id}}' type='checkbox'></input>
                <label for='fileUploadMinor{{:id}}'>Minor Version</label>
                <span class='uploadErrorMessage'></span>
            </li>
        {{/if}}
            {{if hasOwnProperty('versions')}}
                <li style='float:right'><a data-missionId='{{:id}}' onclick='comment(this)'>Comment</a></li>
            {{/if}}
        {{if allowedToEdit}}
            <li style='float:right'><a data-missionId='{{:id}}' onclick='openDeletePopup(this)'>Delete</a></li>
        {{/if}}
        </ul>
        <!--mission templates go here using compositing -->
        {{for versions tmpl="versionTmpl"/}}
    </td>
</tr>`);