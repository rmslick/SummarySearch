const express = require('express');
const bodyParser = require('body-parser');
const app = express();

app.use(bodyParser.urlencoded({extended: true}));
app.post('/description', (req, res) => {
  res.send(`Project description is: ${req.body.projectDescription}.`); });
const port = 8080;

app.listen(port, ()=> { console.log(`Server running on port ${port}`)});

var count = 1;
function SearchIconClick()
{
  var iconProperty = document.getElementById("searchIcon");
  if(count == 0)
  {
    iconProperty.style.color =  #6CC417;
    count = 1;
  }
  else
  {
    iconProperty.style.color = #43BFC7;
    count = 0;
  }

}
