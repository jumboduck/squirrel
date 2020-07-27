describe("Update entry", () => {
    it("should be possible to update the title", () => {
        cy.login().addReview().get("#name").type(" update").blur();
        cy.get("#name-feedback")
            .should("be.visible")
            .should("have.class", "valid-update");
        cy.delete();
    });

    it("should not be possible to leave the title blank", () => {
        cy.login().addReview().get("#name").clear().blur();
        cy.get("#name-feedback")
            .should("be.visible")
            .should("have.class", "invalid-update");
        cy.delete();
    });

    it("should be possible to update the description", () => {
        cy.login().addReview().get("#description").type(" update").blur();
        cy.get("#description-feedback")
            .should("be.visible")
            .should("have.class", "valid-update");
        cy.delete();
    });

    it("should not be possible to leave the description blank", () => {
        cy.login().addReview().get("#description").clear().blur();
        cy.get("#description-feedback")
            .should("be.visible")
            .should("have.class", "invalid-update");
        cy.delete();
    });

    it("should be possible to update the rating", () => {
        cy.login().addReview().get('label[for="rating-0"]').click();
        cy.get("#rating-feedback")
            .should("be.visible")
            .should("have.class", "valid-update");
        cy.delete();
    });

    it("should be possible to add a new tag", () => {
        cy.login()
            .addReview()
            .get("#edit-tags-btn")
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
        cy.delete();

        it("should be possible to delete a tag", () => {
            cy.login()
                .addReview()
                .get("#edit-tags-btn")
                .click()
                .get(".delete-tag:first")
                .click()
                .get("#save-tag-btn")
                .click();
            cy.get("#tags-feedback")
                .should("be.visible")
                .should("have.class", "valid-update");
            cy.get(".view-tag").should("have.length", 2);
            cy.delete();
        });
    });
});
