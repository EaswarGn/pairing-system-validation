if ! command -v tmux &> /dev/null
then
    echo "tmux is not installed. Installing..."
    brew install tmux
else
    echo "tmux is already installed."
fi

cd server
npm install
cd ..
cd client
npm install
cd ..

if pip install -r requirements.txt; then
    echo "Packages installed successfully with pip."
else
    echo "pip failed. Trying pip3..."
    if pip3 install -r requirements.txt; then
        echo "Packages installed successfully with pip3."
    else
        echo "Both pip and pip3 failed to install the packages."
        exit 1
    fi
fi


tmux new-session -d -s mysession -n checker 'cd checker && python app.py'

tmux new-window -t mysession:1 -n server 'cd server && nodemon index.js'

tmux new-window -t mysession:2 -n test_server 'cd server && nodemon test_server.js'

tmux new-window -t mysession:3 -n client 'cd client && npm run dev'

tmux attach -t mysession

