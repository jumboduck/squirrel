![squirrel logo](readme-files/squirrel-readme-logo.png)

Squirrel is an application that allows users to log reviews and ratings of products, places, restaurants, movies, songs, or anything they would wish to keep track of.
It is not meant to be a social application, but a repository of likes and dislikes for the user's future reference. Each entry can be tagged and starred to be made easily searchable, and also updated or deleted.

It has been deployed to heroku and can be viewed [here](https://squirrel-logbook.herokuapp.com/).

## UX

The user's experience was at the front and center during the development of this project.

### User Stories

-   As a user, I want to review a product, so that I can remember what I thought of it at a future date.
-   As a shopper, I want to find a previously reviewed product, so that I can make a shopping decision.
-   As a user, I want to update a review, if my opinion of it has changed.
-   As a user, I want to be able to delete a review, if it is not longer relevant
-   As a beer enthusiast, I want to be able to search through the beers I have consumed, so that I can see what I have tried.
-   As a consumer, I want to be able to categorize my entries, so that I can see results at a glance.
-   As a user, I want to be able to edit the categories in my reviews, so that I can reorganize my repository.
-   As a user, I want to search through entries I have created, to find a specific item.
-   As a user, I want to be able to upload images of what I review, so that I can look at them later
-   As a user, I want to be able to read through my reviews on a mobile device, so that I can access the information in a store.

### Wireframes

## Features

### Existing Features

-   New users can register for a new account
-   Existing users can log in and out of their account
-   This application allows users to create, retrieve, edit and delete reviews connected to their personal account.
-   Reviews can be favorited.
-   Reviews can be searched by keyword, in the entries' name, description and tag fields.
-   Users can upload an image to each review with the cloudinary API.
-   Updating an entry happens seamlessly on the entry's page, without loading a separate update page.

### Features Left to Implement

-   A password recovery system, that would send an email to a user's account, needs to be implemented.
-   The profile page should be expanded to display more information, such as the most used tags and the best rated reviews.
-   The listing page should be expanded to allow to view all favorited items.

## Technologies Used

-   HTML
-   CSS
-   Bootstrap
-   JavaScript / JQuery
-   AJAX
-   Python
-   Flask
-   [The Padwan Project](https://github.com/Eventyret/Padawan)
-   [Cloudinary](https://cloudinary.com/)
-   [Cypress](https://www.cypress.io/) for testing throughout the development process
-   [Material Icons](https://material.io/) for all icons on the site
-   [CSS Autoprefixer](https://autoprefixer.github.io/)

## Testing

### Manual Testing

#### Pagination on Listing page

Thorough conducted to ensure pagination worked as intended, several errors were caught and addressed with the following tests:

-   The page number set in the url (/listing?page=2) was set manually to numbers beyond the range of what the listing includes and leads to a 404 page
-   The page number was manually changed to a string

#### Tag Management

-   Issue with hover CSS of tags not working
-   Issue with tags in adding review: when field is not validated, the variables in the hidden field remain
-   When input tag is blurred, it is removed, causing an error in the console, see: https://github.com/jquery/jquery/issues/4417

#### Textarea resizing

-   Textarea is fixed, needed to find a way to resize it to look natural

### Testing with Cypress

## Deployment

## Credits

### Content

### Media

-   Acorn logo from [Flaticon](https://www.flaticon.com/authors/freepik)

### Acknowledgements

-   Inspiration for this project came from conversations with my friend Cameron.
-   [Simen Daehlin](https://github.com/Eventyret) - [The Padwan Project](https://github.com/Eventyret/Padawan)
-   [Start Bootstrap Resume Template](https://github.com/StartBootstrap/startbootstrap-resume)
-   [Corey Schaefer](https://www.youtube.com/channel/UCCezIgC97PvUuR4_gbFUs5g) for his python tutorials on youtube, especially regarding registration and login forms.
-   [Adam Orchard](https://codepen.io/orchard/pen/Jnwvb) for the 5 star rating code.
-   [Andy Osborne](https://github.com/Andy-Osborne) for helping with the search functionality
