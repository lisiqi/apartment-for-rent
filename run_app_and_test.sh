#!/bin/bash

# Set PYTHONPATH to include the project root directory and src directory
export PYTHONPATH=$(pwd):$(pwd)/src:$PYTHONPATH

# Run the Flask app in the background using poetry
poetry run python app.py &

# Capture the PID of the Flask app process
FLASK_PID=$!

# Wait for a few seconds to ensure the server is up
sleep 5

# Test the prediction endpoint using curl
curl -X POST -H "Content-Type: application/json" -d '{
    "category":"housing\/rent\/apartment","title":"Lithonia, prime location Two BR, Apartment","body":"Square footage: 1054 sq-ft, unit number: 4307. Located in Lithonia, Georgia, Creekside Corners is just 15 mis east of Downtown Atlanta. Close to a variety of shops, restaurants, grocery stores, and Interstate 20, Creekside Corners offers a quiet, high-end apartment community minutes from everything you need. Our tree-filled property contains a swimming pool, a car care center, a play-area, a picnic area with BBQ grill, and a state-of-the-art fitness facilities. Heavily wooded and featuring a historic district, Lithonia provides a beautiful setting with easy commutes into the city via Interstate 20 and Interstate 285. Creekside Corners is in a neighborhood filled with shops and restaurants, many within walkable distance. We re also convenient to Hartsfield-Jackson International Airport, Panola Mountain State Park, and Stone Mountain Park. We provide 6 floor plans so you can find the ideal one-, two-, or 3 beds for your lifestyle.","amenities":"Fireplace,Gated,Gym,Parking,Patio\/Deck,Playground,Pool,Storage,Washer Dryer","bathrooms":2.0,"bedrooms":2.0,"currency":"USD","fee":"No","has_photo":"Thumbnail","pets_allowed":"Cats,Dogs","price_display":1060.0,"price_type":"Monthly","square_feet":1054.0,"address":null,"cityname":"Lithonia","state":"GA","latitude":33.6795,"longitude":-84.1596,"source":"RentDigs.com","time":1568773334.0
    }' http://127.0.0.1:5000/predict

# Kill the Flask app process
pkill -f "poetry run python app.py"
# kill $FLASK_PID
