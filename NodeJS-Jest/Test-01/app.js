const crypto = require('node:crypto')

function getData() {
    return crypto.randomBytes(20)
}

module.exports = {
    getData,
}