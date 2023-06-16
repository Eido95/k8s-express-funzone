const express = require('express')
const { execSync } = require('child_process')
const path = require('path');

const uselessfacts = require('./uselessfacts')

const app = express()
const port = 3000

app.get('/', (request, response) => {
  response.send({
    "app": path.basename(module.filename),
    "hostname": run("hostname"),
    "ips": run("hostname -I")
    })
})

app.listen(port, () => {
  console.log(`K8s Express Fun Zone app listening on port ${port}`)
})

function run(command) {
  return execSync(command).toString().trim();
}