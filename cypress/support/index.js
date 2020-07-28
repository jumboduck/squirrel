import "./commands";

Cypress.Commands.add(
    "login",
    (email = Cypress.env("email"), password = Cypress.env("password")) => {
        cy.visit("/login")

            .get("#email")
            .type(email)

            .get("#password")
            .type(password)

            .get("#submit")
            .click();
    }
);

Cypress.Commands.add("logout", () => {
    cy.visit("/").get("#logout").click();
});

Cypress.Commands.add(
    "addReview",
    (
        content = {
            name: "Test Name",
            description: "Test Description",
            rating: 4,
            fav: true,
            tags: ["tag1", "tag2", "tag3"],
        }
    ) => {
        cy.visit("/add");

        if (content.name) {
            cy.get("#name").type(content.name);
        }

        if (content.description) {
            cy.get("#description").type(content.description);
        }

        if (content.rating || content.rating === 0) {
            cy.get(`label[for="rating-${5 - content.rating}"]`).click();
        }

        if (content.fav) {
            cy.get("#is_fav").click();
        }

        if (content.tags) {
            for (let i = 0; i < content.tags.length; i++) {
                cy.get("#new-tag")
                    .click()
                    .get("#edit-tag-" + (i + 1))
                    .type(content.tags[i]);
            }
        }

        cy.get("#submit").click();
    }
);

Cypress.Commands.add("delete", () => {
    cy.get(".delete-link").click();
});
