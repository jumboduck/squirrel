// Textarea expandable inspired by Vanderson https://codepen.io/Vanderson

function expandTextArea() {
    this.style.removeProperty("height");
    this.style.height = this.scrollHeight + 2 + "px";
}

$("body")
    .on("keydown input", "textarea[data-expandable]", expandTextArea)
    .on("mousedown focus", "textarea[data-expandable]", expandTextArea);

$(document).ready(function () {
    $("textarea[data-expandable]").each(expandTextArea);
});

$(window).resize(function () {
    $("textarea[data-expandable]").each(expandTextArea);
});

// Prevent line breaks in entry names
$(document).ready(function () {
    $("#review-name").keypress(function (event) {
        if (event.which == "13") {
            return false;
        }
    });
});
