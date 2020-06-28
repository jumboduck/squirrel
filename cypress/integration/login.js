describe("Login page", () => {
    it("should be possible to login", () => {
        cy.visit("/login")

            .get("#email")
            .type("test@test.com")

            .get("#password")
            .type("password")

            .get("#submit")
            .click()

            .url()
            .should("match", /listing/);
    });

    it("should reject a wrong password", () => {
        cy.visit("/login")

            .get("#email")
            .type("test@test.com")

            .get("#password")
            .type("wrongpassword")

            .get("#submit")
            .click();

        cy.get(".alert-danger").should("exist");
    });
});
