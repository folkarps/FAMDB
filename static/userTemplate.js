$.templates("userTmpl", `
<tr class="row" data-id="id">
    <td class="cellType">
        <div data-content="login">{{>login}}</div>
    </td>
    <td class="cellType">
        <select onchange="setPermissionLevel(this)" data-userId={{:id}}>
            <option value=-1 {{if permissionLevel==-1}}selected{{/if}}>Banned</option>
            <option value=0 {{if permissionLevel==0}}selected{{/if}}>User</option>
            <option value=1 {{if permissionLevel==1}}selected{{/if}}>Trusted MM</option>
            <option value=2 {{if permissionLevel==2}}selected{{/if}}>Mission admin</option>
            <option value=3 {{if permissionLevel==3}}selected{{/if}}>Full admin</option>
        </select>
    </td>
</tr>`);