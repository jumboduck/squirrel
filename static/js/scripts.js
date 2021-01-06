/**
 * TAG MANAGEMENT
 * ==============
 * The following code holds variables, functions, and event listeners that
 * manage the tag functionality in review pages and in the "New Review" page.
 *
 * In the review pages, the tags are initially displayed as "view tags", which link
 * to a listing of all reviews tagged with the keyword.
 * Each "view tag" has a corresponding "delete tag", which is initially hidden. When
 * clicked, a delete tag will remove itself and its corresponding "view tag".
 *
 * Cliking the "edit tags" button, will hide "view tags" and reveal "delete tags".
 *
 * When editing tags, a new tag can be created by clicking the "new tag" button.
 * This will generate an "tag input", which is a text input field, and allows the
 * user to add new tags.
 *
 * Clicking the "save tags" button will send the newly created tags to the backend,
 * to be validated and to update the database. It will also toggle the "view tags"
 * and "delete tags".
 *
 * This functionality is similar when creating a new review, with the exception that
 * the "view tags" are not generated. The user will only be working with "tag inputs"
 * and "delete tags".
 */

/**
 * The tagNum variable counts the number of tags in an entry
 * This is used to give an ID number to dynamically generated tags.
 * */
let tagNum = $(".view-tag").length;

/**
 * The urlBase variable checks if the page is in the listing or the playground
 */
let urlBase = $("#url-builder").text();

/**
 * This function takes the id of a tag, and extracts the number at the end.
 *
 * @param {string} id The id of tag
 * @returns {number} The number in the id tag
 */
function getNumberFromId(id) {
    return id.match(/\d+/g)[0];
}

/**
 * This function adds the tag created by the user to the hidden input field, separated by
 * a comma.
 * If no content is present in the field, it simply adds the content of the new tag.
 * The hidden field will thus contain a list of all tags for the entry, separated
 * by commas.
 *
 * @param {string} tag The tag inputted by the user
 * @returns {string} A string representing all tags separated by commas
 */
function addToHiddenInput(tag) {
    if ($("#hidden_tags").val() != "") {
        return $("#hidden_tags").val() + "," + tag;
    } else {
        return tag;
    }
}

/**
 * The following function generates the code for a new "view tag" on an entry page.
 *
 * @param {string} id The id of the newly created tag
 * @param {string} word The content of the newly created tag
 * @returns {string} The HTML for the newly created tag
 */
function createTag(id, word = "New Tag") {
    return `<a id="${id}" class="view-tag badge badge-pill badge-primary tag" href="${urlBase}${word}">${word}</a>`;
}

/**
 * This function generates the code to create a new "delete tag" on an entry page, or on
 * the "Add Review" page.
 *
 * @param {string} id The id of the newly created delete tag
 * @param {string} word The content of the newly created delete tag
 * @returns {string} The HTML for the newly created delete tag
 */
function createDeleteTag(id, word) {
    return `<button id="${id}" class="badge badge-pill badge-primary tag delete-tag">${word}
    <span class="material-icons">cancel</span></button>`;
}

/**
 * This function removes a "view tag" and its corresponding "delete tag" from the DOM,
 * when the "delete tag" is clicked.
 * It also gets the string of tags in the #hidden_tags field, makes it an array to
 * remove the deleted tag from it, and rebuilds the string of tags separated by commas.
 */
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

/**
 * This function creates a new tag and its corresponding delete tag.
 * An input field is generated, along with its label, created for
 * It also creates a corresponding width machine, which is a span containing the content
 * of the new tag, used solely for the purpose of defining the width of the tag as the
 * input is being typed into.
 *
 * It also puts the browser's focus onto the newly created tag input.
 *
 * Finally it increments tagNum.
 */
