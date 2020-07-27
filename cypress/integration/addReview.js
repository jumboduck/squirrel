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

    it("should not add a review if no name is typed", () => {
        cy.login("test@test.com", "password");
        cy.addReview("", "Test Description", 3, false, [])
            .url()
            .should("match", /add/);
    });

    it("should not add a review if no description is typed", () => {
        cy.login("test@test.com", "password");
        cy.addReview("Test Name", "", 3, false, [])
            .url()
            .should("match", /add/);
    });

    it("should not add a review if no rating is chosen", () => {
        cy.login("test@test.com", "password");
        cy.addReview("Test Name", "Test Description", NaN, false, [])
            .url()
            .should("match", /add/);
    });
});
