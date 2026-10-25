

export class PasswordChecker {

    public checkPassword(password: string): boolean {
        if (
        password.length < 8 ||
        !password.match(/[a-z]/) ||
        !password.match(/[A-Z]/)
    ) {
        return false;
    }
    return true;
    }

}