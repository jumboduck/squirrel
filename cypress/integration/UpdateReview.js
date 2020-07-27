describe("Update entry", () => {
    it("should be possible to update the title", () => {
        cy.login().addReview().get("#name").type(" update").blur();
        cy.get("#name-feedback")
            .should("be.visible")
            .should("have.class", "valid-update");
    });
});
