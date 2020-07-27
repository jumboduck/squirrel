describe("Add review page", () => {
    it("should be possible to add a review", () => {
        cy.login("test@test.com", "password");
        cy.addReview("Test Name", "Test Description", 4, true, [
            "tag1",
            "tag2",
            "tag3",
        ])
            .url()
            .should("match", /entry/)
            .get("#name")
            .should("have.value", "Test Name");
        cy.delete();
    });
});