function addNewTag() {
    // Create IDs for new elements to be generated
    tagNum += 1;
    let editTagId = "edit-tag-" + tagNum;
    let viewTagId = "tag" + tagNum;
    let labelId = "label" + tagNum;
    let widthMachineId = "width" + tagNum;

    // Generate HTML for new tag input, new "view tag", and new "width machine"
    let newEditTag = `<label for="${editTagId}" id="${labelId}" class="sr-only">New tag</label><input id="${editTagId}" type="text" maxlength="20" placeholder="new tag" spellcheck="false" class="tag badge-pill badge-primary badge-input" />`;
    let newTag = createTag(viewTagId);
    let newWidthMachine = `<span aria-hidden="true" id="${widthMachineId}"class="badge badge-pill badge-primary tag width-machine">invisible</span>`;

    // Append newly created HTML to DOM and focus on the new input
    $(this).before(newEditTag);
    $("#" + editTagId).focus();
    $("#view-tags").append(newTag);
    $(".entry").append(newWidthMachine);
}

/**
 * This function ensures that when an element's view is toggled,
 * its aria-expanded and aria-hidden attributes are updated as well for
 * accessibility purposes.
 *
 * @param {string} field The jQuery selector of the element to be toggled
 */
function toggleAria(field) {
    $(field).toggle();
    $(field).attr("aria-expanded", function (i, attr) {
        return attr === "true" ? "false" : "true";
    });
    $(field).attr("aria-hidden", function (i, attr) {
        return attr === "true" ? "false" : "true";
    });
}
/**
 * The following toggles the "view tags" and "delete tags" from hidden
 * to visible and vice versa.
 */
function toggleViewTags() {
    toggleAria("#edit-tags");
    toggleAria("#view-tags-container");
}

/**
 * This event handler checks for keystrokes in the tag inputs, and updates the
 * content and url of the corresponding "view tag" accordingly.
 * The content of the corresponding "width machine" span is also updated, and its
 * new width is used to update the width of the input.
 *
 * This event is attached to the document because the inputs are dynamically
 * generated.
 */
$(document).on("keydown input", ".badge-input", function () {
    let viewId = "#tag" + getNumberFromId($(this).attr("id"));
    let widthId = "#width" + getNumberFromId($(this).attr("id"));
    // Update name of "view tag"
    $(viewId).text($(this).val());
    // Update url of "view tag"
    $(viewId).attr("href", urlBase + $(this).val());
    // Update width machine and width of "view tag"
    $(widthId).text($(this).val());
    $(this).width($(widthId).width());
});

/**
 * The following event ensures that pressing the "enter" key
 * while the name field or a tag input field are in focus does
 * not submit the form, but instead removes focus from the element.
 */
$(document).on("keypress", "#name, .badge-input", function (event) {
    if (event.keyCode === 13) {
        $(this)[0].blur();
        event.preventDefault();
    }
});

/**
 * When a "tag input" is blurred, it is removed and replaced with a delete tag.
 * Its label, used for screen readers, is also removed.
 * If the input is blurred while empty, it is simply removed.
 *
 * This event is attached to the document because the inputs are dynamically
 * generated.
 */
$(document).on("blur", ".badge-input", function () {
    let tagNumber = getNumberFromId($(this).attr("id"));
    if (!$(this).val()) {
        $("#tag" + tagNumber).remove();
    } else {
        let newTagContent = addToHiddenInput($(this).val());
        let newDeleteTag = createDeleteTag($(this).attr("id"), $(this).val());
        $("#hidden_tags").val(newTagContent);
        $("#new-tag").before(newDeleteTag);
        $(".delete-tag").each(deleteTag);
    }
    $("#label" + tagNumber).remove();
    $(this).remove();
});

/**
 * When the "edit tags" button is clicked, hide the "view tags"
 * and display the "delete tags".
 */
$("#edit-tags-btn").on("click", toggleViewTags);

/**
 * When the "add tag" button is clicked, a new tag input is created
 */
$(".add-tag").on("click", addNewTag);

/**
 * When the "save tags" button is clicked while editing the tags, the new
 * tag information is sent to the backend to update the database, the width
 * machines are removed, and the "delete tags" and "view tags" are toggled
 */
$(document).on("click", "#save-tag-btn", function () {
    // Send new tag information to the database
    let newTags = $("#hidden_tags").val();
    sendData({ tags: newTags }, "/update_tags/", "#tags-feedback");
    // Remove element used to resize tag inputs
    $(".width-machine").each(function () {
        $(this).remove();
    });
    toggleViewTags();
});

