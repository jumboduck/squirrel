describe("Search", () => {
    it("should be possible to search through reviews", () => {
        cy.login()
            .get(".search-input")
            .type("image")
            .get(".search-button")
            .click();
        cy.url().should("match", /search/);
        cy.get(".page-title").contains("SEARCH RESULTS FOR “IMAGE”", {
            matchCase: false,
        });
    });
    after(() => cy.logout());
});
