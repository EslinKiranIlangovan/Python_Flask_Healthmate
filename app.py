from flask import Flask, render_template_string, request
import openai

app = Flask(__name__)

# Set your OpenAI API key here
OPENAI_API_KEY = "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"

# Initialize the OpenAI client
openai.api_key = OPENAI_API_KEY

# Define route for the index page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the form data submitted by the user
        age = request.form['age']
        weight = request.form['weight']
        veg_or_nonveg = request.form['veg_or_nonveg']
        region = request.form['region']
        food_type = request.form['food_type']
        gender = request.form['gender']
        height = request.form['height']
        generic_diseases = request.form.get('generic_diseases', '')
        allergies = request.form.get('allergies', '')

        # Prepare the user data to be sent to the OpenAI API
        user_data = {
            "model": "gpt-3.5-turbo-instruct",
            "prompt": f"My age is {age}, my weight is {weight} kg. I am {veg_or_nonveg}. I'm from {region}. My food type is {food_type}. My gender is {gender}. My height is {height} cm. I {'have' if generic_diseases else 'do not have'} any generic diseases. I {'have' if allergies else 'do not have'} any allergies. Give me a diet and workout plan for me.",
            "max_tokens": 150
        }

        # Make a request to the OpenAI API
        api_response = openai.Completion.create(**user_data)

        # Process the API response as needed
        return api_response.choices[0].text.strip()

    # If it's a GET request, render the HTML template
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HealthMate - Diet and Workout Recommendations</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            margin: 0;
            padding: 0;
        }

        .container {
            max-width: 600px;
            margin: 50px auto;
            background-color: #fff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        h1 {
            text-align: center;
            color: #333;
        }

        label {
            font-weight: bold;
            color: #666;
        }

        input[type="text"],
        select {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ccc;
            border-radius: 5px;
            box-sizing: border-box;
        }

        input[type="submit"] {
            width: 100%;
            background-color: #4CAF50;
            color: white;
            padding: 14px 20px;
            margin: 8px 0;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }

        input[type="submit"]:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>HealthMate - Diet and Workout Recommendations</h1>
        <form action="/" method="post">
            <label for="age">Age:</label>
            <input type="text" id="age" name="age" required>
            
            <label for="weight">Weight:</label>
            <input type="text" id="weight" name="weight" required>
            
            <label for="veg_or_nonveg">Vegetarian/Non-vegetarian:</label>
            <select id="veg_or_nonveg" name="veg_or_nonveg" required>
                <option value="vegetarian">Vegetarian</option>
                <option value="non-vegetarian">Non-vegetarian</option>
            </select>
            
            <label for="region">Region:</label>
            <input type="text" id="region" name="region" required>
            
            <label for="food_type">Food Type:</label>
            <input type="text" id="food_type" name="food_type" required>
            
            <label for="gender">Gender:</label>
            <select id="gender" name="gender" required>
                <option value="male">Male</option>
                <option value="female">Female</option>
            </select>
            
            <label for="height">Height:</label>
            <input type="text" id="height" name="height" required>
            
            <label for="generic_diseases">Generic Diseases (if any):</label>
            <input type="text" id="generic_diseases" name="generic_diseases">
            
            <label for="allergies">Allergies (if any):</label>
            <input type="text" id="allergies" name="allergies">
    
            <input type="submit" value="Submit">
        </form>
    </div>
</body>
</html>
""")

if __name__ == '__main__':
    # Run the app on all network interfaces and port 5000
    app.run(debug=True, host='0.0.0.0', port=5000)
