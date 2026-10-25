
export enum PasswordErrors {
    SHORT = "Password is less than 8 characters",
    LOWER = "Password must contain at least one lowercase character",
    UPPER = "Password must contain at least one uppercase character"
}

export interface CheckResult {
    valid: boolean,
    reasons: string[]
}

export class PasswordChecker {

    public checkPassword(password: string): CheckResult {

        let result: CheckResult = { valid: true, reasons: [] }

        if (password.length < 8) {
            result.valid = false
            result.reasons.push(PasswordErrors.SHORT)
        }

        if(!password.match(/[a-z]/)) {
            result.valid = false
            result.reasons.push(PasswordErrors.LOWER)
        }

        if(!password.match(/[A-Z]/)) {
            result.valid = false
            result.reasons.push(PasswordErrors.UPPER)
        }

        return result;
    }

}