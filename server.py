''' 
Executing this function initiates the application of emotion
detection to be executed over the Flask channel and deployed on
localhost:5000.
'''
from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask("Emotion Detector")

@app.route("/emotionDetector")
def emotion_detect():
    '''Analyzes the given text for emotional content and returns the results.
    '''
    # Retrieve the text to analyze from the request arguments
    text_to_analyze = request.args.get('textToAnalyze')

    # Check for blank input
    if not text_to_analyze or text_to_analyze.strip() == "":
        return "Invalid text! Please try again!"

    # Pass the text to the emotion_detector function and store the response
    response = emotion_detector(text_to_analyze)

    # Handle case where status_code is 400 (error from emotion_detector)
    if isinstance(response, dict) and response.get('status_code') == 400:
        return "Invalid text! Please try again!"

    # Check if dominant_emotion is None (invalid analysis)
    if response.get('dominant_emotion') is None:
        return "Invalid text! Please try again!"

    # Return the normal response
    return f"""For the given statement, the system response is 'anger': {response['anger']},
           'disgust': {response['disgust']}, 'fear': {response['fear']},
           'joy': {response['joy']}, and 'sadness': {response['sadness']}.
           The dominant emotion is {response['dominant_emotion']}"""

@app.route("/")
def render_index_page():
    '''Renders the main index page of the application.
    '''
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
