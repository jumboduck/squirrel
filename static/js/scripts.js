let tagNum = 0;

// Textarea expandable inspired by Vanderson https://codepen.io/Vanderson
function expandTextArea() {
    this.style.removeProperty("height");
    this.style.height = this.scrollHeight + 2 + "px";
}

$("body")
    .on("keydown input", "textarea[data-expandable]", expandTextArea)
    .on("mousedown focus", "textarea[data-expandable]", expandTextArea);

//Copy content of new tag to tag list when created
$("body").on("keydown input", ".badge-input", function () {
    let viewId = "#tag" + getNumberFromId($(this).attr("id"));
    $(viewId + " a").text($(this).val());
    $(this).width($(viewId).width());
});

$(window).resize(function () {
    $("textarea[data-expandable]").each(expandTextArea);
});

// Create/Edit/Delete tags in entries

let tagList = ["food", "drink", "yogurt", "aerosol"];

function createTag(id, word) {
    return `<span id="${id}"class="badge badge-pill badge-primary tag"><a href="{{url_for('listing')}}">${word}</a></span>`;
}

function createDeleteTag(id, word) {
    return `<span id="${id}" class="badge badge-pill badge-primary tag delete-tag">${word}
    <span class="material-icons">cancel</span></span>`;
}

$("#edit-tags-btn").on("click", function () {
    $("#edit-tags").toggle();
    $("#view-tags").toggle();
});

$(document).on("click", "#save-tag-btn", function () {
    $("#edit-tags").toggle();
    $(".badge-input").each(function () {
        let newDeleteTag = createDeleteTag($(this).attr("id"), $(this).val());
        $("#new-tag").before(newDeleteTag);
        $(this).remove();
    });
    $("#view-tags").toggle();
});

function getNumberFromId(id) {
    return id.match(/\d+/g)[0];
}

// Delete tag from list
function deleteTag() {
    $(this).click(function () {
        let viewId = "#tag" + getNumberFromId($(this).attr("id"));
        $(this).remove();
        $(viewId).remove();
    });
}

// Add a new tag to list and focus on it to edit
function addNewTag() {
    let editTagId = "edit-tag-" + tagNum;
    let viewTagId = "tag" + tagNum;
    let newEditTag = `<input id="${editTagId}" type="text" placeholder="new tag" spellcheck="false" class="tag badge-pill badge-primary badge-input" />`;
    let newTag = createTag(viewTagId, "tag name");
    $(this).before(newEditTag);
    $("#" + editTagId).focus();
    $("#view-tags").append(newTag);
    tagNum += 1;
}

$(document).ready(function () {
    //Expand all textareas when document is ready
    $("textarea[data-expandable]").each(expandTextArea);

    // Prevent line breaks in entry names
    $("#review-name").keypress(function (event) {
        if (event.which == "13") {
            return false;
        }
    });

    // Hide the edit tags section on load
    $("#edit-tags").hide();

    // Make delete tags deleteable
    $(".delete-tag").each(deleteTag);

    // Add a new tag
    $(".add-tag").on("click", addNewTag);

    // Generate tag lists
    for (let i = 0; i < tagList.length; i++) {
        let tag = createTag("tag" + tagNum, tagList[i]);
        let deleteTag = createDeleteTag("edit-tag-" + tagNum, tagList[i]);
        $("#view-tags").append(tag);
        $("#new-tag").before(deleteTag);
        tagNum++;
    }
    // Make delete tags deleteable
    $(".delete-tag").each(deleteTag);
});
