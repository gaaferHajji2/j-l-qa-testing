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

    it("should return missing token data", async () => {
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
})