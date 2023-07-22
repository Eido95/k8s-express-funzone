const express = require('express')
const { execSync } = require('child_process')
const https = require('https');
const path = require('path');
const morgan = require('morgan')

const app = express()
const port = 4000

app.use(morgan('dev'))

app.get('/', (request, response) => {
  https.get('https://uselessfacts.jsph.pl/api/v2/facts/random', (incomingMessage) => {
    incomingMessage.on('data', (body) => {
      response.send(getResponseBody(body))
    });

  }).on('error', (error) => {
    console.error(error);
  });
})

app.use((request, response, next) => {
  response.status(404).send(`Sorry can't find that! ${JSON.stringify(getResponseBody(null))}`)
})

app.listen(port, () => {
  console.log(`k8s Express Fun Zone uselessfacts app listening on port ${port}`)
})

function run(command) {
  return execSync(command).toString().trim();
}

function getResponseBody(uselessfactsBody) {
  return {
    "app": path.basename(module.filename),
    "hostname": run("hostname"),
    "ips": run("hostname -I"),
    "uselessfacts": uselessfactsBody ? JSON.parse(uselessfactsBody).text : null
    }
}