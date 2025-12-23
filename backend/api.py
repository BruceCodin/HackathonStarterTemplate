"""Habit tracking api"""

from flask import Flask, request, render_template, redirect, url_for
from database import (check_and_apply_decay,
                      get_all_habits_with_tamagochis, has_completed_today,
                      create_habit, add_completion,
                      delete_habit)
from dotenv import load_dotenv

app = Flask(__name__)


@app.route("/")
def home():
    """
    route for the home page which decays any tamagochis if need be
    updates the completed today field of habits 
    displays all tamagochis
    """

    # check and apply decay
    check_and_apply_decay()

    # get all data
    habits = get_all_habits_with_tamagochis()

    for habit in habits:
        habit['completed_today'] = has_completed_today(habit['habit_id'])

    return render_template('templates/index.html', habits=habits)


@app.route('/habit/create', methods=['POST'])
def add_habit():
    # Get form data
    name = request.form.get('habit_name')
    description = request.form.get('description')
    target_frequency = request.form.get('target_frequency')
    frequency_unit = request.form.get('frequency_unit')

    # Create habit in DB
    create_habit(name, description, target_frequency, frequency_unit)

    # Redirect back to home
    return redirect(url_for('home'))


@app.route("/habit/<habit_id>/complete", methods=['POST'])
def complete_a_habit(habit_id):
    # add a completion to the db
    add_completion(habit_id)
    return redirect(url_for('home'))


@app.route("/habit/<habit_id>/delete")
def del_old_habit(habit_id):
    delete_habit(habit_id)
    return redirect(url_for('home'))


if __name__ == "__main__":
    load_dotenv()
    app.run(debug=True, host="0.0.0.0", port=5000)
