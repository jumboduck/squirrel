$(document).ready(function () {
    const entryId = $("#hidden_id").val();

    // Update db when fav checkbox is clicked
    $(".entry #is_fav").change(function () {
        $.ajax({
            type: "POST",
            url: "/update_fav/" + entryId,
        }).done(function (data) {
            $(".timestamp").text("Last updated on " + data.updated_on);
            $("#update-alerts")
                .text(data.success_message)
                .addClass("alert " + data.message_class);
        });
    });
});
