describe("Login page", () => {
    it("should be possible to login", () => {
        cy.login()
            .url()
            .should("match", /listing/);
        cy.logout();
    });

    it("should reject wrong credentials", () => {
        cy.login("wrongemail@test.com", "wrongpassword");
        cy.get(".alert-danger").should("exist");
    });
});
