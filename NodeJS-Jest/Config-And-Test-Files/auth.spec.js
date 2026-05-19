import jwt from 'jsonwebtoken'
import User from '../models/users'
import { isAuthenticatedUser } from './auth'

let mockRequest = () => {
    return {
        headers: {
            authorization: "Bearer Jafar.Loka.Test"
        }
    }
}

let mockResponse = () => {
    return {
        status: jest.fn().mockReturnThis(),
        json: jest.fn().mockReturnThis()
    }
}

let mockNext = jest.fn()

describe("Test The Auth Module", () => {
    it("should return missing token data", async () => {
        let mockedRequest = mockRequest()
        mockedRequest.headers.authorization = ""
        let mockedResponse = mockResponse()

        await isAuthenticatedUser(mockedRequest, mockedResponse, mockNext)

        expect(mockedResponse.status).toHaveBeenCalledWith(403)
        expect(mockedResponse.json).toHaveBeenCalledWith({ error: "Missing Authorization header with Bearer token" })
        expect(mockNext).not.toHaveBeenCalled()
    })

    it("should return authentication failed", async () => {
        let mockedRequest = mockRequest()
        mockedRequest.headers.authorization = "Bearer"
        let mockedResponse = mockResponse()

        await isAuthenticatedUser(mockedRequest, mockedResponse, mockNext)

        expect(mockedResponse.status).toHaveBeenCalledWith(401)
        expect(mockedResponse.json).toHaveBeenCalledWith({
            error: "Authentication Failed",
        })
        expect(mockNext).not.toHaveBeenCalled()
    })

    it("should call the next function", async () => {
        jest.spyOn(jwt, 'verify').mockResolvedValueOnce({ id: "64a1b2c3d4e5f6a7b8c9d0e1" })
        jest.spyOn(User, 'findById').mockResolvedValueOnce({
            id: "64a1b2c3d4e5f6a7b8c9d0e1",
            name: "Jafar Loka",
            email: "jloka@jloka.com",
            password: "Hash@Test@123"
        })
        let mockedRequest = mockRequest()
        let mockedResponse = mockResponse()

        await isAuthenticatedUser(mockedRequest, mockedResponse, mockNext)

        expect(mockedRequest).toHaveProperty('user')
        expect(mockNext).toHaveBeenCalledTimes(1)
    })
})