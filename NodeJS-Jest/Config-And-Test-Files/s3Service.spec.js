import { S3Service } from './S3Service'; // Adjust path as needed

// 1. Create mock functions outside the jest.mock factory so we can access them in tests
const mockUploadPromise = jest.fn();
const mockUpload = jest.fn(() => ({
  promise: mockUploadPromise,
}));

// 2. Mock aws-sdk
jest.mock('aws-sdk', () => {
  return {
    S3: jest.fn().mockImplementation(() => ({
      upload: mockUpload,
    })),
  };
});

// 3. Import S3 from aws-sdk just to satisfy imports if needed, 
// but we primarily rely on the mocks defined above.
import pkg from 'aws-sdk';
const { S3 } = pkg;

describe('S3Service', () => {
  let s3Service;

  beforeEach(() => {
    // Clear all mock calls and instances
    jest.clearAllMocks();

    // Reset environment variables
    process.env.AWS_ACCESS_KEY_ID = 'test-access-key';
    process.env.AWS_SECRET_KEY = 'test-secret-key';
    process.env.AWS_S3_BUCKET_NAME = 'test-bucket';

    // Reset mock implementations to default success
    mockUploadPromise.mockResolvedValue({
      Location: 'https://test-bucket.s3.amazonaws.com/restaurants/test-file.jpg',
      ETag: '"some-etag"',
    });

    // Instantiate the service
    s3Service = new S3Service();
  });

  afterEach(() => {
    delete process.env.AWS_ACCESS_KEY_ID;
    delete process.env.AWS_SECRET_KEY;
    delete process.env.AWS_S3_BUCKET_NAME;
  });

  it('should initialize S3 with correct credentials', () => {
    // Verify S3 constructor was called with correct config
    expect(S3).toHaveBeenCalledWith({
      accessKeyId: 'test-access-key',
      secretAccessKey: 'test-secret-key',
    });
  });

  it('should upload a file to the correct S3 bucket and path', async () => {
    const mockFile = {
      name: 'test-file.jpg',
      data: Buffer.from('file content'),
    };

    await s3Service.upload(mockFile);

    // Verify upload method was called
    expect(mockUpload).toHaveBeenCalledTimes(1);

    // Verify correct parameters were passed
    expect(mockUpload).toHaveBeenCalledWith({
      Bucket: 'test-bucket/restaurants',
      Key: 'test-file.jpg',
      Body: mockFile.data,
    });
  });

  it('should return the upload result', async () => {
    const mockFile = {
      name: 'test-file.jpg',
      data: Buffer.from('file content'),
    };

    const result = await s3Service.upload(mockFile);

    // Verify the promise was called
    expect(mockUploadPromise).toHaveBeenCalled();

    // Verify the result
    expect(result).toEqual({
      Location: 'https://test-bucket.s3.amazonaws.com/restaurants/test-file.jpg',
      ETag: '"some-etag"',
    });
  });

  it('should handle upload errors', async () => {
    const mockFile = {
      name: 'test-file.jpg',
      data: Buffer.from('file content'),
    };

    // Simulate an error
    const mockError = new Error('Upload failed');
    mockUploadPromise.mockRejectedValueOnce(mockError);

    // Expect the service method to throw/reject
    await expect(s3Service.upload(mockFile)).rejects.toThrow('Upload failed');
  });
});