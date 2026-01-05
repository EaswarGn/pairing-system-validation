//run nodemon index.js and then open testing/index.html to see how 
//the backend works, click the Start Validation button

const express = require('express');
const cors = require('cors');
const crypto = require('crypto');
const axios = require('axios');
const bodyParser = require('body-parser');

const app = express();
app.use(cors());
app.use(express.json());
const port = 3000;

// Array to hold connected clients
let clients = [];
let stop = false;

app.post('/restart', async (req, res) => {
    stop = false;
    await axios.post('http://localhost:3001/restart')
        .then(response => {
            if (response.data.is_stopped == true) {
                res.json({
                    restarted: true
                })
            }
            else {
                res.json({
                    restarted: false
                })
            }
        })
})

app.post('/startValidation', async (req, res) => {
    if (stop == true) {
        return;
    }

    let endpoint = req.body.endpoint;

    //will add actual test cases when they are available
    const test_cases = await get_test_cases();

    //temporary
    endpoint = 'http://localhost:3001/make_pairing'
    await axios.post('http://localhost:3001/intialize_solutions')

    let results = [];
    let total_wrong = 0;
    test_cases_not_passed = []
    for (let i = 1; i <= test_cases.length - 1; i++) {
        if (stop == true) {
            return;
        }
        const postData = {
            test_case: test_cases[i],
            index: i
        };

        await axios.post(endpoint, postData,
            {
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        )
            .then(response => {
                //validate the pairings and append the results
                const pairings = response.data.pairings;
                const postData = {
                    pairings: pairings,
                    index: i + 1
                };
                axios.post('http://127.0.0.1:5000/pairings', postData,
                    {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    }
                )
                    .then(response => {
                        if (response.data[0][0] !== true) {
                            total_wrong++;
                            results.push(response.data);
                            test_cases_not_passed.push(test_cases[i])
                        }
                        else {
                            results.push(response.data[0]);
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
            })
            .catch(error => {
                console.error('Error:', error);
            });

        clients.forEach(client => client.write(`data: ${JSON.stringify({ completed: i + 1, total: test_cases.length })}\n\n`));
        await new Promise(resolve => setTimeout(resolve, 100));
    }
    res.json({
        message: "Validation complete!",
        results: results,
        total_wrong: total_wrong,
        test_cases_not_passed: test_cases_not_passed
    })
})

// SSE endpoint to subscribe to progress updates
app.get('/progress', (req, res) => {
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');

    clients.push(res);

    req.on('close', () => {
        clients = clients.filter(client => client !== res);
    });
});

app.post('/stopValidation', async (req, res) => {
    stop = true;
    clients.forEach(client => client.end());
    clients = []
    await axios.post('http://localhost:3001/stop')
        .then(response => {
            if (response.data.is_stopped == true) {
                res.json({
                    is_stopped: true
                })
            }
            else {
                res.json({
                    is_stopped: false
                })
            }
        })
});


app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});


async function get_test_cases() {
    let url = "http://127.0.0.1:5000";
    const test_cases = [];
    for (let i = 1; i <= 402; i++) {
        try {
            endpoint = url + '/testcase' + '?index=' + i
            const response = await axios.get(endpoint);
            test_cases.push(response.data);
        } catch (error) {
            console.error('Error:', error);
        }
    }
    return test_cases;
}