/**
 * The following only allows specific keystrokes in tag input fields,
 * whether in an entry page or when adding a new entry.
 * This code is inspired by the following conversation on Stack Overflow:
 * https://stackoverflow.com/questions/43799032/allow-only-alphanumeric-in-textbox-using-jquery
 */
$(document).on("keydown", ".badge-input", (e) => {
    let k = e.keyCode || e.which;
    let ok =
        (k >= 65 && k <= 90) || // A-Z
        (k >= 96 && k <= 105) || // a-z
        (k >= 35 && k <= 40) || // arrows
        k === 46 || //del
        k === 13 || //enter
        k === 8 || // backspaces
        k === 32 || // space
        k === 9 || //tab
        (!e.shiftKey && k >= 48 && k <= 57); // only 0-9 (ignore SHIFT options)
    if (!ok || (e.ctrlKey && e.altKey)) {
        e.preventDefault();
    }
});

/**
 * UPDATE ENTRY
 * ============
 * The following code holds variables, functions and event handlers to
 * manage the updates of various fields to the database.
 * These updates are made via AJAX requests to the backend, so that changes
 * to entries can be made without reloading the page.
 */

/**
 * The id of the entry is saved in a hidden field to let the application
 * know which entry to update. The backend will verify that this entry
 * belongs to the logged in user.
 */
const entryId = $("#hidden_id").val();

/**
 * The original name and description of the entry are saved so that they
 * can be reverted to if the fields do not validate.
 */
let originalName = $(".entry #name").val();
let originalDescription = $(".entry #description").val();

/**
 * This function sends data to the backend to update the database.
 * If the request fails, it will revert name and description to their original values.
 * If the request succeeds, the database has updated,update the timestamp, and if
 * the request was to update the image, the image will change.
 *
 * Finally a message is displayed to let the user know if the update has succeeded or not.
 *
 * @param {Object} fieldData The data to be sent to the backend to update the database
 * @param {string} url The url that will process the request
 * @param {string} feedbackEl The jQuery selector of the element that will display feedback for the request
 * @param {boolean} isImage Determines whether the request is for an image or not, as this will require a different
 * AJAX request.
 */
function sendData(fieldData, url, feedbackEl, isImage = false) {
    let ajaxRequest = {
        data: fieldData,
        type: "POST",
        url: url + entryId,
    };
    // Change format of ajax request if it is for an image
    if (isImage) {
        ajaxRequest = {
            data: fieldData,
            type: "POST",
            url: url + entryId,
            contentType: false,
            cache: false,
            processData: false,
        };
    }
    $.ajax(ajaxRequest).done((data) => {
        if (data.status === "failure") {
            // If update was a failure, revert Name and Description
            $("#entry-form #name").val(originalName);
            $("#entry-form #description").val(originalDescription);
            $("textarea[data-expandable]").each(expandTextArea);
        } else {
            // If update was successful, update timestamp
            // and original name and description, if another update
            // if made.
            originalName = $("#entry-form #name").val();
            originalDescription = $("#entry-form #description").val();
            $(".timestamp").text("Last updated on " + data.updated_on);
            if (isImage) {
                // If update was for an image, update the image
                $(".entry-image").attr("src", data.new_image);
            }
        }

        newAlert(feedbackEl, data.message, data.message_class);
    });
}

/**
 * This function creates an alert after a user tries to update a field, either successfully or
 * unsuccessfully.
 *
 * @param {string} element The jQuery selector for the HTML element that displays the message
 * @param {string} message The content of the message
 * @param {string} type The CSS class of the message, it will be either "valid-update" or "invalid-update"
 */
function newAlert(element, message, type) {
    $(element).removeClass("invalid-update valid-update");
    $(element).show();
    $(element).text(message).addClass(type);
    $(element).delay(3000).slideUp();
}

/**
 * Send data to the backend to update the favorite status of the entry,
 * when the checkbox is clicked.
 */
