/*const entryId = $("#hidden_id").val();
let originalName = $(".entry #name").val();
let originalDescription = $(".entry #description").val();

$(document).ready(function () {
    // Update db when fav checkbox is clicked
    $("#entry-form #is_fav").change(() => {
        let favState;
        $("#entry-form #is_fav").is(":checked")
            ? (favState = true)
            : (favState = false);
        sendData({ is_fav: favState }, "/update_fav/");
    });

    // Update db when name is changed
    // If name does not pass validation, return original name and error message
    $("#entry-form #name").blur(() => {
        let newName = $("#entry-form #name").val();
        sendData({ name: newName }, "/update_name/", "#name-feedback");
    });

    // Update db when description is changed
    // If description does not pass validation, return original name and error message
    $("#entry-form #description").blur(() => {
        let newDescription = $("#entry-form #description").val();
        sendData(
            { description: newDescription },
            "/update_description/",
            "#description-feedback"
        );
    });

    // Update db when rating is changed
    $("#entry-form input[name=rating]:not(:checked)").change(() => {
        let newRating = $("input[name=rating]:checked").val();
        sendData({ rating: newRating }, "/update_rating/", "#rating-feedback");
    });

    // Update db when a new image is chosen
    $("#entry-form #image").change(() => {
        let formData = new FormData($("#entry-form")[0]);
        sendData(formData, "/update_image/", "#image-feedback", true);
    });
});

// Updata tags in db when new tags are saved
function sendTagData() {
    let newTags = $("#hidden_tags").val();
    sendData({ tags: newTags }, "/update_tags/", "#tags-feedback");
}

// Update fields in db
function sendData(fieldData, url, feedbackEl, isImage = false) {
    let ajaxRequest;
    if (isImage) {
        ajaxRequest = {
            data: fieldData,
            type: "POST",
            url: url + entryId,
            contentType: false,
            cache: false,
            processData: false,
        };
    } else {
        ajaxRequest = {
            data: fieldData,
            type: "POST",
            url: url + entryId,
        };
    }
    $.ajax(ajaxRequest).done((data) => {
        if (data.status === "failure") {
            $("#entry-form #name").val(originalName);
            $("#entry-form #description").val(originalDescription);
            $("textarea[data-expandable]").each(expandTextArea);
        } else {
            originalName = $("#entry-form #name").val();
            originalDescription = $("#entry-form #description").val();
            $(".timestamp").text("Last updated on " + data.updated_on);
            if (isImage) {
                $(".entry-image").attr("src", data.new_image);
            }
        }

        newAlert(feedbackEl, data.message, data.message_class);
    });
}

// Create an alert
function newAlert(element, message, type) {
    $(element).removeClass("invalid-update valid-update");
    $(element).show();
    $(element).text(message).addClass(type);
    $(element).delay(3000).slideUp();
}
*/
