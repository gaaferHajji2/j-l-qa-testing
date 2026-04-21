const crypto = require('node:crypto')
const { getData } = require('../app')

jest.spyOn(crypto, 'randomBytes').mockImplementationOnce(()=>Promise.resolve('JLoka'))

test('testing spyOn', async () => {
    const t1 = await getData()
    expect(t1).toEqual('JLoka')
})