const entryId = $("#hidden_id").val();
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
        //if (newName.length > 0 && newName.length <= 30) {
        sendData({ name: newName }, "/update_name/", "#name-feedback");
        /*} else {
            $("#entry-form #name").val(originalName);
            newAlert(
                "#name-feedback",
                "Name must be between 1 and 30 characters",
                "invalid-update"
            );
        }*/
    });

    // Update db when description is changed
    // If description does not pass validation, return original name and error message
    $("#entry-form #description").blur(() => {
        let newDescription = $("#entry-form #description").val();
        if (newDescription.length > 0 && newDescription.length <= 2000) {
            sendData(
                { description: newDescription },
                "/update_description/",
                "#description-feedback"
            );
            originalDescription = newDescription;
        } else {
            $("#entry-form #description").val(originalDescription);
            $("textarea[data-expandable]").each(expandTextArea);
            newAlert(
                "#description-feedback",
                "Description must be between 1 and 2000 characters",
                "invalid-update"
            );
        }
    });

    // Update db when rating is changed
    $("#entry-form input[name=rating]:not(:checked)").change(() => {
        let newRating = $("input[name=rating]:checked").val();
        sendData({ rating: newRating }, "/update_rating/", "#rating-feedback");
    });

    // Update db when a new image is chosen
    $("#entry-form #image").change(() => {
        let form_data = new FormData($("#entry-form")[0]);
        $.ajax({
            data: form_data,
            type: "POST",
            url: "/update_image/" + entryId,
            contentType: false,
            cache: false,
            processData: false,
        }).done((data) => {
            $(".entry-image").attr("src", data.new_image);
            $(".timestamp").text("Last updated on " + data.updated_on);
            newAlert(
                "#image-feedback",
                data.success_message,
                data.message_class
            );
        });
    });
});

// Updata tags in db when new tags are saved
function sendTagData() {
    let newTags = $("#hidden_tags").val();
    sendData({ tags: newTags }, "/update_tags/", "#tags-feedback");
}

// Update fields in db
function sendData(fieldData, url, feedbackEl) {
    $.ajax({
        data: fieldData,
        type: "POST",
        url: url + entryId,
    }).done((data) => {
        if (data.status === "failure") {
            $("#entry-form #name").val(originalName);
        } else {
            originalName = $("#entry-form #name").val();
            $(".timestamp").text("Last updated on " + data.updated_on);
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
