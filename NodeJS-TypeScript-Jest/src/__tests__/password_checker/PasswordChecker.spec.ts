import { PasswordChecker } from "../../app/password_checker/PasswordChecker";


describe('PasswordChecker Test Suite', () => {
    let passwordChecker: PasswordChecker;
    
    beforeEach(() => {
        passwordChecker = new PasswordChecker()
    })

    it("Basic Test", () => {
        passwordChecker.checkPassword()

        expect(1 + 1).toBe(2)
    })
})