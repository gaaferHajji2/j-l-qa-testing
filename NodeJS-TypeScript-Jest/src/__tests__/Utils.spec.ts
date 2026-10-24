import { getStringInfo, toUpperCase } from "../app/Utils"

describe("Utils test suite", () => {
    it("should be upper case", () => {
        expect(toUpperCase('jloka')).toBe("JLOKA")
    })

    describe.only("toUpperCase tests", () => {
        it.each([
            {data: 'Jafar-Loka-01', expected: 'JAFAR-LOKA-01'},
            {data: 'j-l-01', expected: 'J-L-01'},
            {data: 'Jafar-Test-01', expected: 'JAFAR-TEST-01'},
        ])("Test parametrize with $data expected $expected", ({ data, expected }) => {
            expect(toUpperCase(data)).toBe(expected)
        })
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
        expect(actual.characters).toEqual(
            expect.arrayContaining(['J', 'L'])
        )
        expect(actual.characters).toContainEqual<string>('J')
        expect(actual.extraInfo).toMatchObject({})
    })

    // it.only("should only run", () => {
    //     expect(1 + 1).toBe(2)
    // })
})