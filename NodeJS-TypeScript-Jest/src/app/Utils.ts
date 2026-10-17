export function toUpperCase(arg: String) {
    return arg.toUpperCase()
}

export type stringInfo = {
    upperCase: string,
    lowercase: string,
    characters: string[],
    length: number,
    extraInfo: Object | undefined
}