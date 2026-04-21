const crypto = require('node:crypto')
const { getData } = require('../app')

test('testing spyOn', async () => {
    jest.spyOn(crypto, 'randomBytes').mockImplementationOnce(()=>Promise.resolve('JLoka'))

    const res = await getData()
    expect(res).toEqual('JLoka')
})