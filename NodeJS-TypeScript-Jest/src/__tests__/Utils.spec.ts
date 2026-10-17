import { getStringInfo, toUpperCase } from "../app/Utils"

describe("Utils test suite", () => {
    it("should be upper case", () => {
        expect(toUpperCase('jloka')).toBe("JLOKA")
    })

    it("should test stringInfo function", () => {
        const testData = "Jafar-Loka"
        const actual = getStringInfo(testData)

        expect(actual).not.toBeNull()
        expect(actual.lowercase).toBe(testData.toLowerCase())
        expect(actual.upperCase).toBe(testData.toUpperCase())
        expect(actual.length).toEqual(testData.length)
        expect(actual.characters).toBeInstanceOf(Array)
        expect(actual.characters).toEqual([...testData])
        expect(actual.characters).toContainEqual('J')
        expect(actual.extraInfo).toMatchObject({})
    })
})