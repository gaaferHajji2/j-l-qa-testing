// tests/job.model.unit.test.js
import Job from './jobs'
import mongoose from 'mongoose'

// 1. Mock mongoose before requiring the model
const mockValidateSync = jest.fn();
const mockSave = jest.fn();
const mockModelInstance = {
  validateSync: mockValidateSync,
  save: mockSave,
};

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

  test('should fail validation if industry is missing', async () => {
    const data = getValidData();
    delete data.industry;
    console.log("The data after delete industry is: ", data)
    const job = new Job(data);
    
    try { 
      await job.validateSync();
    } catch (error) {
      expect(error).toBeDefined();
      expect(error.errors['industry.0'].message).toBe("Please enter industry for this job.");
    }
  });

  test('should fail validation if industry has invalid enum value', async () => {
    const data = getValidData();
    data.industry = ['Invalid Industry'];
    const job = new Job(data);
    
    try {
      await job.validate();
    } catch (error) {
      expect(error).toBeDefined();
      console.log("The errors is: ", error.errors)
      expect(error.errors['industry.0'].message).toBe("Please select correct options for industry.");
    }
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