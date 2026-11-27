import os

from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

PROGRAMS = {
    "Fat Loss (FL)": {
        "workout": "Back Squat 5x5, EMOM Bike, Bench Press, Deadlift, Zone 2 Cardio",
        "diet": "Egg Whites + Oats, Grilled Chicken + Brown Rice, Fish Curry + Millet Roti",
        "calorie_factor": 22,
    },
    "Muscle Gain (MG)": {
        "workout": "Squat 5x5, Bench 5x5, Deadlift 4x6, Front Squat 4x8, Incline Press, Rows",
        "diet": "Eggs + PB Oats, Chicken Biryani (250g), Mutton Curry + Jeera Rice",
        "calorie_factor": 35,
    },
    "Beginner (BG)": {
        "workout": "Air Squats, Ring Rows, Push-ups — Focus: Technique & Form",
        "diet": "Balanced Tamil Meals: Idli-Sambar, Rice-Dal, Chapati. Protein: 120g/day",
        "calorie_factor": 26,
    },
}


@app.route("/", methods=["GET"])
def index():
    """Render main dashboard UI."""
    return render_template("index.html")


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "app": "ACEest Fitness"})


@app.route("/programs", methods=["GET"])
def get_programs():
    """Return list of all available fitness programs."""
    return jsonify({"programs": list(PROGRAMS.keys())})


@app.route("/program/<path:name>", methods=["GET"])
def get_program(name):
    """Return workout and diet details for a specific program."""
    if name in PROGRAMS:
        return jsonify(PROGRAMS[name])
    return jsonify({"error": "Program not found"}), 404


@app.route("/calories", methods=["POST"])
def calculate_calories():
    """Calculate daily calorie target based on weight and program."""
    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not data:
        return jsonify({"error": "No JSON body provided"}), 400

    weight = data.get("weight", 0)
    program = data.get("program", "")

    if program not in PROGRAMS:
        return jsonify({"error": "Invalid program"}), 400

    if isinstance(weight, bool) or not isinstance(weight, (int, float)):
        return jsonify({"error": "Weight must be a number"}), 400

    if weight <= 0 or weight > 500:
        return jsonify({"error": "Weight must be between 0 and 500 kg"}), 400

    factor = PROGRAMS[program]["calorie_factor"]
    calories = int(weight * factor)

    return jsonify({"weight": weight, "program": program, "calories": calories})


if __name__ == "__main__":
    # Local development only; containers run gunicorn (see Dockerfile).
    app.run(
        host=os.environ.get("HOST", "127.0.0.1"),
        port=int(os.environ.get("PORT", "5000")),
        debug=os.environ.get("FLASK_DEBUG") == "1",
    )
