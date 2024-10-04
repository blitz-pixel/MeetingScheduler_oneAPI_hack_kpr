from flask import Flask, request, jsonify
import openai,time

from openai.error import RateLimitError

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = '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'

availability_data = {
    "employee1@example.com": {
        "free_times": ["2024-10-02T09:00:00", "2024-10-02T13:00:00"],
        "preferences": ["morning", "afternoon"]
    },
    "employee2@example.com": {
        "free_times": ["2024-10-02T10:00:00", "2024-10-02T14:00:00"],
        "preferences": ["afternoon"]
    },
}


# Rate limiting settings
last_request_time = 0
request_interval = 1  # Minimum time between requests in seconds

def analyze_availability_with_openai(availability):
    global last_request_time
    current_time = time.time()

    # Check if we need to wait before making another request
    if current_time - last_request_time < request_interval:
        time.sleep(request_interval - (current_time - last_request_time))

    availability_str = str(availability)
    prompt = f"Given the following availability data, suggest the best meeting time:\n{availability_str}"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    last_request_time = time.time()  # Update the last request time
    return response['choices'][0]['message']['content']

# Your existing schedule_meeting function...




@app.route('/schedule_meeting', methods=['POST'])
def schedule_meeting():
    employee_emails = request.json.get('employee_emails', [])
    
    availability = {email: availability_data[email] for email in employee_emails if email in availability_data}

    if not availability:
        return jsonify({'message': 'No available data for the provided emails.'}), 400
    
    try:
        ai_suggestions = analyze_availability_with_openai(availability)
        return jsonify({"suggested_meeting_time": ai_suggestions}), 200
    except RateLimitError:
        return jsonify({'error': 'Rate limit exceeded. Please try again later.'}), 429


if __name__ == '__main__':
    app.run(debug=True)
