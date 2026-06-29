import { toUpperCase } from "../app/Utils"

describe("Utils test suite", () => {
    it("should be upper case", () => {
        expect(toUpperCase('jloka')).toBe("JLOKA")
    })
})