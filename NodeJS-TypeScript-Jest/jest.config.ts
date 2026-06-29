import type { Config } from "jest"

const config: Config = {

// Use the ts-jest preset to seamlessly process TypeScript files
  preset: 'ts-jest',

  // Specify the test environment (use 'jsdom' if you are building front-end apps like React)
  testEnvironment: 'node',

  verbose: true,

  // The directory where Jest should look for your test files
  roots: ['<rootDir>/src'],

  // Explicitly match test file patterns (.test.ts, .spec.ts, .test.tsx, etc.)
  testMatch: [
    '**/__tests__/**/*.+(ts|tsx|js)',
    '**/?(*.)+(spec|test).+(ts|tsx|js)'
  ],

  // A map from regular expressions to paths to transformers
  transform: {
    '^.+\\.(ts|tsx)$': ['ts-jest', {
      // Point ts-jest to a specific tsconfig if necessary
      tsconfig: 'tsconfig.json',
    }],
  },

  // Enable code coverage collection out-of-the-box
  collectCoverage: true,
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov'],
};

export default config;