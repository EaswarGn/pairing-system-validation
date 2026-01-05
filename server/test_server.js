/*
Mock server that should act like the client. 
Made this in order to test the main server.
*/

const express = require('express');
const cors = require('cors');
const crypto = require('crypto');
const axios = require('axios');
const bodyParser = require('body-parser');
const fs = require('fs');

const app = express();
app.use(cors());
app.use(express.json());
const port = 3001;

let solutions = []
let stop = false;

//don't view this for reference, this endpoint was made purely for testing purposes
//it simply gets a list of response objects to send to the server for validation
app.post('/intialize_solutions', async (req, res) => {
    if (stop == true) {
        return;
    }
    const jsonString = fs.readFileSync('solutions.json', 'utf8');
    solutions = JSON.parse(jsonString);
    res.json({
        is_done: true
    })
})

//don't view this for reference, this endpoint was made purely for testing purposes
//this endpoint simply terminates all endpoints that are executing
app.post('/stop', async (req, res) => {
    stop = true;
    res.json({
        is_stopped: true
    })
});

//don't view this for reference, this endpoint was made purely for testing purposes
//this endpoint simply restarts the endpoints after termination
app.post('/restart', async (req, res) => {
    stop = false;
    res.json({
        is_stopped: false
    })
});


app.post('/make_pairing', async (req, res) => {
    if (stop == true) {
        return;
    }
    let index = req.body.index;
    index = gen_rand_index(0.2, index);
    res.json({
        pairings: solutions[index]
    });
})

function gen_rand_index(probability, index) {
    // Ensure the probability is between 0 and 1
    if (probability < 0 || probability > 1) {
        throw new Error('Probability must be between 0 and 1');
    }

    // Generate a random number between 0 and 1
    const randomNumber = Math.random();

    if (randomNumber < probability) {
        return 2;
    }

    // Return true if the random number is less than the given probability
    return index;
}


app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});



