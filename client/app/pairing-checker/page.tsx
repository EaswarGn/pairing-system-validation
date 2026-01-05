'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
const win_index = 403;

export default function PairingChecker() {
    const [file, setFile] = useState(null);
    const [currentIndex, setCurrentIndex] = useState(() => {
        // Retrieve the index from localStorage or default to 1
        return parseInt(localStorage.getItem('currentIndex'));
    });
    const [testCase, setTestCase] = useState(null);
    const [uploadStatus, setUploadStatus] = useState('');
    const [gameOver, setGameOver] = useState(false);
    const [testCaseStatus, setTestCaseStatus] = useState('');
    const [gameWin, setGameWin] = useState(false);

    const fetchTestCase = useCallback(async () => {
        try {
            if (currentIndex == win_index && !gameOver) {
                setGameWin(true);
            }
            else {
                const response = await fetch(`http://127.0.0.1:5000/testcase?index=${currentIndex}`);
                if (response.ok) {
                    const blob = await response.blob();
                    setTestCase(blob);
                    setUploadStatus(testCaseStatus + `\n\nTest case ${currentIndex} fetched successfully. You can now download it.`);
                } else {
                    throw new Error('Failed to fetch test case');
                }
            }
        } catch (error) {
            console.error('Error fetching test case:', error);
            setUploadStatus('Error fetching test case');
        }
    }, [currentIndex]);

    useEffect(() => {
        if (!gameOver) {
            fetchTestCase();
        }
    }, [currentIndex, gameOver, fetchTestCase]);

    useEffect(() => {
        // Save the currentIndex to localStorage whenever it changes
        localStorage.setItem('currentIndex', currentIndex);
    }, [currentIndex]);

    const onDrop = useCallback((acceptedFiles) => {
        if (acceptedFiles.length > 0) {
            setFile(acceptedFiles[0]);
        }
    }, []);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'application/json': ['.json'],
            'text/csv': ['.csv'],
            'text/plain': ['.trf'],
        },
        maxFiles: 1,
    });

    const uploadFile = async () => {
        if (!file) {
            setUploadStatus('No file to upload');
            return;
        }
    
        const formData = new FormData();
        formData.append('file', file);
        formData.append('index', currentIndex);
    
        try {
            const response = await fetch('http://127.0.0.1:5000/pairings', {
                method: 'POST',
                body: formData,
            });
            
            // Check if the response is OK
            if (response.ok) {
                // Parse the JSON data from the response
                const data = await response.json();
    
                // Log the data to the console (or handle it as needed)
                console.log('Response data:', data);
    
                // Handle the response data
                if (data[0][0]) { // Adjust this check based on the actual structure of your response
                    setTestCaseStatus('Solution correct! Moving to next test case.\n');
                    setCurrentIndex(prevIndex => prevIndex + 1);
                    setFile(null);
                } else {
                    let reason = data[0][1];
                    setTestCaseStatus(reason);
                    //setUploadStatus('Incorrect solution.\n' + reason + '\nGame over.\n  ');
                    setGameOver(true);
                    //delete localStorage.currentIndex;
                }
            } else {
                throw new Error('Failed to upload file');
            }
        } catch (error) {
            setUploadStatus('Error uploading file');
            console.error('Upload error:', error);
        }
    };
    
    const downloadTestCase = () => {
        if (testCase) {
            const url = window.URL.createObjectURL(testCase);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = `testcase_${currentIndex}.json`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        }
    };

    if (gameOver) {
        return (
            <div className="w-screen h-screen flex flex-col items-center justify-center bg-gray-100">
                <h1 className="text-3xl font-bold mb-8">Game Over</h1>
                <center>Test case {currentIndex} failed <br></br>
                {testCaseStatus}<br></br>
                Better luck next time!</center>
            </div>
        );
    }

    if (gameWin) {
        return ( // TODO: Add USCF Logo, Add license/validation key/number
            <div className="w-screen h-screen flex flex-col items-center justify-center bg-gray-100">
                <h1 className="text-3xl font-bold mb-8">Software Validated</h1>
                <center> Congratulations <br></br>
                All test cases passed.<br></br>
                You may publish your software declared as USCF-validated</center> 
            </div>
        );
    }

    return (
        <div className="w-screen h-screen flex flex-col items-center justify-center bg-gray-100">
            <h1 className="text-3xl font-bold mb-8 transition-transform duration-300 hover:scale-105">
                Test Case {currentIndex}
            </h1>

            <div className="w-96 bg-white p-6 rounded-xl shadow-md">
                <button 
                    onClick={downloadTestCase}
                    className="w-full px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 transition-colors duration-300 mb-4"
                >
                    Download Test Case
                </button>

                <div 
                    {...getRootProps()} 
                    className="border-2 border-dashed border-gray-300 rounded-lg p-4 mb-4 text-center cursor-pointer transition-colors duration-300 hover:border-blue-500"
                >
                    <input {...getInputProps()} />
                    {isDragActive ? (
                        <p className="text-blue-500">Drop the solution file here ...</p>
                    ) : (
                        <p>Drag and drop your solution file here, or click to select a file</p>
                    )}
                </div>

                {file && (
                    <div className="mb-4">
                        <h4 className="font-semibold">File:</h4>
                        <p className="text-sm">{file.name}</p>
                    </div>
                )}

                <button 
                    onClick={uploadFile}
                    className="w-full px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors duration-300"
                >
                    Submit Solution
                </button>

                {uploadStatus && (
                    <p className={`mt-4 text-center ${uploadStatus.includes('Error') || uploadStatus.includes('Incorrect') ? 'text-red-500' : 'text-green-500'}`}>
                        {uploadStatus}
                    </p>
                )}
            </div>
        </div>
    );
}
