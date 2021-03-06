//importing modules
var express = require ('express');
var mongoose = require ('mongoose');
var bodyparser = require ('body-parser');
var cors = require('cors');
var path = require ('path');

var app = express();

const route = require("./routes/routes");

//port no.
const port = 3000;

//connect to mongo 
mongoose.connect("mongodb://localhost:27017/twitterAnalysis");

mongoose.connection.on("connected",()=>{
    console.log("Connected to database mongodb@27017");   
   })

mongoose.connection.on("error",(err)=>{   
 console.log("Error connecting to database : "+ err);   
})
   
//adding middleware - cors
app.use(cors());

//body -parser
app.use(bodyparser.json());

//static files
app.use(express.static(path.join(__dirname,"public")));

//routes
app.use('/api',route);

//testing Server
app.get("/",(req,res)=>{
    res.send("contact list server ")
});

app.listen(port,()=>{
    console.log("Server started at port :"+port);
});