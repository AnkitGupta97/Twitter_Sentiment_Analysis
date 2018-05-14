const express = require('express');
const router = express.Router();
const TwitterQuery = require("../models/tweetQuery");
const request = require('request');


//retreiving data
router.get('/twitterQueries', (req, res, next) => {
    // "Retrieving the earlier searched"
    TwitterQuery.find(function (err, twitterQueries) {
        res.json(twitterQueries);
    });
});

//add data
router.post('/twitterQuery', (req, res, next) => {
    //logic to add twitter query
    let newQuery = new TwitterQuery({
        query: req.body.query,
        created: req.body.created || new Date().getDate(),
        positive: req.body.positive,
        negative: req.body.negative,
        neutral: req.body.neutral
    });
    newQuery.save((err, newQuery) => {
        if (err) {
            res.json({ msg: " Failed to add query" });
        }
        else {
            res.json({ msg: " query added successfully" });
        }
    });
});

//search query
router.post('/searchQuery', (req, res, next) => {
    //logic to delete query
    var queryName = req.body.query;
    console.log("inside express api : query :" + queryName);
    request.post(
        'http://localhost:5000/startquery',
        { json: { "query": queryName } },
        function (error, response, body) {
            if (error) {
                console.log(error)
            }
            else {
                console.log(body);
                var dataQuery = body;
                if(dataQuery["query"]){
                    let newQuery = new TwitterQuery({
                        query: dataQuery["query"],
                        created: dataQuery["created"] || new Date().getDate(),
                        positive: dataQuery["positive"],
                        negative: dataQuery["negative"],
                        neutral: dataQuery["neutral"]
                    });
                    newQuery.save((err, newQuery) => {
                        if (err) {
                            res.json({ msg: " Failed to add query" });
                        }
                        else {
                            res.json(dataQuery);
                        }
                    });
                }
            }
        }
    );
});

//delete query
router.delete('/querydelete/:id', (req, res, next) => {
    //logic to delete query
    TwitterQuery.remove({ _id: req.params.id }, function (err, result) {
        if (err) {
            res.json({ msg: "unable to delete twitter query" });
        }
        else {
            res.json({ msg: "Twitter Query deleted successfully" });
        }
    });
});


module.exports = router;