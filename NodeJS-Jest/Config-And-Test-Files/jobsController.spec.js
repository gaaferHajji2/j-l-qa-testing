import Job from "../models/jobs"
import { deleteJob, getJob, getJobs, newJob, updateJob } from "./jobsController"

const mockedJobs = [
    {
        "title": "Senior Software Engineer",
        "description": "Design, develop, and maintain scalable backend services using modern cloud technologies.",
        "email": "careers@techflow.io",
        "address": "101 Innovation Drive, San Francisco, CA 94105",
        "company": "TechFlow Solutions",
        "industry": ["Information Technology"],
        "positions": 3,
        "salary": 155000,
        "postingDate": "2024-06-12T09:00:00.000Z",
        "user": "64a1b2c3d4e5f6a7b8c9d0e1"
    },
    {
        "title": "Corporate Financial Advisor",
        "description": "Provide strategic financial planning, risk assessment, and portfolio management for high-net-worth clients.",
        "email": "hr@globaltrustbank.com",
        "address": "550 Madison Avenue, New York, NY 10022",
        "company": "Global Trust Bank",
        "industry": ["Banking", "Business"],
        "positions": 2,
        "salary": 110000,
        "postingDate": "2024-07-01T14:30:00.000Z",
        "user": "64b2c3d4e5f6a7b8c9d0e1f2"
    },
    {
        "title": "Instructional Designer",
        "description": "Create engaging e-learning modules and corporate training curricula aligned with organizational goals.",
        "email": "jobs@learnpath.org",
        "address": "890 Academic Blvd, Austin, TX 78701",
        "company": "LearnPath Institute",
        "industry": ["Education/Training"],
        "positions": 1,
        "salary": 82000,
        "postingDate": "2024-08-15T10:00:00.000Z",
        "user": "64c3d4e5f6a7b8c9d0e1f2a3"
    },
    {
        "title": "Network Infrastructure Specialist",
        "description": "Deploy and troubleshoot enterprise telecommunication networks, ensuring 99.9% uptime and security compliance.",
        "email": "techrecruit@connectwave.net",
        "address": "222 Signal Ridge, Seattle, WA 98101",
        "company": "ConnectWave Telecom",
        "industry": ["Telecommunication", "Information Technology"],
        "positions": 4,
        "salary": 125000,
        "postingDate": "2024-09-03T11:15:00.000Z",
        "user": "64d4e5f6a7b8c9d0e1f2a3b4"
    }
]

const mockReq = () => {
    return {
        body: {},
        // query: { keyword: 'Jafar Loka-01' },
        query: {},
        // params: { id: "64b2c3d4e5f6a7b8c9d0e1f3" },
        params: {},
        user: {
            id: "64a1b2c3d4e5f6a7b8c9d0e1",
            name: "Jafar Loka",
            email: "jloka@jloka.com",
            password: "Hash@Test@123"
        }
    }
}

const mockResp = () => {
    return {
        status: jest.fn().mockReturnThis(),
        json: jest.fn().mockReturnThis()
    }
}

afterEach(() => {
    jest.restoreAllMocks()
    jest.clearAllMocks()
})

