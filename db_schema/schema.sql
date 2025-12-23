-- Schema code for setting up the database for Hackathon Project: Tamagotchi Habit Tracker

DROP TABLE IF EXISTS habits CASCADE;
DROP TABLE IF EXISTS tamagotchi CASCADE;
DROP TABLE IF EXISTS habit_completion CASCADE;

CREATE TABLE habits (
    habit_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    habit_name TEXT NOT NULL,
    habit_description TEXT,
    target_frequency INT NOT NULL,
    frequency_unit TEXT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    animal_type TEXT NOT NULL DEFAULT 'cow',  

    -- Constraints: 
    CONSTRAINT target_frequency_check CHECK (target_frequency >= 0)

);

CREATE TABLE tamagotchi (
    tamagotchi_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    habit_id INT NOT NULL,
    tamagotchi_name TEXT NOT NULL,
    happiness_level INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    -- Habit ID Foreign Key: 
    FOREIGN KEY (habit_id) REFERENCES habits(habit_id) ON DELETE CASCADE,
    -- Constraints:
    CONSTRAINT happiness_level_check CHECK (happiness_level >= 0)

);


CREATE TABLE habit_completion (
    completion_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    habit_id INT NOT NULL,
    completion_date DATE,
    completed_at TIMESTAMP,

    -- Habit ID Foreign Key: 
    FOREIGN KEY (habit_id) REFERENCES habits(habit_id) ON DELETE CASCADE

);