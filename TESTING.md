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

### Login Page

To log into the application, an email attached to an existing user account must be entered, along with its associated password. If the email is not found in the database, or the password does not match, the login fails.

If the email exists and the password matches, the log in succeeds and the user session is created.

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

### Listing Page

#### Pagination

Thorough tests were conducted to ensure pagination worked as intended, several errors were caught and addressed with the following tests:

-   The page number set in the url (ie: /listing?page=2) was set manually to numbers beyond the range of what the listing includes and leads to a 404 page
-   The page number was manually changed to a random string, this now leads to the first page of the listing

### Entry Page

#### Tag Management

-   Issue with hover CSS of tags not working
-   Issue with tags in adding review: when field is not validated, the variables in the hidden field remain
-   When input tag is blurred, it is removed, causing an error in the console, see: https://github.com/jquery/jquery/issues/4417

#### Textarea Resizing

-   A textarea's height is fixed by default. To ensure that all text was visible, a javascript function was created to ensure that the textarea field resized to its content.

-   Because these fields needed to be edited in their "view", they needed to be resized as a user typed to ensure no content was hidden.

-   The textarea also needed to be resized if the size of the window changed, as it could change the text's layout, and pottentially its affect visibility.

### Profile

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
