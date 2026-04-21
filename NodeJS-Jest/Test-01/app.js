const crypto = require('node:crypto')

async function getData() {
    return crypto.randomBytes(20)
}

module.exports = {
    getData,
}