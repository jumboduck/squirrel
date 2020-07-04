const entryId = $("#hidden_id").val();
let originalName = $(".entry #name").val();
let originalDescription = $(".entry #description").val();

$(document).ready(function () {
    // Update db when fav checkbox is clicked
    $(".entry #is_fav").change(() => {
        let favState;
        $(".entry #is_fav").is(":checked")
            ? (favState = true)
            : (favState = false);
        sendData({ is_fav: favState }, "/update_fav/");
    });

    // Update db when name is changed
    // If name does not pass validation, return original name and error message
    $(".entry #name").blur(() => {
        let newName = $(".entry #name").val();
        if (newName.length > 0 && newName.length <= 30) {
            sendData({ name: newName }, "/update_name/", "#name-feedback");
        } else {
            $(".entry #name").val(originalName);
            newAlert(
                "#name-feedback",
                "Name must be between 1 and 30 characters",
                "invalid-update"
            );
        }
    });

    // Update db when description is changed
    // If description does not pass validation, return original name and error message
    $(".entry #description").blur(() => {
        let newDescription = $(".entry #description").val();
        if (newDescription.length > 0 && newDescription.length <= 2000) {
            sendData(
                { description: newDescription },
                "/update_description/",
                "#description-feedback"
            );
        } else {
            $(".entry #description").val(originalDescription);
            $("textarea[data-expandable]").each(expandTextArea);
            newAlert(
                "#description-feedback",
                "Description must be between 1 and 2000 characters",
                "invalid-update"
            );
        }
    });

    // Update db when rating is changed
    $(".entry input[name=rating]:not(:checked)").change(() => {
        let newRating = $("input[name=rating]:checked").val();
        sendData({ rating: newRating }, "/update_rating/", "#rating-feedback");
    });

    // Update db when a new image is chosen
    $("#image").change(() => {
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
            $("#update-alerts")
                .text(data.success_message)
                .addClass("alert " + data.message_class);
        });
    });
});

// Updata tags in db when new tags are saved
function sendTagData() {
    let newTags = $("#hidden_tags").val();
    sendData({ tags: newTags }, "/update_tags/");
}

// Update fields in db
function sendData(fieldData, url, feedbackEl) {
    $.ajax({
        data: fieldData,
        type: "POST",
        url: url + entryId,
    }).done((data) => {
        $(".timestamp").text("Last updated on " + data.updated_on);
        newAlert(feedbackEl, data.success_message, data.message_class);
    });
}

// Create an alert
function newAlert(element, message, type) {
    $(element).removeClass("invalid-update valid-update");
    $(element).text(message).addClass(type);
}
