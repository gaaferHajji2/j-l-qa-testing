import { PasswordChecker } from "../../app/password_checker/PasswordChecker";


describe('PasswordChecker Test Suite', () => {
    let passwordChecker: PasswordChecker;
    
    beforeEach(() => {
        passwordChecker = new PasswordChecker()
    })

    describe("Check The Validation On Password", () => {
        it("Password Length At Least 8 Characters", () => {
            let result = passwordChecker.checkPassword('123456')
            expect(result).toBeFalsy()
        })

        it("Password Must Contain At Least One Lower Case Character", () => {
            let result = passwordChecker.checkPassword('123456')
            expect(result).toBeFalsy()
        })

        it("Password Must Contain At Least One Upper Case Character", ()=>{
            let result = passwordChecker.checkPassword('123456')
            expect(result).toBeFalsy()
        })
    })
})