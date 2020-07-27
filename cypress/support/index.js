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
