![squirrel logo](readme-files/squirrel-readme-logo.png)

# Testing

## Manual Testing

Manual testing was done throughout the development process, as new features were implemented, to ensure of they worked as intended.

### Registration Page

The validation rules for the creation of an account were tested to ensure correct data was sent to the database. The following returned an error as expected:

-   One of the fields missing
-   Confirm password not matching password
-   Username longer than 30 characters
-   Password shorter than 8 characters
-   Invalid email format
-   Email already registered for an existing account

If the fields validate, it was confirmed that an account is created.

If a user is already logged in, accessing the registration page redirects to the listing page.

### Login Page

To log into the application, an email attached to an existing user account must be entered, along with its associated password. If the email is not found in the database, or the password does not match, the login fails.

If the email exists and the password matches, the log in succeeds and the user session is created.

If a user is already logged in, accessing the login page redirects to the listing page.

### About Page

The about page has been accessed while logged in and logged out to ensure to ensure that the paragraph about creating an account displays when the user is logged out.

### New Review Page

The following tests have been done to ensure a review can be added with the appropriate information. All have returned the expected results and feedback:

-   Trying to add a review with empty fields does not add a review
-   A review with a title of 30 characters cannot be added
-   A review with a description over 2000 characters cannot be added
-   Only an image can be added from the file selector in the form
-   A review will not be added if if the rating, title or description are empty

When a review was added, it was ensured that all corresponding fields were appropriately filled in the generated entry page.

Additionally the tagging tool needed testing to ensure data sent to the database was correct.

-   No special characters can be added to a tag
-   When a tag is out of focus, it is changed to a "delete tag", which allows it to be removed
-   Tags created, then deleted with the tagging tool are effectively not added to the database
-   An issue was found where the tags added to the hidden field remained if the form was not validated. This resulted in tags previously inputted to be added to the review without the user's knowledge. it was fixed by clearing the hidden tags field if the form did not validate

### Listing Page

-   It was ensured that entries can be accessed in the listing page by clicking either the image or the title of the corresponding entry
-   Clicking the "delete" button will remove the entry
-   It was ensured that all information for listed entries was correct (title, image, favorite, rating, tags, description, date)
-   As the listing organizes the entries by dated ("created on", or "updated on" if existing), it was ensured that updating an entry, thus changing its update date, pushes it to the top of the listing

#### Tag Listing

Clicking on a tag, either in the listing page or in an entry page will generate a page listing all entry using this tag.

-   It was ensured that tag listing displayed only entries with the relevant tag
-   It was ensured that entering a tag in the url that has not been used in an entry returns a 404 error.

#### Pagination

Thorough tests were conducted to ensure pagination worked as intended, several errors were caught and addressed with the following tests:

-   The page number set in the url (ie: /listing?page=2) was set manually to numbers beyond the range of what the listing includes and leads to a 404 page
-   When the page number is manually changed to a random string, this now leads to the first page of the listing
-   It was ensured that the "previous page" and "next page" buttons exist only when entries would exist to see on the next and previous pages

### Entry Page

It was ensured that all fields of the entries was displayed correctly and showed the appropriate content.

Thorough testing was done to ensure that the entry's content could be updated appropriately. Because these updates are made asynchronously, each test for updates was followed by a page refresh, to ensure that the updates were made on the database side as well as on the frontend.

#### Field Updates

-   It was ensured that the name and description fields could only be updated when validation rules for the field were followed (cannot be blank, cannot start with a space or line break, maximum 30 characters for name and 2000 characters for description)
-   It was ensured an entry could be successfully favorited or unfavorited
-   It was ensured that the rating of an entry could be changed
-   It was ensured that a new image could be uploaded
-   It was ensured that when a new image is uploaded, the previous image is removed from cloudinary
-   It was ensured that tags could be added or removed successfully
-   It was ensured that for each update, the "updated on" text at the bottom of the entry is updated as well
-   For the name, description, and image field, it was ensured that an unsuccessful update returned the appropriate feedback to the user

