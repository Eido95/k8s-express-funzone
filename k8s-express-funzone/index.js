const express = require('express')
const { execSync } = require('child_process')

const app = express()
const port = 3000

app.get('/', (request, response) => {
  const hostname = run("hostname");
  const ip = run("hostname -I");
  response.send(`Fun Zone! (hostname: ${hostname}) (ip: ${ip})`);
})

app.listen(port, () => {
  console.log(`K8s Express Fun Zone app listening on port ${port}`)
})

function run(command) {
  return execSync(command).toString().trim();
}