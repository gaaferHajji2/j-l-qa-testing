// jest.globalSetup.js
import { MongoMemoryServer } from 'mongodb-memory-server'

module.exports = async () => {
    const mongod = await MongoMemoryServer.create()
    const uri = mongod.getUri()
    process.env.MONGO_URI = uri
    global.__MONGOD__ = mongod
}