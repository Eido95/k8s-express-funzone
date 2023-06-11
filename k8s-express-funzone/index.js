const express = require('express')
const app = express()
const port = 3000

app.get('/', (request, response) => {
  response.send('Fun Zone!')
})

app.listen(port, () => {
  console.log(`K8s Express Fun Zone app listening on port ${port}`)
})