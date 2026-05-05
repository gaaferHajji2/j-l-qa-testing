import Job from "../models/jobs"

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
        query: { },
        // params: { id: "64b2c3d4e5f6a7b8c9d0e1f3" },
        params: { },
        user: {
            id: "507f1f77bcf86cd799439011",
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
})

describe("The Jobs Controller Test", () => {

})