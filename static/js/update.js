$(document).ready(function () {
    const entryId = $("#hidden_id").val();

    // Update db when fav checkbox is clicked
    $(".entry #is_fav").change(() => {
        let favState;
        $(".entry #is_fav").is(":checked")
            ? (favState = true)
            : (favState = false);
        $.ajax({
            data: { is_fav: favState },
            type: "POST",
            url: "/update_fav/" + entryId,
        }).done((data) => {
            $(".timestamp").text("Last updated on " + data.updated_on);
            $("#update-alerts")
                .text(data.success_message)
                .addClass("alert " + data.message_class);
        });
    });

    // Update db when name is changed
    $(".entry #name").blur(() => {
        $.ajax({
            data: { name: $(".entry #name").val() },
            type: "POST",
            url: "/update_name/" + entryId,
        }).done((data) => {
            $(".timestamp").text("Last updated on " + data.updated_on);
            $("#update-alerts")
                .text(data.success_message)
                .addClass("alert " + data.message_class);
        });
    });

    // Update db when description is changed
    $(".entry #description").blur(() => {
        $.ajax({
            data: { description: $(".entry #description").val() },
            type: "POST",
            url: "/update_description/" + entryId,
        }).done((data) => {
            $(".timestamp").text("Last updated on " + data.updated_on);
            $("#update-alerts")
                .text(data.success_message)
                .addClass("alert " + data.message_class);
        });
    });

    // Update db when rating is changed
    $(".entry input[name=rating]:not(:checked)").change(() => {
        $.ajax({
            data: { rating: $("input[name=rating]:checked").val() },
            type: "POST",
            url: "/update_rating/" + entryId,
        }).done((data) => {
            $(".timestamp").text("Last updated on " + data.updated_on);
            $("#update-alerts")
                .text(data.success_message)
                .addClass("alert " + data.message_class);
        });
    });
});
