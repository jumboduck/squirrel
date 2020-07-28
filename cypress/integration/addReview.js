describe("Add review page", () => {
    before(() => cy.login());
    beforeEach(() => Cypress.Cookies.preserveOnce("session"));
    it("should be possible to add a review", () => {
        cy.addReview({
            name: "Test Name",
            description: "Test Description",
            rating: 4,
            fav: true,
            tags: ["tag1", "tag2", "tag3"],
        })
            .url()
            .should("match", /entry/)
            .get("#name")
            .should("have.value", "Test Name");
        cy.delete();
    });

    it("should not add a review if no name is typed", () => {
        cy.addReview({
            name: "",
            description: "Test Description",
            rating: 3,
            fav: false,
            tags: [],
        })
            .url()
            .should("match", /add/);
    });

    it("should not add a review if no description is typed", () => {
        cy.addReview({
            name: "Test Name",
            description: "",
            rating: 3,
            fav: false,
            tags: [],
        })
            .url()
            .should("match", /add/);
    });

    it("should not add a review if no rating is chosen", () => {
        cy.addReview({
            name: "Test Name",
            description: "Test Description",
            rating: undefined,
            fav: false,
            tags: [],
        })
            .url()
            .should("match", /add/);
    });
    after(() => cy.logout());
});