$("#entry-form #is_fav").change(() => {
    let favState;
    $("#entry-form #is_fav").is(":checked")
        ? (favState = true)
        : (favState = false);
    sendData({ is_fav: favState }, "/update_fav/");
});

/**
 * Send data to the database to update the name of the entry,
 * when the name field is blurred.
 */
$("#entry-form #name").blur(() => {
    let newName = $("#entry-form #name").val();
    sendData({ name: newName }, "/update_name/", "#name-feedback");
});

/**
 * Send data to the backend to update the description of the entry,
 * when the description field is blurred.
 */
$("#entry-form #description").blur(() => {
    let newDescription = $("#entry-form #description").val();
    sendData(
        { description: newDescription },
        "/update_description/",
        "#description-feedback"
    );
});

/**
 * Send data to the backend to update the rating of the entry,
 * when a new rating is chosen by the user.
 */
$("#entry-form input[name=rating]:not(:checked)").change(() => {
    let newRating = $("input[name=rating]:checked").val();
    sendData({ rating: newRating }, "/update_rating/", "#rating-feedback");
});

/**
 * Send data to the backend to update the image of the entry,
 * when a new image is selected by the user.
 */
$("#entry-form #image").change(() => {
    let formData = new FormData($("#entry-form")[0]);
    sendData(formData, "/update_image/", "#image-feedback", true);
});

/**
 * UTILITIES
 * =========
 * The following functions are various utilities used throughout the application.
 *
 * First are functions and event handlers to manage the dynamic reizing of textarea
 * elements.
 *
 * Second are functions and event handlers that handle the account management section
 * of the user profile.
 *
 * Finally some code to enable specific bootstrap functionalities.
 */

/**
 * This function expands textarea input fields to fit their content content automatically.
 * It is inspired inspired by Vanderson https://codepen.io/Vanderson
 */
function expandTextArea() {
    this.style.removeProperty("height");
    this.style.height = this.scrollHeight + 2 + "px";
}

/**
 * The textarea fields that have the data-expandable attribute are able to expand to fit their
 * content when keys are pressed or the input is clicked into.
 */
$(document)
    .on("keydown input", "textarea[data-expandable]", expandTextArea)
    .on("mousedown", "textarea[data-expandable]", expandTextArea);

/**
 * Expandable text areas will resize when window is resized.
 * This ensures that text does not disappear when the window is made smaller.
 */
$(window).resize(function () {
    $("textarea[data-expandable]").each(expandTextArea);
});

/**
 * The following code shows and hides the fields to update account information
 * on the user's Profile page. It changes the appearance and icon of the buttons
 * used to toggle these fields.
 * It also alters the "aria-expanded" and "aria-hidden" properties for
 * accessibility purposes.
 *
 * @param {string} field The jQuery selector of the field to toggle
 */
function toggleField(field) {
    toggleAria(field);
    $(this).toggleClass("selected");
    $(this).find(".icon").text() === "edit"
        ? $(this).find(".icon").text("close")
        : $(this).find(".icon").text("edit");
}

/**
 * The following event listeners toggle the various account fields
 * on and off to be edited.
 */
$("#update-username-btn").click(function () {
    toggleField.call(this, "#update-username");
});
$("#update-email-btn").click(function () {
    toggleField.call(this, "#update-email");
});
$("#update-password-btn").click(function () {
    toggleField.call(this, "#update-password");
});

$(document).ready(function () {
    //Expand all textareas in entry pages when document is ready
    $("textarea[data-expandable]").each(expandTextArea);

    // Hide the edit tags on entry pages
    $("#edit-tags").hide();

    // Make delete tags deleteable
    $(".delete-tag").each(deleteTag);

    // Hide fields to update user account
    $("#update-username").hide();
    $("#update-email").hide();
    $("#update-password").hide();
});

// In new entry form, changes file input text when a new file is chosen
$(".custom-file-input").change((e) => {
    let fileName = e.target.files[0].name;
    $(".custom-file-label").text(fileName);
});

// Initialize bootstrap tooltips
$("[data-toggle=tooltip]").tooltip();
