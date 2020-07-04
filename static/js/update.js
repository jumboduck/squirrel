const entryId = $("#hidden_id").val();

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
    $(".entry #name").blur(() => {
        let newName = $(".entry #name").val();
        sendData({ name: newName }, "/update_name/");
    });

    // Update db when description is changed
    $(".entry #description").blur(() => {
        let newDescription = $(".entry #description").val();
        sendData({ description: newDescription }, "/update_description/");
    });

    // Update db when rating is changed
    $(".entry input[name=rating]:not(:checked)").change(() => {
        let newRating = $("input[name=rating]:checked").val();
        sendData({ rating: newRating }, "/update_rating/");
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
function sendData(fieldData, url) {
    $.ajax({
        data: fieldData,
        type: "POST",
        url: url + entryId,
    }).done((data) => {
        $(".timestamp").text("Last updated on " + data.updated_on);
        $("#update-alerts")
            .text(data.success_message)
            .addClass("alert " + data.message_class);
    });
}
