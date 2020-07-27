import "./commands";

Cypress.Commands.add("login", (email, password) => {
    cy.visit("/login")

        .get("#email")
        .type(email)

        .get("#password")
        .type(password)

        .get("#submit")
        .click();
});

Cypress.Commands.add("logout", () => {
    cy.visit("/").get("#logout").click();
});

Cypress.Commands.add("addReview", (name, description, rating, fav, tags) => {
    cy.visit("/add")
        .get("#name")
        .type(name)

        .get("#description")
        .type(description)

        .get(`label[for="rating-${rating - 1}"]`)
        .click();

    if (fav) {
        cy.get("#is_fav").click();
    }

    if (tags) {
        for (let i = 0; i < tags.length; i++) {
            cy.get("#new-tag")
                .click()
                .get("#edit-tag-" + (i + 1))
                .type(tags[i]);
        }
    }

    cy.get("#submit").click();
});
