describe("View entry", () => {
    it("should be possible to view a review by clicking on image", () => {
        cy.login("test@test.com", "password");
        cy.get(".card a img:first").click().url().should("match", /entry/);
        cy.logout();
    });
    it("should be possible to view a review by clicking on title", () => {
        cy.login("test@test.com", "password");
        cy.get(".card h2 a:first").click().url().should("match", /entry/);
        cy.logout();
    });
});
