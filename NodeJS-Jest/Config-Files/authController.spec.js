import bcrypt from "bcryptjs"
import { registerUser } from "./authController"
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
    id: 1,
    name: "Jafar Loka",
    email: "jloka@jloka.com",
    password: "Hash@Test@123"
}

describe("Register User Tests", () => {
    it("Register User Successfully", async ()=>{
        jest.spyOn(bcrypt, 'hash').mockResolvedValueOnce("Hash@Test@123")
        jest.spyOn(User, 'create').mockResolvedValueOnce(mockUserResp)

        const mockedReq = mockReq()
        const mockedResp = mockResp()

        await registerUser(mockedReq, mockedResp)

        expect(mockedResp.status).toHaveBeenCalledWith(201)
        expect(mockedResp.json).toHaveBeenCalledWith({ token: 'Token@123' })
    })
})