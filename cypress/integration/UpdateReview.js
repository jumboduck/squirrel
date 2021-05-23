describe("Update entry", () => {
    before(() => cy.login().addReview());
    beforeEach(() => Cypress.Cookies.preserveOnce("session"));

    it("should be possible to update the title", () => {
        cy.get("#name").type(" update").blur();
        cy.get("#name-feedback")
            .should("be.visible")
            .should("have.class", "valid-update");
    });

    it("should not be possible to leave the title blank", () => {
        cy.get("#name").clear().blur();
        cy.get("#name-feedback")
            .should("be.visible")
            .should("have.class", "invalid-update");
    });

    it("should be possible to update the description", () => {
        cy.get("#description").type(" update").blur();
        cy.get("#description-feedback")
            .should("be.visible")
            .should("have.class", "valid-update");
    });

    it("should be possible to update the image", () => {
        cy.get("input[type=file]").attachFile("acorn-test-image.jpg");

        cy.get("#image-feedback")
            .should("be.visible")
            .should("have.class", "valid-update");
    });

    it("should not be possible to leave the description blank", () => {
        cy.get("#description").clear().blur();
        cy.get("#description-feedback")
            .should("be.visible")
            .should("have.class", "invalid-update");
    });

    it("should be possible to update the rating", () => {
        cy.get('label[for="rating-0"]').click();
        cy.get("#rating-feedback")
            .should("be.visible")
            .should("have.class", "valid-update");
    });

    it("should be possible to add a new tag", () => {
        cy.get("#edit-tags-btn")
            .click()
            .get("#new-tag")
            .click()
            .type("another tag")
            .get("#save-tag-btn")
            .click();
        cy.get("#tags-feedback")
            .should("be.visible")
            .should("have.class", "valid-update");
        cy.get(".view-tag").should("have.length", 4);
    });

    it("should be possible to delete a tag", () => {
        cy.get("#edit-tags-btn")
            .click()
            .get(".delete-tag:first")
            .click()
            .get("#save-tag-btn")
            .click();
        cy.get("#tags-feedback")
            .should("be.visible")
            .should("have.class", "valid-update");
        cy.get(".view-tag").should("have.length", 3);
    });

    after(() => cy.delete().logout());
});
