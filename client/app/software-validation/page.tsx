'use client'

import React, { useState, useEffect, ChangeEvent, FormEvent } from 'react';

export default function SoftwareValidation() {
    const [endpoint, setEndpoint] = useState<string>('');
    const [isValidationStarted, setIsValidationStarted] = useState<boolean>(false);
    const [progress, setProgress] = useState<number>(0);
    const [results, setResults] = useState<any[]>([]); // Store validation results here
    const [isDownloadReady, setIsDownloadReady] = useState<boolean>(false); // Track if the download is ready

    const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
        setEndpoint(e.target.value);
    };

    const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setIsValidationStarted(true);
        setProgress(0);
        setIsDownloadReady(false);
        startValidation(endpoint, setProgress, setResults);
    };

    const handleStopValidation = () => {
        setIsValidationStarted(false);
        setProgress(0);
        setResults([]);
        stopValidation();
    };

    const handleDownload = () => {
        const blob = new Blob([JSON.stringify(results, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'validation_results.json';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    };

    useEffect(() => {
        let intProgress = Math.floor(progress)
        console.log(intProgress)
        if (intProgress === 100) {
            console.log("yes")
            console.log(results)
            setIsDownloadReady(true);
        }
    }, [progress]);

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-100">
            <form onSubmit={handleSubmit} className="bg-white p-8 rounded-lg shadow-lg max-w-md w-full">
                <h2 className="text-2xl font-semibold mb-6 text-gray-800 text-center">Enter Your API Endpoint</h2>
                <div className="mb-4">
                    <label htmlFor="endpoint" className="block text-gray-700 font-bold mb-2">
                        API Endpoint:
                    </label>
                    <input
                        type="text"
                        id="endpoint"
                        value={endpoint}
                        onChange={handleInputChange}
                        placeholder="https://api.example.com/endpoint"
                        className="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                </div>
                <button
                    type="submit"
                    className="w-full bg-blue-500 text-white p-3 rounded-lg font-semibold hover:bg-blue-600 transition duration-300"
                >
                    Submit
                </button>
                {isValidationStarted && (
                    <>
                        <button
                            type="button"
                            onClick={handleStopValidation}
                            className="w-full mt-4 bg-red-500 text-white p-3 rounded-lg font-semibold hover:bg-red-600 transition duration-300"
                        >
                            Stop Validation
                        </button>
                        <div className="relative pt-4">
                            <div className="overflow-hidden h-4 mb-4 text-xs flex rounded bg-green-200">
                                <div
                                    style={{ width: `${progress}%` }}
                                    className="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-green-500 transition-all duration-300"
                                >
                                    {progress}%
                                </div>
                            </div>
                        </div>
                    </>
                )}
                {isDownloadReady && (
                    <button
                        type="button"
                        onClick={handleDownload}
                        className="w-full mt-4 bg-green-500 text-white p-3 rounded-lg font-semibold hover:bg-green-600 transition duration-300"
                    >
                        Download Results
                    </button>
                )}
            </form>
        </div>
    );
}




let total = 0;

async function startValidation(endpoint, setProgress, setResults) {
    //temporary mock endpoint
    endpoint = "http://localhost:3001"

    if (endpoint !== "") {
        await fetch('http://localhost:3000/restart', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json' // Specify the content type as JSON
            },
        })
            .then(response => response.json())
        fetch('http://localhost:3000/startValidation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json' // Specify the content type as JSON
            },
            body: JSON.stringify({
                endpoint: endpoint
            })
        })
            .then(response => response.json())
            .then(data => {
                setResults(data)
            })
            .catch(error => console.error('Error:', error));
    }
    connectToProgressEndpoint(setProgress);
}


async function stopValidation() {
    // Function to disconnect from the SSE endpoint
    disconnectFromProgressEndpoint();
    fetch('http://localhost:3000/stopValidation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json' // Specify the content type as JSON
        },
    })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));
}

let eventSource = ""

function disconnectFromProgressEndpoint() {
    if (eventSource) {
        eventSource.close(); // Close the SSE connection
    }
}

function connectToProgressEndpoint(setProgress) {
    eventSource = new EventSource('http://localhost:3000/progress');

    eventSource.onmessage = function (event) {
        const progress = JSON.parse(event.data);
        total = progress.total;
        let percent = ((progress.completed / progress.total) * 100).toFixed(2);
        setProgress(percent)
    };

    // eventSource.onerror = function (event) {
    //     console.error('Connection to /progress lost. Attempting to reconnect in 3 seconds...');
    //     eventSource.close(); // Close the current connection
    //     setTimeout(connectToProgressEndpoint, 3000); // Attempt to reconnect after 3 seconds
    // };
}
