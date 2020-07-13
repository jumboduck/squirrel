let tagNum = $(".view-tag").length + 1;

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
    let widthId = "#width" + getNumberFromId($(this).attr("id"));
    // Update name of View Tag
    $(viewId + " a").text($(this).val());
    // Update tag url
    $(viewId + " a").attr("href", "../listing/" + $(this).val());
    $(widthId).text($(this).val());
    $(this).width($(widthId).width());
});

// Prevents line breaks in Review Name and tags.
// Pressing enter will instead send focus to the next element.
$("body").on("keypress", "#name, .badge-input", function (event) {
    if (event.keyCode === 13) {
        $(this).blur();
        return false;
    }
});

// Expandable text areas resize when window size is changed
$(window).resize(function () {
    $("textarea[data-expandable]").each(expandTextArea);
});

// Create/Edit/Delete tags in entries

// Creating a new HTML Tag
function createTag(id, word) {
    return `<span id="${id}"class="view-tag badge badge-pill badge-primary tag"><a href="/listing/${word}">${word}</a></span>`;
}

// Creating a new HTML Delete Tag
function createDeleteTag(id, word) {
    return `<span id="${id}" class="badge badge-pill badge-primary tag delete-tag">${word}
    <span class="material-icons">cancel</span></span>`;
}

// Turning on Tag Edit mode
$("#edit-tags-btn").on("click", function () {
    $("#edit-tags").toggle();
    $("#view-tags-container").toggle();
});

// Saving changes to tags
$(document).on("click", "#save-tag-btn", function () {
    $("#edit-tags").toggle();
    $(".badge-input").each(function () {
        // If nothing has been inputed the new tag is deleted
        if (!$(this).val()) {
            $(this).remove();
            $("#tag" + getNumberFromId($(this).attr("id"))).remove();
        } else {
            let newTagContent = tagsToString("#hidden_tags", this);
            console.log(newTagContent);

            let newDeleteTag = createDeleteTag(
                $(this).attr("id"),
                $(this).val()
            );
            $("#hidden_tags").val(newTagContent);
            $("#new-tag").before(newDeleteTag);
            $(".delete-tag").each(deleteTag);
            $(this).remove();
        }
    });
    // Send new tag information to the database
    sendTagData();
    // Remove element used to resize tag inputs
    $(".width-machine").each(function () {
        $(this).remove();
    });
    // Return to normal tag view
    $("#view-tags-container").toggle();
});

function getNumberFromId(id) {
    return id.match(/\d+/g)[0];
}

// Delete tag from list
function deleteTag() {
    $(this).click(function () {
        let viewId = "#tag" + getNumberFromId($(this).attr("id"));
        // Make value of hidden field an array, remove the deleted tag, then rebuild string
        let tagArray = $("#hidden_tags").val().split(",");
        let newTagArray = tagArray.filter((tag) => tag !== $(viewId).text());
        $("#hidden_tags").val(newTagArray.join());
        $(this).remove();
        $(viewId).remove();
    });
}

// Add a new tag to list and focus on it to edit
function addNewTag() {
    let editTagId = "edit-tag-" + tagNum;
    let viewTagId = "tag" + tagNum;
    let widthMachineId = "width" + tagNum;
    let newEditTag = `<input id="${editTagId}" type="text" maxlength="20" placeholder="new tag" spellcheck="false" class="tag badge-pill badge-primary badge-input" />`;
    let newTag = createTag(viewTagId, "tag name");
    let newWidthMachine = `<span aria-hidden="true" id="${widthMachineId}"class="badge badge-pill badge-primary tag width-machine">invisible</span>`;
    $(this).before(newEditTag);
    $("#" + editTagId).focus();
    $("#view-tags").append(newTag);
    $(".entry").append(newWidthMachine);
    tagNum += 1;
}

// In new entry form, changes text input text when a new file is chosen
$(".custom-file-input").change((e) => {
    let fileName = e.target.files[0].name;
    $(".custom-file-label").text(fileName);
});

// Generate string from input tag elements into hidden field separated by commas
// If no value is there, it returns the input
function tagsToString(hiddenTagEl, inputEl) {
    if ($(hiddenTagEl).val()) {
        return $(hiddenTagEl).val() + "," + $(inputEl).val();
    } else {
        return $(inputEl).val();
    }
}

$(document).ready(function () {
    //Expand all textareas when document is ready
    $("textarea[data-expandable]").each(expandTextArea);

    // Hide the edit tags section on load
    $("#edit-tags").hide();

    // Add a new tag
    $(".add-tag").on("click", addNewTag);

    // Make delete tags deleteable
    $(".delete-tag").each(deleteTag);
});
