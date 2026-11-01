import { calculateComplexity, type stringInfo } from "../../app/doubles/JUtils"

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

    test("Test empty extraInfo", () => {
        let t1 = {
            length: 5,
            extraInfo: {}
        }

        let result = calculateComplexity(t1 as any)
        expect(result).toBe(5)
    })
})