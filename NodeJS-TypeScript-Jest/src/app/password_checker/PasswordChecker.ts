
export enum PasswordErrors {
    SHORT = "Password is less than 8 characters",
    LOWER = "Password must contain at least one lowercase character",
    UPPER = "Password must contain at least one uppercase character",
    NUMBER = "Password must contain at least one number"
}

export interface CheckResult {
    valid: boolean,
    reasons: string[]
}

export class PasswordChecker {

    public checkPassword(password: string, isAdmin: boolean = false): CheckResult {

        let result: CheckResult = { valid: true, reasons: [] }

        this.checkShortPasswords(password, result)
        this.checkNoLowerPasswords(password, result)
        this.checkNoUpperPasswords(password, result)
        
        if(isAdmin) {
            this.checkNoNumberPassword(password, result)
        }

        return result;
    }

    private checkShortPasswords(password: string, result: CheckResult) {
        if (password.length < 8) {
            result.valid = false
            result.reasons.push(PasswordErrors.SHORT)
        }
    }

    private checkNoLowerPasswords(password: string, result: CheckResult) {
        if(!password.match(/[a-z]/)) {
            result.valid = false
            result.reasons.push(PasswordErrors.LOWER)
        }
    }

    private checkNoUpperPasswords(password: string, result: CheckResult) {
        if(!password.match(/[A-Z]/)) {
            result.valid = false
            result.reasons.push(PasswordErrors.UPPER)
        }
    }

    private checkNoNumberPassword(password: string, result: CheckResult) {
        if(!password.match(/[0-9]/)){
            result.valid = false
            result.reasons.push(PasswordErrors.NUMBER)
        }
    }
}