#### Tag Management

Several issues were discovered when testing the tag management tool in entries:

-   It was ensured that duplicated tags are removed
-   A CSS bug was fixed, where the hover state of tags was not enforced
-   When input tag is blurred, it is removed, causing an error in the console, which is a known issue, see the [following thread on github](https://github.com/jquery/jquery/issues/4417)
-   It was ensured no special characters could be added to tags
-   It was ensured that tags could be added and removed successfully

#### Textarea Resizing

A textarea element's height is fixed by default. To ensure that all text was visible, a javascript function was created to ensure that the textarea field resized to its content

-   Because these fields needed to be edited in their "view", they needed to be resized as a user typed to ensure no content was hidden

-   The textarea also needed to be resized if the size of the window changed, as it could change the text's layout, and pottentially its affect visibility

### Profile

#### Statistics Display

-   It was ensured that the relevant information was appropriately displayed on the profile page
-   A bug was discovered where the average rating was the accounting for reviews across the entire application, not just for the currently logged in user. It was addressed successfully

#### Account Management

The account management tool displays and hides three fields to update chosen by the user

-   Updating only the username was tested successfully
-   Updating the username with over 30 characters did not succeed, as expected
-   Updated only the email was tested successfully
-   Updating the email with a wrongly formatted address did not succeed, as expected
-   Updated only the password was tested successfully
-   Trying to update any of these fields with the wrong current password returned an error as expected
-   Updating all three fields at once was tested successfully

## End-to-End Testing with Cypress

Automated testing was conducted with [Cypress](https://www.cypress.io/).

The tests created cover the [user stories](README.md#user-stories) found in the application's main readme file. This allowed for widespread testing of all primary functionalities of the application whenever significant updates for made, and ensure that these core functionalities worked as expected.

![cypress test video](readme-files/squirrel-cypress-video.gif)

Various commands were created to facilitate the automation process:

-   **login**: log into the application with a test account
-   **logout**: log out of the application
-   **addReview**: create a review
-   **delete**: delete a review

### Login

The following tests were run on the login page:

-   The application should successfully log in with an existing account
-   The application should reject wrong credentials

### Logout

The application should successfully be able to log out of the user's account.

### Add Review Page

The following tests were run on the page to add a new review:

-   A new review should be added when all fields are filled successfully
-   A review should not be added if no name has been typed
-   A review should not be added if no description has been typed
-   A review should not be added if no rating was chosen

### Update Review

The following tests were run to ensure each entry can be updated by the user:

-   It should be possible to update the title
-   It should not be possible to leave the title blank
-   It should be possible to update the description
-   It should not be possible to leave the description blank
-   It should be possible to update the image
-   It should be possible to update the rating
-   It should be possible to add a new tag
-   It should be possible to delete a tag

### Delete Review

It should be possible to delete a review.

### View Entry

From the listing page, the following tests were conducted:

-   It should be possible to access a review by clicking on its title in the listing page
-   It should be possible to access a review by clicking on its image in the listing page

### Search function

The application should successfuly display search results, when a term is sent through the search input in the navigation.

## Responsive Testing

An important feature of the application is to make it responsive across a variety of devices. For this reason thorough testing was conducted to ensure content remained readable and editable on various screen sizes.

The navigation, layout and various functionalities (login, logout, add, view, delete and update reviews) were tested across various screen sizes with chrome developer tools and with the [Responsive Viewer](https://chrome.google.com/webstore/detail/responsive-viewer/inmopeiepgfljkpkidclfgbgbmfcennb) Chrome extension.

These tests were performed on the following devices and browsers:

-   Chrome, Safari and Firefox on Mac OS
-   Chrome and Safari on iPhone XR
-   Chrome and Safari on iPad with Retina display
-   Chrome on Xiaomi Redmi 4A
-   Firefox on Xiaomi Redmi Note 5

A CSS issue was discovered and fixed on displays above 2000px wide, where the width of the tiles made the delete button overlap the date.
