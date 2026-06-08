`mongodb-memory-server` is specifically designed to download and manage its own MongoDB binary. **It cannot be configured to use your local MongoDB installation.**

If you want to use your local MongoDB, simply bypass `mongodb-memory-server` entirely:

## Use Local MongoDB Directly

```javascript
import mongoose from 'mongoose'

export const connectToDB = async () => {
  const uri = process.env.MONGO_URI || 'mongodb://localhost:27017/testdb'
  await mongoose.connect(uri)
}

export const closeDBConnection = async () => {
  await mongoose.connection.dropDatabase()
  await mongoose.connection.close()
}
```

## For Jest Tests with Local MongoDB

```javascript
// jest.config.js
module.exports = {
  testEnvironment: 'node',
}
```

```javascript
// __tests__/setup.js
import mongoose from 'mongoose'

beforeAll(async () => {
  const uri = process.env.MONGO_URI || 'mongodb://localhost:27017/testdb'
  await mongoose.connect(uri)
})

afterEach(async () => {
  // Clean collections between tests instead of dropping DB
  const collections = mongoose.connection.collections
  for (const key in collections) {
    await collections[key].deleteMany({})
  }
})

afterAll(async () => {
  await mongoose.connection.close()
})
```

## Key Differences

| Feature | mongodb-memory-server | Local MongoDB |
|---------|----------------------|---------------|
| Binary management | Downloads & manages own | Uses existing installation |
| Isolation | Fresh instance per run | Shared with other apps |
| Speed | Slower first run | Always fast |
| Setup required | None | MongoDB must be running |
| CI/CD friendly | Yes (self-contained) | Requires MongoDB service |

## When to Use Which

- **Local MongoDB**: Development, when MongoDB is already installed, faster tests
- **mongodb-memory-server**: CI/CD pipelines, team environments where MongoDB isn't guaranteed, isolated testing

> ⚠️ **Warning**: If using local MongoDB for tests, always use a **dedicated test database** (e.g., `myapp_test`) to avoid corrupting development or production data. Never point tests at a production database.

If your goal was to avoid the download overhead of `mongodb-memory-server`, switching to direct local MongoDB connection is the correct solution.