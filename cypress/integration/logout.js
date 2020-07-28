describe("Logout", () => {
    it("should be possible to logout", () => {
        cy.login();
        cy.logout().url().should("match", /login/);
    });
});
