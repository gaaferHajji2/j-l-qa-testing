To create **strict unit tests** without connecting to a database (real or in-memory), we must mock Mongoose itself. This isolates the test to only verify that the **Schema definition** and **Mongoose validation logic** work correctly, without any I/O overhead.

We will use `jest.mock` to mock the `mongoose` library.

### Prerequisites

Ensure you have Jest installed:
```bash
npm install --save-dev jest
```

### The Unit Test File (`tests/job.model.unit.test.js`)

This approach mocks `mongoose.Schema` and `mongoose.model` to capture the schema definition and then manually triggers Mongoose's internal validation engine on a document instance.

```javascript
// tests/job.model.unit.test.js

// 1. Mock mongoose before requiring the model
const mockValidateSync = jest.fn();
const mockSave = jest.fn();
const mockModelInstance = {
  validateSync: mockValidateSync,
  save: mockSave,
};

// Mock the mongoose module
jest.mock('mongoose', () => {
  const actualMongoose = jest.requireActual('mongoose');
  
  return {
    ...actualMongoose,
    Schema: jest.fn((definition, options) => {
      // Return a real Schema instance so we can use its internal validation logic if needed,
      // OR simply store the definition for inspection.
      // For strict unit testing of validators, we often let Mongoose create the schema 
      // but mock the connection/model parts.
      return new actualMongoose.Schema(definition, options);
    }),
    model: jest.fn((name, schema) => {
      // Return a mock constructor that returns our mock instance
      const ModelConstructor = jest.fn(function(data) {
        this.data = data;
        // Create a real document-like object for validation testing
        // We use a real Schema instance to test validators accurately
        this._doc = data;
      });
      
      ModelConstructor.prototype.validateSync = function() {
        // Create a temporary real document to run actual Mongoose validation logic
        // This is a hybrid approach: mocking the DB connection but using real Schema logic
        const TempModel = actualMongoose.model('TempJob', this.schema || new actualMongoose.Schema({}));
        // Note: Accessing internal schema from mock is tricky. 
        // See alternative approach below for cleaner pure unit test.
        return null; 
      };

      ModelConstructor.prototype.save = mockSave;
      
      return ModelConstructor;
    }),
  };
});

// Since mocking Mongoose internals while keeping validation logic is complex,
// The most reliable "Unit Test" for Mongoose Schemas without a DB 
// is to import the SCHEMA directly and test it using a detached Document.

// REVISED APPROACH: Export the Schema separately for easier unit testing.
// If you cannot change the source code, see the note at the bottom.

// Assuming you can slightly refactor models/Job.js to export schema:
// module.exports = { JobModel: mongoose.model('Job', jobSchema), jobSchema };

// For this example, I will assume we are testing the validation logic 
// by creating a standalone Schema instance in the test file that mirrors the original.

const mongoose = require('mongoose');

// Define the schema exactly as in the model (Copy-Paste for Unit Test isolation)
const jobSchema = new mongoose.Schema({
  title: {
    type: String,
    required: [true, "Please enter Job title."],
    trim: true,
    maxlength: [100, "Job title can not exceed 100 characters."],
  },
  description: {
    type: String,
    required: [true, "Please enter Job description."],
  },
  email: {
    type: String,
    required: [true, "Please enter email"],
  },
  address: {
    type: String,
    required: [true, "Please add an address."],
  },
  company: {
    type: String,
    required: [true, "Please add Company name."],
  },
  industry: {
    type: [String],
    required: [true, "Please enter industry for this job."],
    enum: {
      values: [
        "Business",
        "Information Technology",
        "Banking",
        "Education/Training",
        "Telecommunication",
        "Others",
      ],
      message: "Please select correct options for industry.",
    },
  },
  positions: {
    type: Number,
    default: 1,
  },
  salary: {
    type: Number,
    required: [true, "Please enter expected salary for this job."],
  },
  postingDate: {
    type: Date,
    default: Date.now,
  },
  user: {
    type: mongoose.Schema.ObjectId,
    ref: "User",
    required: true,
  },
});

// Create a model only for testing purposes (no DB connection needed for validateSync)
const Job = mongoose.model('JobTest', jobSchema);

describe('Job Model Unit Tests (Validation Logic)', () => {
  
  // Helper to get valid data
  const getValidData = () => ({
    title: 'Developer',
    description: 'Code stuff',
    email: 'dev@example.com',
    address: '123 Main St',
    company: 'Tech Co',
    industry: ['Information Technology'],
    salary: 100000,
    user: new mongoose.Types.ObjectId(),
  });

  test('should be valid with all required fields', () => {
    const job = new Job(getValidData());
    const error = job.validateSync();
    expect(error).toBeUndefined();
  });

  test('should fail validation if title is missing', () => {
    const data = getValidData();
    delete data.title;
    const job = new Job(data);
    const error = job.validateSync();
    
    expect(error).toBeDefined();
    expect(error.errors.title.message).toBe("Please enter Job title.");
  });

  test('should fail validation if title is too long', () => {
    const data = getValidData();
    data.title = 'a'.repeat(101);
    const job = new Job(data);
    const error = job.validateSync();
    
    expect(error).toBeDefined();
    expect(error.errors.title.message).toBe("Job title can not exceed 100 characters.");
  });

  test('should trim title', () => {
    const data = getValidData();
    data.title = '  Developer  ';
    const job = new Job(data);
    
    // Mongoose trim happens during save/set, but validateSync checks current state
    // To test trim effectively, we check the value after setting
    job.title = '  Developer  ';
    expect(job.title).toBe('Developer');
  });

  test('should fail validation if description is missing', () => {
    const data = getValidData();
    delete data.description;
    const job = new Job(data);
    const error = job.validateSync();
    
    expect(error).toBeDefined();
    expect(error.errors.description.message).toBe("Please enter Job description.");
  });

  test('should fail validation if email is missing', () => {
    const data = getValidData();
    delete data.email;
    const job = new Job(data);
    const error = job.validateSync();
    
    expect(error).toBeDefined();
    expect(error.errors.email.message).toBe("Please enter email");
  });

  test('should fail validation if address is missing', () => {
    const data = getValidData();
    delete data.address;
    const job = new Job(data);
    const error = job.validateSync();
    
    expect(error).toBeDefined();
    expect(error.errors.address.message).toBe("Please add an address.");
  });

  test('should fail validation if company is missing', () => {
    const data = getValidData();
    delete data.company;
    const job = new Job(data);
    const error = job.validateSync();
    
    expect(error).toBeDefined();
    expect(error.errors.company.message).toBe("Please add Company name.");
  });

  test('should fail validation if industry is missing', () => {
    const data = getValidData();
    delete data.industry;
    const job = new Job(data);
    const error = job.validateSync();
    
    expect(error).toBeDefined();
    expect(error.errors.industry.message).toBe("Please enter industry for this job.");
  });

  test('should fail validation if industry has invalid enum value', () => {
    const data = getValidData();
    data.industry = ['Invalid Industry'];
    const job = new Job(data);
    const error = job.validateSync();
    
    expect(error).toBeDefined();
    expect(error.errors.industry.message).toBe("Please select correct options for industry.");
  });

  test('should pass validation with valid enum values', () => {
    const data = getValidData();
    data.industry = ['Business', 'Banking'];
    const job = new Job(data);
    const error = job.validateSync();
    
    expect(error).toBeUndefined();
  });

  test('should set default positions to 1', () => {
    const data = getValidData();
    delete data.positions;
    const job = new Job(data);
    
    expect(job.positions).toBe(1);
  });

  test('should fail validation if salary is missing', () => {
    const data = getValidData();
    delete data.salary;
    const job = new Job(data);
    const error = job.validateSync();
    
    expect(error).toBeDefined();
    expect(error.errors.salary.message).toBe("Please enter expected salary for this job.");
  });

  test('should set default postingDate', () => {
    const data = getValidData();
    delete data.postingDate;
    const job = new Job(data);
    
    expect(job.postingDate).toBeDefined();
    expect(job.postingDate instanceof Date).toBe(true);
  });

  test('should fail validation if user is missing', () => {
    const data = getValidData();
    delete data.user;
    const job = new Job(data);
    const error = job.validateSync();
    
    expect(error).toBeDefined();
    expect(error.errors.user.message).toMatch(/Path `user` is required/);
  });
});
```

### Key Differences from Integration Tests

1.  **No Database Connection**: We do not connect to MongoDB. We use `validateSync()`, which runs Mongoose's validation logic entirely in memory.
2.  **Schema Duplication**: To keep this a true *unit* test (isolated from the implementation file's imports/mocks), I duplicated the schema definition in the test file. 
    *   *Best Practice Refactor*: In your actual `models/Job.js`, export the schema separately:
        ```javascript
        const jobSchema = new mongoose.Schema({...});
        module.exports = { Job: mongoose.model('Job', jobSchema), jobSchema };
        ```
    *   Then, in your test, you can `require('../models/Job').jobSchema` and create a test model from it, ensuring DRY (Don't Repeat Yourself) principles while maintaining unit isolation.
3.  **Speed**: These tests run almost instantly because there is no I/O.
4.  **`validateSync()`**: This method is key for unit testing. It returns a `ValidationError` object if validation fails, or `undefined` if it passes, allowing for easy Jest assertions.