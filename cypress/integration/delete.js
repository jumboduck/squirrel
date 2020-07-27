describe("Delete review", () => {
    it("should be possible to delete a review", () => {
        cy.login().addReview().delete();
        cy.get(".alert").contains("was deleted.");
    });
});
