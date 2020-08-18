![squirrel logo](readme-files/squirrel-readme-logo.png)

# Testing

## Manual Testing

Manual testing was done throughout the development process, as new features were implemented, to ensure of they worked as intended.

### Registration Page

### Login Page

### New Review Page

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
