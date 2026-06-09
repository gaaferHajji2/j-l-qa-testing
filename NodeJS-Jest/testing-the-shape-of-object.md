When building a NodeJS application with TDD, there are several approaches to assert the shape of objects received from API requests. Here's a comprehensive guide:

## 1. Using Jest with Custom Matchers

```javascript
// test/api.test.js
const request = require('supertest');
const app = require('../app');

describe('GET /users/:id', () => {
  it('should return user object with correct shape', async () => {
    const response = await request(app)
      .get('/users/123')
      .expect(200);

    // Assert specific properties exist and have correct types
    expect(response.body).toHaveProperty('id');
    expect(response.body).toHaveProperty('name');
    expect(response.body).toHaveProperty('email');
    
    // Assert types
    expect(typeof response.body.id).toBe('number');
    expect(typeof response.body.name).toBe('string');
    expect(typeof response.body.email).toBe('string');
    
    // Assert nested objects
    expect(response.body).toHaveProperty('profile');
    expect(response.body.profile).toHaveProperty('avatar');
    expect(response.body.profile).toHaveProperty('bio');
  });

  it('should match exact shape using objectContaining', async () => {
    const response = await request(app)
      .get('/users/123')
      .expect(200);

    expect(response.body).toEqual(
      expect.objectContaining({
        id: expect.any(Number),
        name: expect.any(String),
        email: expect.stringMatching(/.+@.+\..+/),
        createdAt: expect.any(String),
        profile: expect.objectContaining({
          avatar: expect.any(String),
          bio: expect.any(String)
        })
      })
    );
  });
});
```

## 2. Using Schema Validation Libraries

### With Joi:

```javascript
// test/schemas/user.schema.js
const Joi = require('joi');

const userSchema = Joi.object({
  id: Joi.number().integer().positive().required(),
  name: Joi.string().min(1).max(100).required(),
  email: Joi.string().email().required(),
  age: Joi.number().integer().min(0).optional(),
  createdAt: Joi.date().iso().required(),
  profile: Joi.object({
    avatar: Joi.string().uri().optional(),
    bio: Joi.string().max(500).optional()
  }).optional()
});

// test/api.test.js
describe('GET /users/:id', () => {
  it('should return valid user object', async () => {
    const response = await request(app)
      .get('/users/123')
      .expect(200);

    // Validate against schema
    const { error, value } = userSchema.validate(response.body);
    
    expect(error).toBeUndefined();
    expect(value).toBeDefined();
  });
});
```

### With Zod:

```javascript
// test/schemas/user.schema.js
const { z } = require('zod');

const userSchema = z.object({
  id: z.number().int().positive(),
  name: z.string().min(1).max(100),
  email: z.string().email(),
  age: z.number().int().min(0).optional(),
  createdAt: z.string().datetime(),
  profile: z.object({
    avatar: z.string().url().optional(),
    bio: z.string().max(500).optional()
  }).optional()
});

// test/api.test.js
describe('GET /users/:id', () => {
  it('should return valid user object', async () => {
    const response = await request(app)
      .get('/users/123')
      .expect(200);

    // Parse and validate
    const result = userSchema.safeParse(response.body);
    
    expect(result.success).toBe(true);
    if (result.success) {
      expect(result.data).toBeDefined();
    }
  });
});
```

## 3. Creating Reusable Shape Assertions

```javascript
// test/utils/assertShape.js
function assertObjectShape(obj, expectedShape, path = '') {
  for (const [key, expectedType] of Object.entries(expectedShape)) {
    const currentPath = path ? `${path}.${key}` : key;
    
    // Check property exists
    expect(obj).toHaveProperty(key);
    
    const value = obj[key];
    
    // Handle nested objects
    if (typeof expectedType === 'object' && !Array.isArray(expectedType)) {
      expect(typeof value).toBe('object');
      expect(value).not.toBeNull();
      assertObjectShape(value, expectedType, currentPath);
    } 
    // Handle arrays
    else if (expectedType === Array) {
      expect(Array.isArray(value)).toBe(true);
    }
    // Handle specific types
    else {
      expect(typeof value).toBe(expectedType);
    }
  }
}

// Usage in tests
describe('GET /users/:id', () => {
  it('should return user with correct shape', async () => {
    const response = await request(app)
      .get('/users/123')
      .expect(200);

    const expectedShape = {
      id: 'number',
      name: 'string',
      email: 'string',
      createdAt: 'string',
      profile: {
        avatar: 'string',
        bio: 'string'
      },
      posts: Array
    };

    assertObjectShape(response.body, expectedShape);
  });
});
```

## 4. TypeScript Integration (if using TS)

```typescript
// test/types/user.types.ts
export interface UserProfile {
  avatar?: string;
  bio?: string;
}

export interface User {
  id: number;
  name: string;
  email: string;
  age?: number;
  createdAt: string;
  profile?: UserProfile;
}

// test/api.test.ts
import { User } from './types/user.types';

describe('GET /users/:id', () => {
  it('should return user with correct type', async () => {
    const response = await request(app)
      .get('/users/123')
      .expect(200);

    const user: User = response.body;
    
    // TypeScript will catch type errors at compile time
    expect(user.id).toBeGreaterThan(0);
    expect(user.name).toBeTruthy();
    expect(user.email).toMatch(/.+@.+\..+/);
  });
});
```

## 5. Complete TDD Example

```javascript
// First, write the test (RED)
describe('User API', () => {
  describe('GET /users/:id', () => {
    it('should return 404 for non-existent user', async () => {
      await request(app)
        .get('/users/999')
        .expect(404);
    });

    it('should return user with valid shape', async () => {
      const response = await request(app)
        .get('/users/1')
        .expect(200);

      expect(response.body).toEqual(
        expect.objectContaining({
          id: expect.any(Number),
          name: expect.any(String),
          email: expect.any(String),
          createdAt: expect.any(String)
        })
      );
      
      // Ensure no unexpected properties
      const allowedKeys = ['id', 'name', 'email', 'createdAt', 'profile'];
      const actualKeys = Object.keys(response.body);
      actualKeys.forEach(key => {
        expect(allowedKeys).toContain(key);
      });
    });
  });
});

// Then implement the code (GREEN)
// app.js
const express = require('express');
const app = express();

app.get('/users/:id', (req, res) => {
  const user = findUserById(req.params.id);
  
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }
  
  res.json({
    id: user.id,
    name: user.name,
    email: user.email,
    createdAt: user.createdAt.toISOString(),
    profile: user.profile || undefined
  });
});

module.exports = app;
```

## Best Practices:

1. **Start simple**: Begin with basic property checks, then add complexity
2. **Use `expect.objectContaining()`**: For flexible matching without requiring exact equality
3. **Validate at boundaries**: Test both successful responses and error cases
4. **Don't over-test**: Focus on the contract/API shape, not implementation details
5. **Reuse schemas**: Share validation schemas between tests and runtime validation
6. **Test edge cases**: Null values, missing optional fields, empty arrays

The approach you choose depends on your project's complexity. For simple APIs, Jest's built-in matchers work well. For complex schemas, consider Joi or Zod for better maintainability and reusability.