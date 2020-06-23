let tagNum = 0;

// Textarea expandable inspired by Vanderson https://codepen.io/Vanderson
function expandTextArea() {
    this.style.removeProperty("height");
    this.style.height = this.scrollHeight + 2 + "px";
}

function copyNewIdContent() {
    let viewId = "#tag" + getNumberFromId($(this).attr("id"));
    $(this).on("keydown", function () {
        $(viewId + " a").text() = $(this).val();
    });
}

$("body")
    .on("keydown input", "textarea[data-expandable]", expandTextArea)
    .on("mousedown focus", "textarea[data-expandable]", expandTextArea);

$(window).resize(function () {
    $("textarea[data-expandable]").each(expandTextArea);
});

//Create/Edit/Delete tags in entries

let tagList = ["food", "drink", "yogurt"];

function createTag(id, word) {
    return `<span id="${id}"class="badge badge-pill badge-primary tag"><a href="{{url_for('listing')}}">${word}</a></span>`;
}

$("#edit-tags-btn").on("click", function () {
    $("#edit-tags").toggle();
    //$("#view-tags").toggle();
});

$("#save-tag-btn").on("click", function () {
    $("#edit-tags").toggle();
    //$("#view-tags").toggle();
});

//Delete tag from list
function deleteTag() {
    $(this).click(function () {
        $(this).remove();
    });
}

function getNumberFromId(id) {
    return id.match(/\d+/g)[0];
}

//Add a new tag to list and focus on it to edit
function addNewTag() {
    tagNum += 1;
    let editTagId = "edit-tag-" + tagNum;
    let viewTagId = "tag" + tagNum;
    let newEditTag = `<input id="${editTagId}" type="text" placeholder="new tag" spellcheck="false" class="tag badge-pill badge-primary badge-input" />`;
    let newTag = createTag(viewTagId, "tag name");
    $(this).before(newEditTag);
    $("#" + editTagId).focus();
    $("#edit-tags-btn").before(newTag);
}

$(document).ready(function () {
    //Expand all textareas when document is ready
    $("textarea[data-expandable]").each(expandTextArea);

    //Prevent line breaks in entry names
    $("#review-name").keypress(function (event) {
        if (event.which == "13") {
            return false;
        }
    });

    //Hide the edit tags section on load
    $("#edit-tags").hide();

    //Make delete tags deleteable
    $(".delete-tag").each(deleteTag);

    //Add a new tag
    $(".add-tag").on("click", addNewTag);

    for (let i = 0; i < tagList.length; i++) {
        let tag = createTag(tagNum, tagList[i]);
        $("#view-tags").append(tag);
    }
});
