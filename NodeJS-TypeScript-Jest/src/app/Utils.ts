export function toUpperCase(arg: string) {
    return arg.toUpperCase()
}

export type stringInfo = {
    upperCase: string,
    lowercase: string,
    characters: string[],
    length: number,
    extraInfo: Object | undefined
}

export function getStringInfo(arg: string): stringInfo {
    return {
        lowercase: arg.toLowerCase(),
        upperCase: arg.toUpperCase(),
        characters: [...arg],
        length: arg.length,
        extraInfo: {}
    }
}