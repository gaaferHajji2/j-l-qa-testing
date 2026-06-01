import jwt from 'jsonwebtoken'
import { getJwtToken } from './helpers'
import { sendEmail } from './helpers'
import nodemailer from 'nodemailer'

jest.mock('nodemailer');

describe("Test Helpers", () => {

  const ORIGINAL_ENV = process.env

  beforeEach(() => {
    // Create a shallow copy so mutations don't affect other tests
    process.env = { ...ORIGINAL_ENV }
    process.env.JWT_SECRET = 'Test@123'
    process.env.JWT_EXPIRES_TIME = '1w'
  });

  afterEach(() => {
    process.env = ORIGINAL_ENV
    jest.resetAllMocks()
  });

  it("Test JWT Token", async () => {
    jest.spyOn(jwt, 'sign').mockResolvedValueOnce('JLoka-Token')
    let id = "123"

    const token = await getJwtToken(id)

    expect(token).toBeDefined()
    expect(token).toBe('JLoka-Token')
    expect(jwt.sign).toHaveBeenCalledWith({ id }, 'Test@123', {
      expiresIn: '1w',
    })
  })
})

describe("Test the NodeMailer", () => {
  // Mock data
  const mockOptions = {
    email: 'test@example.com',
    subject: 'Test Subject',
    message: 'Test Message Body',
  };

  const mockTransporter = {
    sendMail: jest.fn(),
  };

  beforeEach(() => {
    // Reset mocks before each test
    jest.clearAllMocks();

    // Set up environment variables if needed for specific tests, 
    // though the mock bypasses the actual connection logic.
    process.env.SMTP_HOST = 'smtp.test.com';
    process.env.SMTP_PORT = '587';
    process.env.SMTP_EMAIL = 'user@test.com';
    process.env.SMTP_PASSWORD = 'password';

    nodemailer.createTransport.mockReturnValue(mockTransporter);
  })

  it('should create a transporter with correct configuration', async () => {
    // Call the function
    await sendEmail(mockOptions);

    // Assert that createTransport was called once
    expect(nodemailer.createTransport).toHaveBeenCalledTimes(1);

    // Assert it was called with the correct config
    expect(nodemailer.createTransport).toHaveBeenCalledWith({
      host: process.env.SMTP_HOST,
      port: process.env.SMTP_PORT,
      auth: {
        user: process.env.SMTP_EMAIL,
        pass: process.env.SMTP_PASSWORD,
      },
    });
  });

  it('should call sendMail with the correct message options', async () => {
    // Mock the resolution of sendMail
    mockTransporter.sendMail.mockResolvedValue({ messageId: '12345' });

    // Call the function
    await sendEmail(mockOptions);

    // Assert that sendMail was called on the transporter
    expect(mockTransporter.sendMail).toHaveBeenCalledTimes(1);

    // Assert the message object passed to sendMail is correct
    expect(mockTransporter.sendMail).toHaveBeenCalledWith({
      from: 'noreply@test.com',
      to: mockOptions.email,
      subject: mockOptions.subject,
      text: mockOptions.message,
    });
  });

    it('should return the response from sendMail', async () => {
    // Mock the resolution of sendMail
    const mockResponse = { messageId: 'abcde', response: '250 OK' };
    mockTransporter.sendMail.mockResolvedValue(mockResponse);

    // Call the function
    const result = await sendEmail(mockOptions);

    // Assert the returned value matches the mock response
    expect(result).toEqual(mockResponse);
  });

  it('should throw an error if sendMail fails', async () => {
    // Mock the rejection of sendMail
    const mockError = new Error('Network Error');
    mockTransporter.sendMail.mockRejectedValue(mockError);

    // Expect the async function to reject
    await expect(sendEmail(mockOptions)).rejects.toThrow('Network Error');
  });

})