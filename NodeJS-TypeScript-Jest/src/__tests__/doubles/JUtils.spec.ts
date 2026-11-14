import { calculateComplexity, JStringUtils, toUppercaseWithCallback, type stringInfo } from "../../app/doubles/JUtils"

describe("Test Doubles", () => {
    test("Test Object With Data", () => {
        let t1 = {
            length: 5,
            extraInfo: {
                JLoka01: "Jafar-Loka-01",
                JLoka02: "Jafar-LOka-02"
            }
        }

        let result = calculateComplexity(t1 as any)
        expect(result).toBe(10)
    })

    test("Test Empty ExtraInfo", () => {
        let t1 = {
            length: 5,
            extraInfo: {}
        }

        let result = calculateComplexity(t1 as any)
        expect(result).toBe(5)
    })

    test("With String Value And Callback", () => {
        let arg = "Jafar Loka"
        let callback = jest.fn()

        let result = toUppercaseWithCallback(arg, callback)

        expect(callback).toHaveBeenCalledWith(`Callback with: ${arg}`)
        expect(callback).toHaveBeenCalledTimes(1)
        expect(result).toBe("JAFAR LOKA")
    })

    test("with callback Only", () => {
        let arg = ''
        let callback = jest.fn()

        let result = toUppercaseWithCallback(arg, callback)

        expect(callback).toHaveBeenCalledWith(`Invalid Argument!`)
        expect(callback).toHaveBeenCalledTimes(1)
        expect(result).toBe(undefined)
    })
})

describe("Testing Spies", () => {
    let sut: JStringUtils

    beforeEach(() => {
        sut = new JStringUtils()
    })

    afterEach(() => {
        jest.clearAllMocks()
        jest.resetAllMocks()
    })

    test("Test On To Upper Case", async () => {
        const toUpperSpy = jest.spyOn(sut, 'toUpperCase').mockResolvedValueOnce(Promise.resolve("JAFAR-LOKA"))
        const res1 = await sut.toUpperCase("Jafar-Loka")

        expect(res1).toEqual("JAFAR-LOKA")
        expect(toUpperSpy).toHaveBeenCalledTimes(1)
        expect(toUpperSpy).toHaveBeenCalledWith("Jafar-Loka")
    })

    test("Test Throw Error", () => {
        jest.spyOn(sut, 'toUpperCase').mockImplementation(() => {
            throw new Error('Illegal Argument!')
        })

        expect(() => sut.toUpperCase(undefined)).toThrow('Illegal Argument!')
    })
})