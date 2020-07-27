describe("Update entry", () => {
    it("should be possible to update the title", () => {
        cy.login().addReview().get("#name").type(" update").blur();
        cy.get("#name-feedback")
            .should("be.visible")
            .should("have.class", "valid-update");
    });

    it("should not be possible to leave the title blank", () => {
        cy.login().addReview().get("#name").clear().blur();
        cy.get("#name-feedback")
            .should("be.visible")
            .should("have.class", "invalid-update");
    });

    it("should be possible to update the description", () => {
        cy.login().addReview().get("#description").type(" update").blur();
        cy.get("#description-feedback")
            .should("be.visible")
            .should("have.class", "valid-update");
    });

    it("should not be possible to leave the description blank", () => {
        cy.login().addReview().get("#description").clear().blur();
        cy.get("#description-feedback")
            .should("be.visible")
            .should("have.class", "invalid-update");
    });
});
