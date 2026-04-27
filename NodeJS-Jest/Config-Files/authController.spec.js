import { registerUser } from "./authController";

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

describe("Register User Tests", () => {
    it("Register User Successfully", async ()=>{

    })
})