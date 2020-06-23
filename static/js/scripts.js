// Textarea expandable inspired by Vanderson https://codepen.io/Vanderson
function expandTextArea() {
    this.style.removeProperty("height");
    this.style.height = this.scrollHeight + 2 + "px";
}

$("body")
    .on("keydown input", "textarea[data-expandable]", expandTextArea)
    .on("mousedown focus", "textarea[data-expandable]", expandTextArea);

$(window).resize(function () {
    $("textarea[data-expandable]").each(expandTextArea);
});

//Create/Edit/Delete tags in entries

$("#edit-tags-btn").on("click", function () {
    $("#edit-tags").toggle();
    $("#view-tags").toggle();
});

$("#save-tag-btn").on("click", function () {
    $("#edit-tags").toggle();
    $("#view-tags").toggle();
});

function deleteTag() {
    $(this).click(function () {
        $(this).remove();
    });
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
});
