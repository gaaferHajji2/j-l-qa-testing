import User from "./users"

afterEach(() => {
    jest.resetAllMocks()
})

describe("Test The Users Model", () => {
    it("should create a new user with _id", () => {
        let user = new User({
            name: "Jafar Loka",
            email: "test@test.com",
            password: '12345674890'
        })

        expect(user).toHaveProperty('_id')
    })

    it("should throw validation error", async () => {
        try{
            let user = new User()

            // Here we don't call any other 3rd parties methods
            jest.spyOn(user, 'validate').mockRejectedValueOnce({
                errors: {
                    name: '',
                    email: '',
                    password: ''
                }
            })

            await user.validate()
        } catch (err) {
            expect(err.errors.name).toBeDefined()
            expect(err.errors.email).toBeDefined()
            expect(err.errors.password).toBeDefined()
        }
    })
})