describe("The Jobs Controller Test", () => {
    describe("Get All Jobs", () => {
        it("should return all jobs array", async () => {
            const mockSkip = jest.fn().mockReturnThis() // Returns 'this' to allow chaining
            const mockLimit = jest.fn().mockReturnThis()

            jest.spyOn(Job, 'find').mockReturnValue({
                limit: mockLimit,
                skip: mockSkip,
            })

            let jobs = [mockedJobs[0], mockedJobs[1]]

            mockSkip.mockResolvedValue(jobs)

            let mockedRequest = mockReq()
            let mockedResponse = mockResp()

            await getJobs(mockedRequest, mockedResponse)

            expect(mockedResponse.status).toHaveBeenCalledWith(200)
            expect(mockedResponse.json).toHaveBeenCalledWith({ jobs })
        })

        it("Get Job By Specific Keyword", async () => {
            const keyword = { title: /dev/i };
            const resPerPage = 10;
            const skip = 0;
            const mockSkip = jest.fn().mockReturnThis() // Returns 'this' to allow chaining
            const mockLimit = jest.fn().mockReturnThis()

            jest.spyOn(Job, 'find').mockReturnValue({
                limit: mockLimit,
                skip: mockSkip,
            })

            let jobs = [mockedJobs[0], mockedJobs[1]]

            mockSkip.mockResolvedValue(jobs)

            let mockedRequest = mockReq()
            mockedRequest.query.keyword = keyword
            mockedRequest.query.page = 1
            let mockedResponse = mockResp()

            await getJobs(mockedRequest, mockedResponse)

            expect(mockedResponse.status).toHaveBeenCalledWith(200)
            expect(mockedResponse.json).toHaveBeenCalledWith({ jobs })
            expect(Job.find).toHaveBeenCalledWith({
                title: {
                    $regex: mockedRequest.query.keyword,
                    $options: "i",
                },
            })
        })
    })

    describe("Create A New Job", () => {
        it("should create a new job", async () => {
            jest.spyOn(Job, 'create').mockImplementationOnce(() => mockedJobs[0])

            let mockedReq = mockReq()
            let mockedRes = mockResp()

            await newJob(mockedReq, mockedRes)

            expect(mockedRes.status).toHaveBeenCalledWith(200)
            expect(mockedRes.json).toHaveBeenCalledWith({ job: mockedJobs[0] })
        })

        it("should throw exception", async () => {
            jest.spyOn(Job, 'create').mockRejectedValue({ name: 'ValidationError' })

            let mockedReq = mockReq()
            let mockedRes = mockResp()
            await newJob(mockedReq, mockedRes)

            expect(mockedRes.status).toHaveBeenCalledWith(400)
            expect(mockedRes.json).toHaveBeenCalledWith({
                error: "Please enter all values",
            })
        })
    })

    describe("Get Job By Id", () => {
        it("should return one job only", async () => {
            jest.spyOn(Job, 'findById').mockResolvedValueOnce(mockedJobs[0])

            let mockedReq = mockReq()
            mockedReq.params.id = '64a1b2c3d4e5f6a7b8c9d0e1'
            let mockedRes = mockResp()

            await getJob(mockedReq, mockedRes)

            expect(mockedRes.status).toHaveBeenCalledWith(200)
            expect(mockedRes.json).toHaveBeenCalledWith({ job: mockedJobs[0] })
        })

        it("should return no job found", async () => {
            jest.spyOn(Job, 'findById').mockResolvedValueOnce(null)

            let mockedReq = mockReq()
            let mockedRes = mockResp()

            await getJob(mockedReq, mockedRes)

            expect(mockedRes.status).toHaveBeenCalledWith(404)
            expect(mockedRes.json).toHaveBeenCalledWith({
                error: "Job not found",
            })
        })

        it("should throw exception", async () => {
            jest.spyOn(Job, 'findById').mockRejectedValueOnce({ name: 'CastError' })

            let mockedReq = mockReq()
            mockedReq.params = { id: "Jafar-Loka-01" }
            let mockedRes = mockResp()

            await getJob(mockedReq, mockedRes)

            expect(Job.findById).toHaveBeenCalledWith(mockedReq.params.id)
            expect(mockedRes.status).toHaveBeenCalledWith(400)
            expect(mockedRes.json).toHaveBeenCalledWith({
                error: "Please enter correct id",
            })
        })
    })

    describe("Update Job By Id", () => {
        it("should update the job successfully", async () => {
            jest.spyOn(Job, 'findById').mockResolvedValueOnce(mockedJobs[0])
            jest.spyOn(Job, 'findByIdAndUpdate').mockResolvedValueOnce(mockedJobs[0])

            let mockedReq = mockReq()
            mockedReq.params = { id: "64a1b2c3d4e5f6a7b8c9d0e1"}
            mockedReq.body = mockedJobs[0]
            let mockedResp = mockResp()

            await updateJob(mockedReq, mockedResp)
            expect(Job.findByIdAndUpdate).toHaveBeenLastCalledWith(mockedReq.params.id, mockedReq.body, { new: true })
            expect(mockedResp.status).toHaveBeenCalledWith(200)
            expect(mockedResp.json).toHaveBeenCalledWith({ job: mockedJobs[0] })
        })

        it("should return job not found", async () => {
            jest.spyOn(Job, 'findById').mockResolvedValueOnce(null)
            // jest.spyOn(Job, 'findByIdAndUpdate').mockResolvedValueOnce(mockedJobs[0])

            let mockedReq = mockReq()
            let mockedResp = mockResp()

            await updateJob(mockedReq, mockedResp)

            expect(mockedResp.status).toHaveBeenCalledWith(404)
            expect(mockedResp.json).toHaveBeenCalledWith({
                error: "Job not found",
            })
        })

        it("should return not allowed to update job", async () => {
            jest.spyOn(Job, 'findById').mockResolvedValueOnce(mockedJobs[0])
            // jest.spyOn(Job, 'findByIdAndUpdate').mockResolvedValueOnce(mockedJobs[0])

            let mockedReq = mockReq()
            mockedReq.user.id = "1"
            let mockedResp = mockResp()

            await updateJob(mockedReq, mockedResp)

            expect(mockedResp.status).toHaveBeenCalledWith(401)
            expect(mockedResp.json).toHaveBeenCalledWith({
                error: "You are not allowed to update this job",
            })
        })
    })

    describe("Delete Job By Id", () => {
        it("should delete a product", async() => {
            jest.spyOn(Job, 'findById').mockResolvedValueOnce(mockedJobs[0])
            jest.spyOn(Job, 'findByIdAndDelete').mockResolvedValueOnce(mockedJobs[0])

            let mockedReq = mockReq()
            mockedReq.params = { id: "64a1b2c3d4e5f6a7b8c9d0e1" }
            let mockedResp = mockResp()

            await deleteJob(mockedReq, mockedResp)

            expect(Job.findById).toHaveBeenCalledWith(mockedReq.params.id)
            expect(Job.findByIdAndDelete).toHaveBeenCalledWith(mockedReq.params.id)
            expect(mockedResp.status).toHaveBeenCalledWith(200)
            expect(mockedResp.json).toHaveBeenCalledWith({
                job: mockedJobs[0]
            })
        })
    })
})