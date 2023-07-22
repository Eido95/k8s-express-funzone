const express = require('express')
const { execSync } = require('child_process')
const path = require('path');
const morgan = require('morgan')

const uselessfacts = require('./uselessfacts')

const app = express()
const port = 3000

app.use(morgan('dev'))

app.get('/', (request, response) => {
  response.send(getResponseBody())
})

app.use((req, res, next) => {
  res.status(404).send(`Sorry can't find that! ${JSON.stringify(getResponseBody())}`)
})

app.listen(port, () => {
  console.log(`k8s Express Fun Zone app listening on port ${port}`)
})

function run(command) {
  return execSync(command).toString().trim();
}

function getResponseBody() {
  return {
    "app": path.basename(module.filename),
    "hostname": run("hostname"),
    "ips": run("hostname -I")
    }
}