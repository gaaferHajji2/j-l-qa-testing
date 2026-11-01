export type stringInfo = {
    upperCase: string,
    lowercase: string,
    characters: string[],
    length: number,
    extraInfo: Object | undefined
}

export function calculateComplexity(stringInfo: stringInfo) {
    if(!stringInfo.extraInfo || Object.keys(stringInfo.extraInfo).length === 0)
        return stringInfo.length
    return Object.keys(stringInfo.extraInfo!).length * stringInfo.length
}

export function toUppercaseWithCallback(arg: string, callback: Function) {
    if(!arg){
        callback('Invalid Argument!')
        return;
    }

    callback(`Callback with: ${arg}`)
    return arg.toUpperCase()
}