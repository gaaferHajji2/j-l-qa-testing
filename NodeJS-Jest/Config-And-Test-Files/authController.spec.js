import bcrypt from "bcryptjs"
import { registerUser, loginUser } from "./authController"
import User from "../models/users"
import { getJwtToken } from "../utils/helpers"

jest.mock("../utils/helpers", () => ({
    getJwtToken: jest.fn(() => 'Token@123')
}))

const mockReq = () => {
    return {
        body: {
            name: "Jafar Loka",
            email: "jloka@jloka.com",
            password: "Test@123"
        }
    }
}

const mockResp = () => {
    return {
        status: jest.fn().mockReturnThis(),
        json: jest.fn().mockReturnThis()
    }
}

const mockUserResp = {
    id: "507f1f77bcf86cd799439011",
    name: "Jafar Loka",
    email: "jloka@jloka.com",
    password: "Hash@Test@123"
}

afterEach(() => {
    jest.restoreAllMocks()
})

describe("Register User Tests", () => {
    it("Register User Successfully", async () => {
        jest.spyOn(bcrypt, 'hash').mockResolvedValueOnce("Hash@Test@123")
        jest.spyOn(User, 'create').mockResolvedValueOnce(mockUserResp)

        const mockedReq = mockReq()
        const mockedResp = mockResp()

        await registerUser(mockedReq, mockedResp)

        expect(mockedResp.status).toHaveBeenCalledWith(201)
        expect(mockedResp.json).toHaveBeenCalledWith({ token: 'Token@123' })
        expect(User.create).toHaveBeenCalledWith({
            name: "Jafar Loka",
            email: "jloka@jloka.com",
            password: "Hash@Test@123"
        })
    })

    it('should throw a validation error', async () => {
        const mockedReq = mockReq()
        const mockedResp = mockResp()

        mockedReq.body.name = null
        mockedReq.body.email = null
        mockedReq.body.password = null

        await registerUser(mockedReq, mockedResp)

        expect(mockedResp.status).toHaveBeenCalledWith(400)
        expect(mockedResp.json).toHaveBeenCalledWith({
            error: "Please enter all values",
        })
    })

    it('should throw error for duplicate email', async () => {
        jest.spyOn(User, 'create').mockRejectedValueOnce({ code: 11000 })
        const mockedReq = mockReq()
        const mockedResp = mockResp()

        await registerUser(mockedReq, mockedResp)

        expect(mockedResp.status).toHaveBeenLastCalledWith(400)
        expect(mockedResp.json).toHaveBeenCalledWith({ error: "Duplicate email" })
    })
})

describe("Login User Tests", () => {
    it("should throw validation error", async () => {
        const mockedReq = mockReq().body = { body: {} }
        const mockedResp = mockResp()

        await loginUser(mockedReq, mockedResp)

        expect(mockedResp.status).toHaveBeenCalledWith(400)
        expect(mockedResp.json).toHaveBeenCalledWith({
            error: "Please enter email & Password",
        })
    })

    it('should return invalid request for email or password', async () => {
        jest.spyOn(User, 'findOne').mockImplementation(() => ({
            select: jest.fn(() => null), // Returns the same mock object
            // exec: jest.fn().mockResolvedValue({
            //     _id: '123',
            //     email: 'test@example.com',
            //     password: 'hashedpassword' // Included because of +password
            // }),
        }));

        const mockedReq = mockReq()
        const mockedResp = mockResp()

        await loginUser(mockedReq, mockedResp)

        expect(mockedResp.status).toHaveBeenCalledWith(401)
        expect(mockedResp.json).toHaveBeenCalledWith({
            error: "Invalid Email or Password",
        })
    })

    it("should return password is incorrect", async () => {
        jest.spyOn(bcrypt, 'compare').mockResolvedValueOnce(false)
        jest.spyOn(User, 'findOne').mockImplementation(() => ({
            select: jest.fn(() => null), // Returns the same mock object
            exec: jest.fn().mockResolvedValue({
                _id: '123',
                name: "Jafar Loka",
                email: 'test@example.com',
                password: 'hashedpassword' // Included because of +password
            }),
        }));
        const mockedReq = mockReq()
        const mockedResp = mockResp()
        await loginUser(mockedReq, mockedResp)

        expect(mockedResp.status).toHaveBeenCalledWith(401)
        expect(mockedResp.json).toHaveBeenCalledWith({
            error: "Invalid Email or Password",
        })
    })

    it("should return valid token", async () => {
        jest.spyOn(bcrypt, 'compare').mockResolvedValueOnce(() => true)
        jest.spyOn(User, 'findOne').mockImplementation(() => ({
            select: jest.fn(() => mockUserResp), // Returns the same mock object
            // exec: jest.fn().mockResolvedValue(mockUserResp),
        }));

        const mockedReq = mockReq()
        const mockedResp = mockResp()
        await loginUser(mockedReq, mockedResp)

        expect(mockedResp.status).toHaveBeenCalledWith(200)
        expect(mockedResp.json).toHaveBeenCalledWith({
            token: 'Token@123'
        })
    })

    it("should return ISE", async () => {
        jest.spyOn(User, 'findOne').mockImplementation(() => ({
            select: jest.fn().mockRejectedValue(), // Returns the same mock object
            // exec: jest.fn().mockResolvedValue(mockUserResp),
        }));

        const mockedReq = mockReq()
        const mockedResp = mockResp()
        await loginUser(mockedReq, mockedResp)

        expect(mockedResp.status).toHaveBeenCalledWith(500)
        expect(mockedResp.json).toHaveBeenCalledWith({
            error: "Error while loggin in",
        })
    })
})