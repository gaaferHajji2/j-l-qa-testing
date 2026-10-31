import { PasswordChecker, PasswordErrors, type CheckResult } from "../../app/password_checker/PasswordChecker";


describe('PasswordChecker Test Suite', () => {
    let passwordChecker: PasswordChecker;
    
    beforeEach(() => {
        passwordChecker = new PasswordChecker()
    })

    describe("Check The Validation On Password", () => {
        it("Password Length At Least 8 Characters", () => {
            let result: CheckResult = passwordChecker.checkPassword('123456')
            expect(result.valid).toBeFalsy()
            expect(result.reasons).toEqual([PasswordErrors.SHORT, PasswordErrors.LOWER, PasswordErrors.UPPER])
        })

        it("Password Length At Least 8 Characters -- Contain Lower Case Letters", () => {
            let result: CheckResult = passwordChecker.checkPassword('123abc')
            expect(result.valid).toBeFalsy()
            expect(result.reasons).toEqual([PasswordErrors.SHORT, PasswordErrors.UPPER])
            expect(result.reasons).not.toContain(PasswordErrors.LOWER)
        })

        it("Password Length At Least 8 Characters -- Contain Upper Case Letters", () => {
            let result: CheckResult = passwordChecker.checkPassword('123ABC')
            expect(result.valid).toBeFalsy()
            expect(result.reasons).toEqual([PasswordErrors.SHORT, PasswordErrors.LOWER])
            expect(result.reasons).not.toContain(PasswordErrors.UPPER)
        })

        it("Password Must Contain At Least One Lower Case Character -- no characters", () => {
            let result: CheckResult = passwordChecker.checkPassword('12345678')
            expect(result.valid).toBeFalsy()
            expect(result.reasons).toEqual([PasswordErrors.LOWER, PasswordErrors.UPPER])
            expect(result.reasons).not.toContain(PasswordErrors.SHORT)
        })

        it("Password Must Contain At Least One Lower Case Character", () => {
            let result: CheckResult = passwordChecker.checkPassword('12345678ABC')
            expect(result.valid).toBeFalsy()
            expect(result.reasons).toEqual([PasswordErrors.LOWER])
            expect(result.reasons).not.toContain(PasswordErrors.SHORT)
        })

        it("Password Must Contain At Least One Upper Case Character", ()=>{
            let result: CheckResult = passwordChecker.checkPassword('12345678abc')
            expect(result.valid).toBeFalsy()
            expect(result.reasons).toEqual([PasswordErrors.UPPER])
            expect(result.reasons).not.toContain(PasswordErrors.SHORT)
        })

        it("Should Return True For The Correct Values", () => {
            let result: CheckResult = passwordChecker.checkPassword('12345678abcABC')
            expect(result.valid).toBeTruthy()
            expect(result.reasons).toEqual([])
            expect(result.reasons).not.toContain(PasswordErrors.SHORT)
        })

        it("Should Not Valid Admin Password Contain No Number And Return False", () => {
            const result = passwordChecker.checkPassword("JafarLoka-ITE-Developer", true)

            expect(result.valid).toBeFalsy()
            expect(result.reasons).toContain(PasswordErrors.NUMBER)
        })

        it("Should Valid Admin Password Contain Number And Return True", () => {
            const result = passwordChecker.checkPassword("JafarLoka-01", true)
            expect(result.valid).toBeTruthy()
            expect(result.reasons).not.toContain(PasswordErrors.NUMBER)
            expect(result.reasons).toEqual([])
        })

        it("Should Valid Normal User Password Without Number To Return Truthy", () => {
            const result = passwordChecker.checkPassword("JafarLoka-ITE-Developer")
            expect(result.valid).toBeTruthy()
            expect(result.reasons).not.toContain(PasswordErrors.NUMBER)
            expect(result.reasons).toEqual([])
        })
    })
})