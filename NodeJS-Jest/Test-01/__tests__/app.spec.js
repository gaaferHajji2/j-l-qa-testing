const crypto = require('node:crypto')
const { getData } = require('../app')

jest.mock('node:crypto')

test('Mocking function', async () => {
    crypto.randomBytes.mockResolvedValueOnce('bytes')
    const res = await getData()
    expect(res).toEqual('bytes')
})

test('Mocking function', async () => {
    crypto.randomBytes.mockImplementationOnce(() => Promise.resolve('bytes'))
    const res = await getData()
    expect(res).toEqual('bytes')
})