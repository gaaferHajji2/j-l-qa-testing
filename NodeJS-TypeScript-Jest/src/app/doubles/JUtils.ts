export type stringInfo = {
    upperCase: string,
    lowercase: string,
    characters: string[],
    length: number,
    extraInfo: Object | undefined
}

type fnWithString = (arg: string) => void

export function calculateComplexity(stringInfo: stringInfo) {
    if(!stringInfo.extraInfo || Object.keys(stringInfo.extraInfo).length === 0)
        return stringInfo.length
    return Object.keys(stringInfo.extraInfo!).length * stringInfo.length
}

export function toUppercaseWithCallback(arg: string, callback: fnWithString) {
    if(!arg){
        callback('Invalid Argument!')
        return;
    }

    callback(`Callback with: ${arg}`)
    return arg.toUpperCase()
}

export class JStringUtils {
    public toUpperCase(arg: string): string {
        if (!arg) {
            throw new Error('Illegal Argument!')
        }

        return arg.toUpperCase()
    }

    public logString(arg: string): void {
        console.log(arg)
    }
}