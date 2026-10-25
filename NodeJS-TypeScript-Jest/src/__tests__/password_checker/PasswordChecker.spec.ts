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
            let result = passwordChecker.checkPassword('12345678')
            expect(result).toBeFalsy()
        })

        it("Password Must Contain At Least One Upper Case Character", ()=>{
            let result = passwordChecker.checkPassword('12345678abc')
            expect(result).toBeFalsy()
        })

        it("Should Return True For The Correct Values", ()=> {
            let result = passwordChecker.checkPassword('12345678abcABC')
            expect(result).toBeTruthy()
        })
    })
})