describe("Login page", () => {
    it("should be possible to login", () => {
        cy.login("test@test.com", "password")
            .url()
            .should("match", /listing/);
    });

    it("should reject a wrong password", () => {
        cy.login("test@test.com", "wrongpassword");
        cy.get(".alert-danger").should("exist");
    });
});
