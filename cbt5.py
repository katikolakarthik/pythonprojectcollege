import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pandas as pd

# Function to validate login with Excel data
def validate_login():
    entered_username = username_entry.get().strip()
    entered_password = password_entry.get().strip()

    # Load the Excel file containing the usernames and passwords
    excel_file_path = "credentials.xlsx"  # Replace with the correct path
    try:
        credentials_df = pd.read_excel(excel_file_path)
        credentials_df.columns = credentials_df.columns.str.strip()
        credentials_df['Username'] = credentials_df['Username'].fillna('').astype(str).str.strip().str.lower()
        credentials_df['Password'] = credentials_df['Password'].fillna('').astype(str).str.strip()

        user_data = credentials_df[credentials_df['Username'] == entered_username.lower()]
        if not user_data.empty:
            stored_password = user_data['Password'].values[0]
            if entered_password == stored_password:
                messagebox.showinfo("Login Successful", "You have logged in successfully!")
                root.destroy()  # Close the login window
                open_questions_window(entered_username)  # Pass username to questions window
            else:
                messagebox.showerror("Login Failed", "Invalid password.")
        else:
            messagebox.showerror("Login Failed", "Username not found.")
    except Exception as e:
        messagebox.showerror("Error", f"Error reading the Excel file: {str(e)}")

# Function to display the questions GUI
def open_questions_window(username):
    # Create new window for questions
    question_window = tk.Tk()
    question_window.title("Online CBT Exam - Questions")
    question_window.geometry("800x600")  # Adjust the size of the question window

    file_path = "questions.xlsx"  # Replace with your questions Excel file path

    try:
        # Load questions from the Excel file
        questions_df = pd.read_excel(file_path)
        answers = {}  # Dictionary to store user's answers

        # Scrollable Frame Setup
        canvas = tk.Canvas(question_window, bg="pink")
        scrollbar = tk.Scrollbar(question_window, orient="vertical", command=canvas.yview)
        question_frame = tk.Frame(canvas, bg="pink")

        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((0, 0), window=question_frame, anchor="nw")
        question_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Load all questions into the frame
        for idx, question_data in questions_df.iterrows():
            question_panel = tk.Frame(question_frame, bg="pink")
            question_panel.pack(fill="both", expand=True, pady=10, padx=20)

            # Question label
            question_label = tk.Label(
                question_panel,
                text=f"Question {idx + 1}: {question_data['Question']}",
                wraplength=700,
                font=("Arial", 12),
                bg="pink",
                anchor="w",
                justify="left"
            )
            question_label.pack(anchor="w")

            # Create StringVar for tracking the selected answer
            selected_answer = tk.StringVar(value="")  # Default value is no selection
            answers[idx] = selected_answer

            # Options as radio buttons
            for option in ['Option A', 'Option B', 'Option C', 'Option D']:
                tk.Radiobutton(
                    question_panel,
                    text=f"{option[-1]}. {question_data[option]}",
                    variable=selected_answer,
                    value=option[-1],
                    font=("Arial", 12),
                    bg="pink",
                    anchor="w",
                    justify="left"
                ).pack(anchor="w", padx=20)

        # Submit Button
        def submit_exam():
            for idx, selected_answer in answers.items():
                if selected_answer.get() == "":
                    messagebox.showwarning("Warning", f"Please answer Question {idx + 1}")
                    return

            # Save responses
            response_data = []
            for idx, selected_answer in answers.items():
                response_data.append({
                    'Question': questions_df.iloc[idx]['Question'],
                    'Selected Answer': selected_answer.get(),
                    'Correct Answer': questions_df.iloc[idx]['Correct Answer'],
                    'Username': username  # Add the username to the responses
                })

            responses_df = pd.DataFrame(response_data)
            responses_df.to_excel("User_Responses.xlsx", index=False)
            messagebox.showinfo("Quiz Completed", "Your responses have been submitted!")
            question_window.quit()  # Close the application

        # Submit button
        submit_button = tk.Button(
            question_window,
            text="Submit Exam",
            font=("Arial", 12),
            command=submit_exam,
            bg="#4CAF50",
            fg="white"
        )
        submit_button.pack(side="bottom", pady=10)

    except Exception as e:
        messagebox.showerror("Error", f"Error reading the questions file: {str(e)}")

# Run the application for login
root = tk.Tk()
root.title("Login Form")
root.geometry("600x400")  # Adjusted window size
root.config(bg="pink")  # Set pink background color

# Disable maximize option
root.resizable(False, False)

# Add logo and college details (similar to your existing code)
logo_path = "logo.jpeg"
naac_logo_path = "naac.jpeg"

# Add left-side logo
try:
    logo_image = Image.open(logo_path).resize((80, 80))
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = tk.Label(root, image=logo_photo, bg="pink")
    logo_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
except Exception as e:
    print(f"Error loading logo: {e}")

# Add college details
college_details = tk.Label(
    root,
    text=(
        "TKRCET\n"
        "Approved By AICTE. Affiliated to JNTUH. Accredited By NBA\n"
        "Accredited by NAAC with 'A + ' Grade.\n"
        "Recognized under 2(f) and 12(B) of UGC Act 1956"
    ),
    font=("Arial", 10, "bold"),
    fg="blue",
    bg="pink",
    justify="center"
)
college_details.grid(row=0, column=1, columnspan=2, padx=10, pady=5, sticky="nsew")

# Add right-side logo
try:
    naac_logo_image = Image.open(naac_logo_path).resize((80, 80))
    naac_logo_photo = ImageTk.PhotoImage(naac_logo_image)
    naac_logo_label = tk.Label(root, image=naac_logo_photo, bg="pink")
    naac_logo_label.grid(row=0, column=3, padx=10, pady=5, sticky="e")
except Exception as e:
    print(f"Error loading NAAC logo: {e}")

# Login GUI widgets with added Title and Note

# Title for the CBT exam
exam_title = tk.Label(
    root,
    text="Online CBT Exam",
    font=("Arial", 16, "bold"),
    fg="green",
    bg="pink"
)
exam_title.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

# Note for the users
note_label = tk.Label(
    root,
    text="***** Note: Your username is your password *****",
    font=("Arial", 12, "italic"),
    fg="red",
    bg="pink"
)
note_label.grid(row=2, column=0, columnspan=4, padx=10, pady=5, sticky="nsew")

# Username label and entry
username_label = tk.Label(root, text="Username:", font=("Arial", 12), bg="pink")
username_label.grid(row=3, column=1, padx=10, pady=5, sticky="e")
username_entry = tk.Entry(root, font=("Arial", 12))
username_entry.grid(row=3, column=2, padx=10, pady=5, sticky="w")

# Password label and entry
password_label = tk.Label(root, text="Password:", font=("Arial", 12), bg="pink")
password_label.grid(row=4, column=1, padx=10, pady=5, sticky="e")
password_entry = tk.Entry(root, font=("Arial", 12), show="*")
password_entry.grid(row=4, column=2, padx=10, pady=5, sticky="w")

# Login button
login_button = tk.Button(root, text="Login", command=validate_login, bg="#4CAF50", fg="white", font=("Arial", 12))
login_button.grid(row=5, column=1, columnspan=2, pady=20)

# Run the application
root.mainloop()
