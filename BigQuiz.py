import pgzrun
import random

# Constants for the screen dimensions
WIDTH = 800
HEIGHT = 600

# Rectangles for different parts of the game interface
main_box = Rect(0, 0, 600, 180)     # Main question box dimensions
timer_box = Rect(0, 0, 150, 100)    # Timer box dimensions
answer_box1 = Rect(0, 0, 290, 100)  # Answer box 1 dimensions
answer_box2 = Rect(0, 0, 290, 100)  # Answer box 2 dimensions
answer_box3 = Rect(0, 0, 290, 100)  # Answer box 3 dimensions
answer_box4 = Rect(0, 0, 290, 100)  # Answer box 4 dimensions

# Positioning the rectangles on the screen to ensure they do not touch
main_box.move_ip(40, 50)            # Move main question box
timer_box.move_ip(650, 50)          # Move timer box to the top right corner
answer_box1.move_ip(50, 320)        # Move answer box 1
answer_box2.move_ip(400, 320)       # Move answer box 2 next to answer box 1
answer_box3.move_ip(50, 450)        # Move answer box 3 below answer box 1
answer_box4.move_ip(400, 450)       # Move answer box 4 below answer box 2

# List of answer boxes for collision detection
answer_boxes = [answer_box1, answer_box2, answer_box3, answer_box4]

# Initial score and timer settings
score = 0                            # Initialize score
time_left = 10                       # Set the timer for 10 seconds

# List of questions with the format [question, answer1, answer2, answer3, answer4, correct_answer_index]
questions = [
    ["What is the capital of Australia?", "Sydney", "Canberra", "Melbourne", "Brisbane", 2],
    ["What is 7 multiplied by 6?", "42", "36", "48", "54", 1],
    ["Who wrote 'Romeo and Juliet'?", "Mark Twain", "William Shakespeare", "Charles Dickens", "Ernest Hemingway", 2],
    ["What is the smallest planet in our solar system?", "Earth", "Mars", "Mercury", "Venus", 3],
    ["In what year did the Titanic sink?", "1912", "1905", "1920", "1898", 1],
    ["What is the chemical symbol for gold?", "Ag", "Au", "Pb", "Fe", 2],
    ["Which organ is responsible for pumping blood throughout the body?", "Liver", "Lungs", "Heart", "Kidneys", 3],
    ["What is the largest mammal in the world?", "Elephant", "Blue Whale", "Giraffe", "Great White Shark", 2],
    ["Who painted the Mona Lisa?", "Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Claude Monet", 3],
    ["What is the longest river in the world?", "Amazon", "Nile", "Yangtze", "Mississippi", 2],
    ["Which planet is known as the Red Planet?", "Jupiter", "Saturn", "Mars", "Earth", 3],
    ["What gas do plants absorb from the atmosphere?", "Oxygen", "Carbon Dioxide", "Nitrogen", "Helium", 2],
    ["What is the hardest natural substance on Earth?", "Gold", "Diamond", "Iron", "Quartz", 2],
    ["In which country would you find the Great Pyramid of Giza?", "Greece", "Egypt", "Mexico", "China", 2],
    ["What is the main ingredient in guacamole?", "Tomato", "Avocado", "Pepper", "Onion", 2]
]

# Select the first question to start with
question = questions.pop(0)         # Remove and store the first question from the list

# List of colors for the background and boxes
background_colors = [ # Background colors
    (169, 169, 169),  # Dim Gray
    (173, 216, 230),  # Light Blue
    (144, 238, 144),  # Light Green
    (230, 230, 250),  # Lavender
    (255, 218, 185)]  # Peach Puff
box_colors = [        # Box colors
    (135, 206, 250),  # Sky Blue
    (240, 128, 128),  # Light Coral
    (238, 221, 130),  # Pale Goldenrod
    (240, 230, 140),  # Khaki
    (176, 224, 230)]  # Light Steel Blue
text_colors = [       # Text colors
    (0, 0, 0),        # Black
    (0, 0, 128),      # Navy
    (0, 100, 0),      # Dark Green
    (255, 140, 0),    # Dark Orange 
    (139, 0, 0)]      # Dark Red           

# Variables to hold current colors for the question
current_background_color = random.choice(background_colors)  # Randomly select a background color
current_box_color = random.choice(box_colors)                # Randomly select a box color
current_text_color = random.choice(text_colors)              # Randomly select a text color

# Function to draw the game elements on the screen
def draw():
    screen.fill(current_background_color)  # Fill the background with the selected color
    screen.draw.filled_rect(main_box, current_box_color)   # Draw the main question box
    screen.draw.filled_rect(timer_box, current_box_color)  # Draw the timer box
    
    for box in answer_boxes:
        screen.draw.filled_rect(box, current_box_color)  # Draw each answer box
    
    # Draw timer and question with fixed text color
    screen.draw.textbox(str(time_left), timer_box, color=current_text_color)    # Display remaining time
    screen.draw.textbox(question[0], main_box, color=current_text_color)        # Display the current question
    
    # Display answers in their respective boxes with fixed text color
    for index, box in enumerate(answer_boxes):
        screen.draw.textbox(question[index + 1], box, color=current_text_color)  # Draw each answer

# Function to handle game over state
def game_over():
    global question, time_left
    message = "Game over. You got %s questions correct" % str(score)  # Construct game over message
    question = [message, "-", "-", "-", "-", 5]  # Set question to display game over message
    time_left = 0  # Set time left to 0 to end the game

# Function to handle correct answers
def correct_answer():
    global question, score, time_left
    score += 1           # Increase score by 1 for a correct answer
    if questions:        # Check if there are more questions
        question = questions.pop(0)  # Pop the next question
        # Update colors for the new question
        update_colors()  # Change colors for the new question
        time_left = 10   # Reset timer for the next question
    else:
        print("End of questions")  # Indicate that there are no more questions
        game_over()                # Trigger game over

# Function to update colors for the new question
def update_colors():
    global current_background_color, current_box_color, current_text_color
    current_background_color = random.choice(background_colors)  # Randomly select a new background color
    current_box_color = random.choice(box_colors)                # Randomly select a new box color
    current_text_color = random.choice(text_colors)              # Randomly select a new text color

# Function to handle mouse click events
def on_mouse_down(pos):
    index = 1  # Start with index 1 for the answer boxes
    for box in answer_boxes:
        if box.collidepoint(pos):  # Check if mouse click is within the box
            print("Clicked on answer " + str(index))  # Print which answer box was clicked
            if index == question[5]:  # Check if the clicked box is the correct answer
                print("You got it correct!")  # Print correct answer message
                correct_answer()  # Handle correct answer logic
            else:
                game_over()  # Trigger game over for incorrect answer
            break            # Exit the loop once a box is clicked
        index += 1           # Increment index for the next box

# Function to update the remaining time
def update_time_left():
    global time_left
    if time_left > 0:
        time_left -= 1  # Decrease time left by 1 second
    else:
        game_over()  # Trigger game over when time runs out

# Function to handle key events
def on_key_up(key):
    global score
    if key == keys.H:  # If 'H' key is pressed
        print("The correct answer is box number %s" % question[5])  # Display correct answer index
    if key == keys.SPACE:  # If 'SPACE' key is pressed
        score -= 1  # Deduct 1 point from the score
        correct_answer()  # Handle the correct answer logic

# Schedule the time update function to run every second
clock.schedule_interval(update_time_left, 1.0)  # Update the timer every second

# Start the game loop
pgzrun.go()  # Launch the game

