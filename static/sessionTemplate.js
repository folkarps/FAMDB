$.templates("sessionTmpl", `
<tr class="row" data-id="id">
    <td class="cellMissions"><a href="#"><i style="float:left" id="chevron" class="fa fa-chevron-up"></i>
        <div>{{>name}}</div>
    </a></td>
    <td class="cellType">
        <div>{{>date}}</div>
    </td>
    <td class="cellType">
        <div>{{>host}}</div>
    </td>
    <td class="cellType">
        <div>{{>players}}</div>
    </td>
</tr>
<tr id="descRow" class="row descRow">
    <td class="cellDropdown" colspan="10">
        {{for missionNamesList}}{{>#data}}<br/>{{/for}}
        <ul class="buttons" class={{:editClass}}>
            <li><a data-sessionId={{:id}} onclick="editSession(this)">Edit</a></li>
            <li style="float:right"><a data-sessionId={{:id}} onclick="openDeletePopup(this)">Delete</a></li>
        </ul>
    </td>
</tr>`);