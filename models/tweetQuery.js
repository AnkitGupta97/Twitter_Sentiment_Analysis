const mongoose = require('mongoose');

const twitterQuerySchema = mongoose.Schema({
    query:{
        type: String,
        required : true
    }, 
    created: { type: Date, default: Date.now },
    positive:[String],
    negative:[String],
    neutral:[String]
});

const twitterQuery = module.exports  = mongoose.model("twitterQuery",twitterQuerySchema);