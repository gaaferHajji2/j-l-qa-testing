const crypto = require('node:crypto')
const { getData } = require('../app')

jest.mock('node:crypto')

describe('test mocking', () => {
    it('Mocking function', async () => {
        crypto.randomBytes.mockResolvedValueOnce('bytes')
        const res = await getData()
        expect(res).toEqual('bytes')
    })

    it('Mocking function', async () => {
        crypto.randomBytes.mockImplementationOnce(() => Promise.resolve('bytes'))
        const res = await getData()
        expect(res).toEqual('bytes')
    })
})

describe('test spyOn', () => {
    it('testing spyOn', async () => {
        jest.spyOn(crypto, 'randomBytes').mockImplementationOnce(()=>Promise.resolve('JLoka'))
    
        const res = await getData()
        expect(res).toEqual('JLoka')
    })
})