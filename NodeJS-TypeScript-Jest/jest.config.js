const { createDefaultPreset } = require("ts-jest");

const tsJestTransformCfg = createDefaultPreset().transform;

const baseDir = '<rootDir>\\\\src\\\\app\\\\password_checker'
const baseTestDir = '<rootDir>\\\\src\\\\__tests__\\\\password_checker'

/** @type {import("jest").Config} **/
module.exports = {
  testEnvironment: "node",
  transform: {
    ...tsJestTransformCfg,
  },
  testMatch: [
    `${baseTestDir}\\\\*.spec.ts`,
  ],
  coveragePathIgnorePatterns: [
    "\\\\node_modules\\\\",
  ],

  collectCoverage: true,
  collectCoverageFrom: [
    `${baseDir}\\\\*.ts`
  ],

  // Indicates which provider should be used to instrument code for coverage
  coverageProvider: "v8",

  // An object that configures minimum threshold enforcement for coverage results
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },

  coverageDirectory: 'coverage', // Default
  coverageReporters: ['text', 'lcov', 'html'], // Ensure reporters are set
};