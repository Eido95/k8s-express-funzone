const express = require('express')
const { execSync } = require('child_process')
const https = require('https');
const path = require('path');

const app = express()
const port = 4000

app.get('/', (request, response) => {
  https.get('https://uselessfacts.jsph.pl/api/v2/facts/random', (incomingMessage) => {
    incomingMessage.on('data', (body) => {
      response.send({
        "app": path.basename(module.filename),
        "hostname": run("hostname"),
        "ips": run("hostname -I"),
        "uselessfacts": JSON.parse(body).text 
        })
    });

  }).on('error', (error) => {
    console.error(error);
  });
})

app.listen(port, () => {
  console.log(`K8s Express Fun Zone uselessfacts app listening on port ${port}`)
})

function run(command) {
  return execSync(command).toString().trim();
}

