$.templates("tagsIndexListTmpl", `
<ul>
{{props tagsIndex}}
    <li><div id="{{>key}}" class="tagIndexHeading">#{{>key}}</div>
        <ul>
        {{for prop}}<li><a href="index.html?missionId={{>id}}">{{>name}}</a></li>{{/for}}
        </ul>
    </li>
{{/props}}
`);

function LoadData() {
    $.getJSON("validTags", function(data) {
        var validTags = data;
        validTags.sort();

        $.getJSON("missions", function(data) {
            var missions = data;
            var tagsIndex = {};

            validTags.forEach(t => tagsIndex[t] = []);
            missions.forEach(m => m.tags.forEach(t => tagsIndex[t].push({name: m.missionName, id: m.id})));
            validTags.forEach(t => tagsIndex[t].sort((a,b) => a.name.localeCompare(b.name)));

            $('#missionsListTableContainer').html($.render.tagsIndexListTmpl({validTags: validTags, tagsIndex: tagsIndex}));
        });
    });
}

UpdateLoginButton();
LoadData();