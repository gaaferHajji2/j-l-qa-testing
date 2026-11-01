import { calculateComplexity, toUppercaseWithCallback, type stringInfo } from "../../app/doubles/JUtils"

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