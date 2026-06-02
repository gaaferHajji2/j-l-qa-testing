import mongoose from "mongoose"
import { MongoMemoryServer } from 'mongodb-memory-server'

let mongo = null

export const connectToDatabase = async () => {
    mongo = await MongoMemoryServer.create()
    const uri = mongo.getUri()

    await mongoose.connect(uri)
}

export const closeDBConnection = async () => {
    await mongoose.connection.dropDatabase()
    await mongoose.connection.close()

    await mongo.stop()
}