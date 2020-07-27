describe("Logout", () => {
    it("should be possible to logout", () => {
        cy.login("test@test.com", "password");
        cy.logout().url().should("match", /login/);
    });
});
