import request from 'supertest'
import { connectToDatabase, closeDBConnection } from './db-handler'

beforeAll(async ()=> await connectToDatabase())
afterAll(async () => await closeDBConnection())