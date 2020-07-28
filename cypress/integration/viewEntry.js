describe("View entry", () => {
    before(() => cy.login());
    beforeEach(() => Cypress.Cookies.preserveOnce("session"));
    it("should be possible to view a review by clicking on image", () => {
        cy.get(".card:first a img").click().url().should("match", /entry/);
    });
    it("should be possible to view a review by clicking on title", () => {
        cy.get(".logo-image").click();
        cy.get(".card:first h2 a").click().url().should("match", /entry/);
    });
});
