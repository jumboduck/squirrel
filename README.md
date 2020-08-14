![squirrel logo](readme-files/squirrel-readme-logo.png)

Squirrel is an application that allows users to log reviews and ratings of products, places, restaurants, movies, songs, or anything they would wish to keep track of.
It is not meant to be a social application, but a repository of likes and dislikes for the user's future reference. Each entry can be tagged and starred to be made easily searchable, and also updated or deleted.

![squirrel responsive displays](readme-files/squirrel-responsive-displays.png)

It has been deployed to heroku and can be viewed [here](https://squirrel-logbook.herokuapp.com/).

## UX

### Project Goal

The user's experience was at the front and center during the development of this project. One of the goals of the project was to create an application that is intuitive and satisfying to use. For this reason, Squirrel was built to be usable across all screen sizes,

Starting from user stories, some initial wireframes were sketched out, as well as the application's data structure.

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

Following these user stories, wireframes were drawn to provide a starting point and guidance throughout the development process. The full wireframes can be found [here](readme-files/squirrel-wireframes.pdf).

![squirrel wireframe](readme-files/squirrel-wireframe-shot.png)

The final design of the application departed from the original wireframe in slight ways:

-   The navigation moved from the top to the right hand side of the window on medium screen sizes and higher.
-   The page listing all reviews was made using bootstrap cards to make it more aesthetically pleasing.
-   The search was made a single text input in the navigation instead of a page of its own, to make it more accessible

### Views and Data Structure

Before starting the development of squirrel, its database's structure was delineated:

![data structure](readme-files/squirrel_data_structure.png)

Each of the applications views and the actions that could be taken by the user were defined. These would later help decide which routes would need to be created with Flask. It was decided early on in this process that the "read" and "update" views for entries would be one and the same.

![views and actions](readme-files/squirrel-views.png)

Data validation was also decided early in this process for any data that could be inputted by the user.

![data validation](readme-files/squirrel_data_validation.png)

These elements remained roughly the same throughout the application's development, however some adjustments had to be made along the way. A few notable updates:

-   An image_id field was added to each entry to allow its deletion from cloudinary if the entry is deleted
-   The score field for each entry became a rating from 1 to 5
-   Some additional views were created for user registration and search results

### Design

The application was built using bootstrap and its responsive grid system. The [Start Bootstrap Resume Template](https://github.com/StartBootstrap/startbootstrap-resume) was used for the main structure of the site, and its default styling was overriden by a [style.css](static/css/style.css) file.

Fonts and colors were carefully chosen to give the application a distinctive brand and feel.

#### Typography

Three fonts are used throughout the site:

1. **Poiret One** for the logo

    > ![poiret one example](readme-files/squirrel-poiret-one.png)

2. **Montserrat** for titles, this font is used exclusively in uppercase

    > ![montserrat example](readme-files/squirrel-montserrat.png)

3. **Raleway** for textual content such as paragraphs, tags, and navigation links
    > ![raleway example](readme-files/squirrel-raleway.png) ![raleway example with tags](readme-files/squirrel-raleway-tags.png)

The marriage of these three fonts blends elegance and readability across the site.

#### Color Scheme

A simple color scheme was used to accentuate readability and usability.

-   ![#535F6B](https://placehold.it/15/535F6B/000000?text=+) `#535F6B - navy blue, primary color`

This color is used in the navigation, and is echoed throughout the site, in various buttons and links.
It was initially a lighter shade of blue, but was darkened to create a stronger contrast with the text in the navigation, for accessibility and readability purposes.

-   ![#A99279](https://placehold.it/15/a99279/000000?text=+) `#A99279 - light brown, secondary color`

The light brown is an accent found throughout the application. It highlights links and buttons that the user can interact, such as links to entries, tag buttons, the search button, etc...

-   ![#FF69B4](https://placehold.it/15/FF69B4/000000?text=+) `#FF69B4 - pink, favorite color`

This color is used exclusively to color the heart representing favorited reviews. It was chosen to stick out, so that these reviews can be easily seen in a list.

-   ![#FFAA1D](https://placehold.it/15/FFAA1D/000000?text=+) `#FFAA1D - yellow, rating color`

Similar to the favorite color, this yellow is used exclusively for the star ratings. It was also chosen to be easily identifiable at a glance.

-   ![#F5F5F5](https://placehold.it/15/F5F5F5/000000?text=+) `#F5F5F5 - off white, background color`

This off white was chosen for the background color for the site as it provides good contrast with the other chosen colors, but is less aggressive than a plain white.

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
