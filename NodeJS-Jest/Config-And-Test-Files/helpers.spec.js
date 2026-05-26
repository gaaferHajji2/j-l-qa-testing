import jwt from 'jsonwebtoken'
import { getJwtToken } from './helpers'

describe("Test Helpers", () => {

    const ORIGINAL_ENV = process.env

    beforeEach(() => {
        // Create a shallow copy so mutations don't affect other tests
        process.env = { ...ORIGINAL_ENV }
        process.env.JWT_SECRET = 'Test@123'
        process.env.JWT_EXPIRES_TIME = '1w'
    });

    afterEach(() => {
        process.env = ORIGINAL_ENV
    });

    it("Test JWT Token", async () => {
        jest.spyOn(jwt, 'sign').mockResolvedValueOnce('JLoka-Token')
        let id = "123"

        const token = await getJwtToken(id)

        expect(token).toBeDefined()
        expect(token).toBe('JLoka-Token')
        expect(jwt.sign).toHaveBeenCalledWith({ id }, 'Test@123', {
            expiresIn: '1w',
        })
    })
})