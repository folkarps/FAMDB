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
    <td class='cellBroken'><i title='Broken' class='{{:brokenClass}}'></i></td>
    <td class='cellRevision'><i title='Revision' class='{{:revisionClass}}'></i></td>
</tr>
<tr id='descRow' class='row descRow' data-missionId={{:id}}>
    <td data-id='id' class='cellDropdown' colspan='10'>
        <p class='fullInfo'>
        <div class='cellDropdownSubtitle'>Framework</div>
        <br>
        <div >{{>framework}}</div>
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

        <ul class='buttons' data-class='editClass'>
            <li><a data-missionId={{:id}} onclick='editMission(this)'>Edit</a></li>

            <li>
                <label for='{{:fileUploadId}}' class='fileInputLabel'>
                    Browse
                </label>
                <span></span>
                <input id='{{:fileUploadId}}' onchange='updateFileLabel(this)' data-missionId='{{:id}}'
                       style='display:none'
                       type='file'
                       multiple='multiple'/>
                <a onclick='uploadFile(this)'>Submit</a>
                <span class='uploadErrorMessage'></span>
            </li>
            <li style='float:right'><a data-missionId='{{:id}}' onclick='openDeletePopup(this)'>Delete</a></li>
        </ul>
        <!--mission templates go here using compositing -->
        {{for versions tmpl="versionTmpl"/}}
    </td>
</tr>`);