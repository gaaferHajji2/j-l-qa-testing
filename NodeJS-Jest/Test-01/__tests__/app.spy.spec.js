const crypto = require('node:crypto')
const { getData } = require('../app')


test('testing spyOn', async () => {
    jest.spyOn(crypto, 'randomBytes').mockImplementationOnce(()=>Promise.resolve('JLoka'))

    const t1 = await getData()
    expect(t1).toEqual('JLoka')
})