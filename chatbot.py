import tkinter as tk
from tkinter import messagebox, scrolledtext, Toplevel
import sqlite3
from datetime import datetime
import random

class MentalHealthChatbot:
    def __init__(self):
        self.init_db()
        self.setup_responses()
        self.create_main_window()
        self.show_welcome_screen()
        self.root.mainloop()

    def init_db(self):
        """Initialize the SQLite database"""
        self.conn = sqlite3.connect('mental_health_chatbot.db')
        self.cursor = self.conn.cursor()
        
        # Create tables if they don't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT UNIQUE,
                name TEXT,
                password TEXT,
                terms_accepted BOOLEAN,
                registration_date TEXT,
                last_login TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                timestamp TEXT,
                user_message TEXT,
                bot_response TEXT,
                sentiment TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        self.conn.commit()
    

    def setup_responses(self):
        """Setup keyword responses for the chatbot"""
        self.responses = {
            # Academic stress
         "academic": {
            "keywords": ["exam", "study", "assignment", "grade", "coursework", "deadline", "fail", "lecture", "module"],
            "replies": [
                "University academics can feel overwhelming at first. Many first-years struggle with the transition - you're not alone in this. What specifically feels challenging right now?",
                "I hear the stress in your message. The jump from school to uni work is bigger than most people expect. Would it help to talk through one particular assignment?",
                "Academic pressure is really common, especially in first year when everything's new. What's one small step you could take to feel more on top of things?"
            ],
            "follow_up": [
                "How does this academic stress compare to what you experienced in school?",
                "Have you found any particular study techniques that help, even just a little?",
                "Would breaking things down into smaller tasks make it feel more manageable?"
            ]
            
        },
            
            # Financial stress
              "financial": {
            "keywords": ["money", "rent", "tuition", "loan", "broke", "expensive", "cost", "budget", "bills"],
            "replies": [
                "Money worries can feel especially heavy when you're adjusting to independent living. Many students struggle with this - have you looked into what support your uni offers?",
                "Financial stress is so common for students. It's okay to feel overwhelmed by this. What's the biggest financial pressure right now?",
                "Living on a student budget is really tough. Would it help to talk through some budgeting strategies or campus resources?"
            ],
            "follow_up": [
                "Have you contacted your university's financial advice service? They often know about grants or funds students don't realize exist.",
                "What's one financial worry that's been keeping you up at night? Maybe we can problem-solve it together.",
                "Many students don't know about campus food banks or hardship funds - would you like information about these?"
            ]
      
        },
            
            # Anxiety
               "anxiety": {
            "keywords": ["anxious", "worry", "nervous", "panic", "overwhelm", "scared", "fear", "stressed"],
            "replies": [
                "Anxiety can feel so intense when you're in a new environment. Would you like to try a quick grounding technique together?",
                "That sounds really difficult. First year brings so many changes that can trigger anxiety. What helps you feel even slightly more grounded?",
                "Your brain might be in overdrive trying to adjust to all this newness. Would sharing more about what specifically feels overwhelming help?"
            ],
            "follow_up": [
                "When you feel anxious, do you notice it more in your body (like racing heart) or your thoughts?",
                "Have you found anything that helps ease the anxiety, even just a little bit?",
                "Would practicing a breathing technique together right now be helpful?"
            ]
        },
            
            # Depression
                "depression": {
            "keywords": ["depressed", "sad", "hopeless", "empty", "numb", "worthless", "useless", "motivation"],
            "replies": [
                "I'm really sorry you're feeling this way. Depression can make the transition to uni especially hard. You're not alone in this struggle.",
                "That sounds incredibly difficult. First year can sometimes feel isolating when you're dealing with depression. Would talking more about this help?",
                "Depression lies to you - you matter, even when it doesn't feel that way. What's one small thing that might feel manageable today?"
                "I'm sorry you're feeling this way. Would you like me to share some support options with you?"
                "Would you like information about university counseling services?",
                "I can share some self-help resources if that would be helpful?",
            ],
            "follow_up": [
                "Have you connected with any support services at your university? I can help you find them if you'd like.",
                "What does your support system look like right now? Even one person who checks in can make a difference.",
                "Would it help to brainstorm tiny, achievable goals for the next few days?"
            ]
        },
            
            # Loneliness
               "loneliness": {
            "keywords": ["lonely", "alone", "isolated", "friendless", "left out", "excluded", "homesick"],
            "replies": [
                "Feeling lonely at uni is more common than people talk about. It often takes time to find your people. What's your experience been like so far?",
                "That ache of loneliness can feel especially sharp in first year. Many students feel this way but hide it. Have you found any spaces that feel slightly more comfortable?",
                "Making friends at uni isn't always automatic like people assume. What kinds of connections are you hoping to find?"
            ],
            "follow_up": [
                "Have you explored any societies or clubs that align with your interests?",
                "What was social life like for you before uni? Sometimes that context helps.",
                "Would you like some low-pressure suggestions for meeting people?"
            ]
        },
            
            # Sleep issues
              "sleep": {
            "keywords": ["tired", "sleep", "insomnia", "exhausted", "awake", "restless", "night", "energy"],
            "replies": [
                "Sleep problems can make everything else at uni feel harder. What's your nighttime routine been like?",
                "Poor sleep is so common in first year with all the changes. What do you think might be contributing to your sleep difficulties?",
                "When sleep is off, it affects everything. Have you noticed any patterns to your sleep struggles?"
            ],
            "follow_up": [
                "Have you tried any relaxation techniques before bed? Even simple ones can help.",
                "Is your sleep schedule consistent or does it vary a lot?",
                "Would information about sleep hygiene strategies be helpful?"
            ]
        },
        
            
            # Crisis keywords (will trigger emergency protocol)
            "crisis": {
            "keywords": ["suicide", "kill myself", "end it all", "want to die", "harm myself", "self-harm", "no point"],
            "replies": [
                "I'm really concerned about what you're sharing. You matter, and there are people who want to support you through this.",
                "This sounds incredibly painful. Please know help is available - you don't have to go through this alone.",
                "I hear how much you're struggling right now. Let me connect you with immediate support options."
            ],
            "resources": [
                "University Crisis Support:\nPhone: 0800 123 4567 (24/7)\nText: UNI to 85258",
                "Samaritans (UK): 116 123 (24/7, free)\nShout (UK): Text SHOUT to 85258",
                "Your GP can also help connect you with ongoing support."
            ]
        },
            # Positive sentiment
            "positive": {
            "keywords": ["happy", "good", "great", "better", "improve", "progress", "excited", "proud"],
            "replies": [
                "It's wonderful to hear you're feeling positive! What's been going well for you?",
                "I'm so glad to hear that! Celebrating the wins is so important. Want to share more about what's working?",
                "That's fantastic! First year has its ups and downs - it's great you're recognizing the good moments too."
            ],
            "follow_up": [
                "What do you think has contributed to this positive feeling?",
                "How might you build on or maintain this positive experience?",
                "Is there someone you can share this good moment with?"
            ]
        },

        # Transition challenges
        "transition": {
            "keywords": ["adjust", "homesick", "new", "change", "different", "culture shock", "settle"],
            "replies": [
                "The transition to uni life is a huge adjustment that often isn't talked about enough. What's been the most surprising part for you?",
                "It's completely normal to feel unsettled during this transition period. What do you miss most from home?",
                "First term can feel like emotional whiplash with all the changes. What aspect of uni life feels hardest to adjust to?"
            ],
            "follow_up": [
                "Have you found any little things that help you feel more at home here?",
                "What did your support system look like before uni? Sometimes recreating bits of that helps.",
                "Would connecting with other students who might share your background be helpful?"
            ]
        },

            # Default responses when no keywords match
             "default": {
            "keywords": [],
            "replies": [
                "I hear you. Starting university brings up so many different feelings. Can you tell me more about what's on your mind?",
                "Thank you for sharing that with me. What's been your experience with this so far?",
                "That sounds significant. How has this been affecting your first year experience?",
                "I want to understand better. Could you share more about what this has been like for you?"
            ],
            "follow_up": [
                "What emotions come up for you when you think about this?",
                "Has this changed how you're approaching uni life?",
                "What would support with this look like for you right now?"
            ]
        }  
    }
    
        self.empathetic_phrases = [
        "That sounds really tough, especially when you're adjusting to so much newness.",
        "I can imagine how overwhelming that must feel on top of all the other first-year challenges.",
        "It makes complete sense you'd feel that way given everything.",
        "That's a really human response to the pressures you're facing.",
        "I hear how much this is affecting you. That's so valid."
    ]

        self.normalizing_statements = [
        "Many first-years experience something similar - it doesn't mean there's anything wrong with you.",
        "This is more common than people talk about, especially in first term.",
        "You're not alone in feeling this way during the transition to uni.",
        "Lots of students struggle with this but don't always show it.",
        "This is a normal reaction to the huge changes you're navigating."
    ]

        self.open_ended_questions = [
        "What's that been like for you?",
        "How has this affected your experience so far?",
        "What do you wish people understood about this?",
        "Where would you like to go from here?",
        "What kind of support would feel most helpful right now?"
    ]

    
        self.response_enhancers = {
        "empathy_first": lambda: random.choice(self.empathetic_phrases),
        "normalize": lambda: random.choice(self.normalizing_statements),
        "open_ended": lambda: random.choice(self.open_ended_questions),
        "combine": lambda: f"{random.choice(self.empathetic_phrases)} {random.choice(self.open_ended_questions)}"
    }
    
        self.help_resources = {
        "university": [
            "University Counseling Service: counseling@university.edu | 0800 123 4567",
            "Student Wellbeing Portal: wellbeing.university.ac.uk",
            "24/7 Mental Health Support Line: 0800 987 6543",
            "Academic Support: academicsupport.university.ac.uk"
        ],
        "national": [
            "Mind (Mental Health Charity): mind.org.uk | 0300 123 3393",
            "Samaritans (24/7 Support): samaritans.org | 116 123",
            "Shout Crisis Text Line: Text 'SHOUT' to 85258",
            "NHS Mental Health Services: nhs.uk/mental-health"
        ],
        "self_help": [
            "Student Minds (Student Mental Health): studentminds.org.uk",
            "The Mix (Under 25s Support): themix.org.uk",
            "Headspace (Meditation App): headspace.com/students",
            "SilverCloud (Online CBT): silvercloudhealth.com"
        ]
    }
    


    # ===== ADD THESE NEW METHODS HERE =====
    def get_enhanced_response(self, category, message):
        """Generate enhanced response using the advanced components"""
        base_response = random.choice(self.responses[category]["replies"])
        
        if random.random() < 0.5:
            enhancement_type = random.choice(list(self.response_enhancers.keys()))
            enhanced_part = self.response_enhancers[enhancement_type]()
            return f"{enhanced_part} {base_response}"
        return base_response

    def get_follow_up(self, category):
        """Get a follow-up question if available"""
        if "follow_up" in self.responses[category]:
            return random.choice(self.responses[category]["follow_up"])
        return None
    

        

    def create_main_window(self):
        """Create the main application window"""
        self.root = tk.Tk()
        self.root.title("Mental Health Support")
        self.root.geometry("500x500")
        self.root.configure(bg="#f0f8ff")

    def show_welcome_screen(self):

        """Show welcome screen with login/signup options"""
        self.clear_window()
    
        self.welcome_frame = tk.Frame(self.root, bg="#f0f8ff")
        self.welcome_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
    
    # More casual heading
        tk.Label(self.welcome_frame, text="Uni Mental Health Support", 
            font=("Helvetica", 20, "bold"), bg="#f0f8ff", fg="#2c3e50").pack(pady=20)
    
    # Friendly subheading
        tk.Label(self.welcome_frame, 
            text="Hi there! I'm here to help you navigate uni life.\nNo judgment, just support.", 
            font=("Helvetica", 12), bg="#f0f8ff", fg="#333333").pack(pady=10)
    
    # Button container for better spacing
        button_frame = tk.Frame(self.welcome_frame, bg="#f0f8ff")
        button_frame.pack(pady=20)
    
    # More inviting button text with better styling
        tk.Button(button_frame, text="Login!", command=self.show_login_frame, 
             bg="#4b6cb7", fg="white", font=("Helvetica", 12),
             padx=20, pady=5).pack(pady=10, fill=tk.X)
    
        tk.Button(button_frame, text="First time here? Sign up", command=self.show_signup_frame,
             bg="#2c3e50", fg="white", font=("Helvetica", 12),
             padx=20, pady=5).pack(pady=10, fill=tk.X)
    
    # Confidentiality notice
        tk.Label(self.welcome_frame, 
            text="All conversations are confidential and anonymized.",
            font=("Helvetica", 8), bg="#f0f8ff", fg="#666666").pack(side=tk.BOTTOM, pady=10)

    def show_login_frame(self):
        """Show login interface"""
        self.clear_window()
        
        self.login_frame = tk.Frame(self.root, bg="#f0f8ff")
        self.login_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        tk.Label(self.login_frame, text="Login", font=("Helvetica", 24, "bold"), 
                bg="#f0f8ff", fg="#2b5876").pack(pady=10)
        
        # Student ID
        id_frame = tk.Frame(self.login_frame, bg="#f0f8ff")
        id_frame.pack(pady=5)
        tk.Label(id_frame, text="Student ID:", font=("Helvetica", 12), bg="#f0f8ff").pack(side=tk.LEFT)
        self.login_id = tk.Entry(id_frame, font=("Helvetica", 12), width=25)
        self.login_id.pack(side=tk.LEFT, padx=5)
        
        # Password
        pass_frame = tk.Frame(self.login_frame, bg="#f0f8ff")
        pass_frame.pack(pady=5)
        tk.Label(pass_frame, text="Password:", font=("Helvetica", 12), bg="#f0f8ff").pack(side=tk.LEFT)
        self.login_pass = tk.Entry(pass_frame, font=("Helvetica", 12), width=25, show="*")
        self.login_pass.pack(side=tk.LEFT, padx=5)
        
        # Buttons
        tk.Button(self.login_frame, text="Login", command=self.handle_login,
                 bg="#4b6cb7", fg="white", font=("Helvetica", 14)).pack(pady=20)
        
        tk.Button(self.login_frame, text="Forgot Password?", command=self.show_forgot_password,
                 fg="#4b6cb7", relief=tk.FLAT, bd=0, font=("Helvetica", 10)).pack(pady=5)
        
        tk.Button(self.login_frame, text="Back", command=self.show_welcome_screen,
                 bg="#95a5a6", fg="white", font=("Helvetica", 10)).pack(pady=5)

    def show_forgot_password(self):
        """Show password reset interface"""
        self.clear_window()
        
        self.forgot_frame = tk.Frame(self.root, bg="#f0f8ff")
        self.forgot_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        tk.Label(self.forgot_frame, text="Reset Password", font=("Helvetica", 20, "bold"), 
                bg="#f0f8ff", fg="#2b5876").pack(pady=10)
        
        # Student ID
        id_frame = tk.Frame(self.forgot_frame, bg="#f0f8ff")
        id_frame.pack(pady=10)
        tk.Label(id_frame, text="Student ID:", font=("Helvetica", 12), bg="#f0f8ff").pack(side=tk.LEFT)
        self.reset_id = tk.Entry(id_frame, font=("Helvetica", 12), width=25)
        self.reset_id.pack(side=tk.LEFT, padx=5)
        
        # New Password
        new_pass_frame = tk.Frame(self.forgot_frame, bg="#f0f8ff")
        new_pass_frame.pack(pady=5)
        tk.Label(new_pass_frame, text="New Password:", font=("Helvetica", 12), bg="#f0f8ff").pack(side=tk.LEFT)
        self.new_pass = tk.Entry(new_pass_frame, font=("Helvetica", 12), width=25, show="*")
        self.new_pass.pack(side=tk.LEFT, padx=5)
        
        # Confirm Password
        confirm_frame = tk.Frame(self.forgot_frame, bg="#f0f8ff")
        confirm_frame.pack(pady=5)
        tk.Label(confirm_frame, text="Confirm Password:", font=("Helvetica", 12), bg="#f0f8ff").pack(side=tk.LEFT)
        self.confirm_pass = tk.Entry(confirm_frame, font=("Helvetica", 12), width=25, show="*")
        self.confirm_pass.pack(side=tk.LEFT, padx=5)
        
        # Buttons
        tk.Button(self.forgot_frame, text="Reset Password", command=self.handle_password_reset,
                 bg="#4b6cb7", fg="white", font=("Helvetica", 12, "bold")).pack(pady=20)
        
        tk.Button(self.forgot_frame, text="Back to Login", command=self.show_login_frame,
                 bg="#95a5a6", fg="white", font=("Helvetica", 10)).pack(pady=5)

    def handle_password_reset(self):
        """Handle password reset logic"""
        student_id = self.reset_id.get().strip()
        new_pass = self.new_pass.get()
        confirm_pass = self.confirm_pass.get()
        
        if not all([student_id, new_pass, confirm_pass]):
            messagebox.showerror("Error", "All fields are required")
            return
        
        if not (student_id.isdigit() and len(student_id) == 8 and student_id.startswith("28")):
            messagebox.showerror("Error", "Student ID must be 8 digits starting with 28")
            return
        
        if new_pass != confirm_pass:
            messagebox.showerror("Error", "Passwords don't match")
            return
        
        if len(new_pass) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters")
            return
        
        # Update password in database
        try:
            self.cursor.execute("SELECT id FROM users WHERE student_id=?", (student_id,))
            if not self.cursor.fetchone():
                messagebox.showerror("Error", "Student ID not found")
                return
            
            self.cursor.execute("UPDATE users SET password=? WHERE student_id=?", 
                              (new_pass, student_id))
            self.conn.commit()
            messagebox.showinfo("Success", "Password updated successfully!")
            self.show_login_frame()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

    def show_signup_frame(self):
        """Show signup interface"""
        self.clear_window()
        
        self.signup_frame = tk.Frame(self.root, bg="#f0f8ff")
        self.signup_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        tk.Label(self.signup_frame, text="Sign Up", font=("Helvetica", 24, "bold"), 
                bg="#f0f8ff", fg="#2b5876").pack(pady=10)
        
        # Name
        name_frame = tk.Frame(self.signup_frame, bg="#f0f8ff")
        name_frame.pack(pady=5)
        tk.Label(name_frame, text="Full Name:", font=("Helvetica", 12), bg="#f0f8ff").pack(side=tk.LEFT)
        self.signup_name = tk.Entry(name_frame, font=("Helvetica", 12), width=25)
        self.signup_name.pack(side=tk.LEFT, padx=5)
        
        # Student ID
        id_frame = tk.Frame(self.signup_frame, bg="#f0f8ff")
        id_frame.pack(pady=5)
        tk.Label(id_frame, text="Student ID:", font=("Helvetica", 12), bg="#f0f8ff").pack(side=tk.LEFT)
        self.signup_id = tk.Entry(id_frame, font=("Helvetica", 12), width=25)
        self.signup_id.pack(side=tk.LEFT, padx=5)
        
        # Password
        pass_frame = tk.Frame(self.signup_frame, bg="#f0f8ff")
        pass_frame.pack(pady=5)
        tk.Label(pass_frame, text="Password:", font=("Helvetica", 12), bg="#f0f8ff").pack(side=tk.LEFT)
        self.signup_pass = tk.Entry(pass_frame, font=("Helvetica", 12), width=25, show="*")
        self.signup_pass.pack(side=tk.LEFT, padx=5)
        
        # Confirm Password
        confirm_frame = tk.Frame(self.signup_frame, bg="#f0f8ff")
        confirm_frame.pack(pady=5)
        tk.Label(confirm_frame, text="Confirm Password:", font=("Helvetica", 12), bg="#f0f8ff").pack(side=tk.LEFT)
        self.signup_confirm = tk.Entry(confirm_frame, font=("Helvetica", 12), width=25, show="*")
        self.signup_confirm.pack(side=tk.LEFT, padx=5)
        
        # Terms checkbox
        self.terms_var = tk.BooleanVar()
        terms_check = tk.Checkbutton(
            self.signup_frame,
            text="I agree to the Terms and Conditions",
            variable=self.terms_var,
            bg="#f0f8ff",
            font=("Helvetica", 10),
            command=self.show_terms
        )
        terms_check.pack(pady=10)
        
        # Buttons
        tk.Button(self.signup_frame, text="Sign Up", command=self.handle_signup,
                 bg="#4b6cb7", fg="white", font=("Helvetica", 14)).pack(pady=10)
        
        tk.Button(self.signup_frame, text="Back", command=self.show_welcome_screen,
                 bg="#95a5a6", fg="white", font=("Helvetica", 10)).pack(pady=5)

    def show_terms(self):
        """Show terms and conditions in a new window"""
        if hasattr(self, 'terms_window') and self.terms_window.winfo_exists():
            return
            
        self.terms_window = Toplevel(self.root)
        self.terms_window.title("Terms and Conditions")
        self.terms_window.geometry("500x400")
        
        terms_text = """
        TERMS AND CONDITIONS FOR MENTAL HEALTH CHATBOT
        
        1. CONFIDENTIALITY
        - All conversations are confidential.
        - We may contact services if there's risk of harm.
        
        2. DATA USAGE
        - Your data is stored securely.
        - Conversations are anonymized for research.
        
        3. LIMITATIONS
        - Not a substitute for professional care.
        - In emergencies, contact local services.
        
        4. ACCEPTABLE USE
        - Use respectfully.
        - Misuse may terminate account.
        
        5. CONSENT
        - Confirm you're a student.
        - Understand automated support limits.
        
        Last updated: """ + datetime.now().strftime("%Y-%m-%d")
        
        text_widget = scrolledtext.ScrolledText(
            self.terms_window,
            wrap=tk.WORD,
            font=("Helvetica", 10)
        )
        text_widget.insert(tk.INSERT, terms_text)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        close_btn = tk.Button(
            self.terms_window,
            text="I Understand",
            command=self.terms_window.destroy
        )
        close_btn.pack(pady=5)

    def handle_signup(self):
      """Handle signup logic"""
      name = self.signup_name.get().strip()
      student_id = self.signup_id.get().strip()
      password = self.signup_pass.get()
      confirm_pass = self.signup_confirm.get()

      if not all([name, student_id, password, confirm_pass]):
        messagebox.showerror("Error", "All fields are required")
        return

      if not (student_id.isdigit() and len(student_id) == 8 and student_id.startswith("28")):
        messagebox.showerror("Error", "Student ID must be 8 digits starting with 28")
        return
 
      if password != confirm_pass:
        messagebox.showerror("Error", "Passwords don't match")
        return

      if len(password) < 6:
        messagebox.showerror("Error", "Password must be at least 6 characters")
        return

      if not self.terms_var.get():
        messagebox.showerror("Error", "You must agree to the terms")
        return

      try:
        self.cursor.execute(
            "INSERT INTO users (student_id, name, password, terms_accepted, registration_date, last_login) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (student_id, name, password, True, 
             datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
             datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        self.conn.commit()
        messagebox.showinfo("Success", "Account created successfully!")
        self.show_login_frame()
      except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Student ID already exists")
      except sqlite3.Error as e:
        messagebox.showerror("Error", f"Database error: {e}")
    
    def handle_login(self):
       """Handle login logic"""
       student_id = self.login_id.get().strip()
       password = self.login_pass.get()

       if not student_id or not password:
          messagebox.showerror("Error", "Please enter both Student ID and Password")
          return
    
    # Validate student ID format first
       if not (student_id.isdigit() and len(student_id) == 8 and student_id.startswith("28")):
          messagebox.showerror("Error", "Invalid Student ID format. Must be 8 digits starting with 28")
          return

       try:
        # Check credentials
          self.cursor.execute("SELECT id, name FROM users WHERE student_id=? AND password=?", 
                          (student_id, password))
          user = self.cursor.fetchone()
        
          if user:
            self.user_id, self.current_user = user[0], user[1]
            # Update last login time
            self.cursor.execute(
                "UPDATE users SET last_login=? WHERE id=?",
                (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.user_id))
            self.conn.commit()
            self.show_main_menu()
          else:
              messagebox.showerror("Error", "Invalid Student ID or Password")
       except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
    def show_main_menu(self):
        """Show main menu after login"""
        self.clear_window()
        
        self.menu_frame = tk.Frame(self.root, bg="#f0f8ff")
        self.menu_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        tk.Label(self.menu_frame, text=f"Welcome, {self.current_user}!", 
                font=("Helvetica", 20, "bold"), bg="#f0f8ff", fg="#2b5876").pack(pady=10)
        
        tk.Label(self.menu_frame, text="How can we support you today?",
                font=("Helvetica", 12), bg="#f0f8ff").pack(pady=10)
        
        # Support topics - all options included
        topics = [
            ("Academic Stress", "#4b6cb7"),
            ("Financial Worries", "#4b6cb7"),
            ("Anxiety", "#4b6cb7"),
            ("Depression", "#4b6cb7"),
            ("Loneliness", "#4b6cb7"),
            ("Sleep Issues", "#4b6cb7"),
            ("Just need to talk", "#4b6cb7")
        ]
        
        for text, color in topics:
            btn = tk.Button(
                self.menu_frame,
                text=text,
                font=("Helvetica", 12),
                bg=color,
                fg="white",
                width=20,
                command=lambda t=text: self.start_chat(t)
            )
            btn.pack(pady=5)
        
        # Emergency button
        tk.Button(
            self.menu_frame,
            text="Emergency Help",
            font=("Helvetica", 10, "bold"),
            bg="#e74c3c",
            fg="white",
            command=self.show_emergency_help
        ).pack(pady=10)
        
        # Logout button
        tk.Button(
            self.menu_frame,
            text="Logout",
            font=("Helvetica", 12),
            bg="#95a5a6",
            fg="white",
            command=self.show_welcome_screen
        ).pack(pady=20)

    def get_help_resources(self, resource_type="university"):
        """Return formatted help resources"""
        resources = self.help_resources.get(resource_type, [])
        return "\n".join([f"• {resource}" for resource in resources])

    def show_emergency_help(self):
        """Show emergency contact information"""
        emergency_info = (
            "Emergency Contacts:\n\n"
            "University Counseling Service:\n"
            "Phone: 0800 123 4567\n"
            "Email: counselling@university.edu\n"
            "Open: Mon-Fri 9am-5pm\n\n"
            "24/7 Helplines:\n"
            "Samaritans: 116 123 (UK)\n"
            "National Suicide Prevention Lifeline: 988 (US)\n"
            "Crisis Text Line: Text HOME to 741741 (US/UK)\n\n"
            "In immediate danger? Call 999 (UK) or 911 (US)"
        )
        
        messagebox.showinfo("Emergency Help", emergency_info)

    def start_chat(self, topic):
        """Start a chat session"""
        self.clear_window()
        
        self.chat_frame = tk.Frame(self.root, bg="#f0f8ff")
        self.chat_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Chat header
        header = tk.Frame(self.chat_frame, bg="#f0f8ff")
        header.pack(fill=tk.X, pady=5)
        
        tk.Label(header, text=f"Chat: {topic}", font=("Helvetica", 16, "bold"), 
                bg="#f0f8ff", fg="#2b5876").pack(side=tk.LEFT)
        
        tk.Button(header, text="Back to Menu", command=self.show_main_menu,
                 bg="#4b6cb7", fg="white", font=("Helvetica", 10)).pack(side=tk.RIGHT)
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            self.chat_frame,
            font=("Helvetica", 12),
            wrap=tk.WORD,
            width=50,
            height=15,
            state=tk.DISABLED
        )
        self.chat_display.pack(pady=10, padx=5, fill=tk.BOTH, expand=True)
        
        # Configure tags for different message types
        self.chat_display.tag_config("user", foreground="#2c3e50")
        self.chat_display.tag_config("bot", foreground="#2980b9")
        self.chat_display.tag_config("crisis", foreground="red")

        # Add typing indicator label
        self.typing_label = tk.Label(
        self.chat_frame,
        text="",
        font=("Helvetica", 10, "italic"),
        bg="#f0f8ff",
        fg="#666666"
        )
        self.typing_label.pack()
        
        # Welcome message
        self.add_message(f"Buddy: Hello {self.current_user}! You've selected '{topic}'. How can I help you today?", "bot")
        
        # Input area
        input_frame = tk.Frame(self.chat_frame, bg="#f0f8ff")
        input_frame.pack(fill=tk.X, pady=10)
        
        self.user_input = tk.Entry(
            input_frame,
            font=("Helvetica", 12),
            width=40
        )
        self.user_input.pack(side=tk.LEFT, padx=5)
        self.user_input.bind("<Return>", lambda e: self.process_message())
        
        send_btn = tk.Button(
            input_frame,
            text="Send",
            font=("Helvetica", 12),
            bg="#4b6cb7",
            fg="white",
            command=self.process_message
        )
        send_btn.pack(side=tk.LEFT)
    def process_message(self):
         """Process user message with a 5-second response delay"""
         message = self.user_input.get().strip()
         if not message:
          return
    
    # Add user message to chat
         self.add_message(f"You: {message}", "user")
         self.user_input.delete(0, tk.END)
    
    # Show typing indicator
         self.typing_label.config(text="Buddy is typing...")
         self.root.update()
    
    # Schedule the response after 5 seconds
         self.root.after(5000, lambda: self.generate_and_show_response(message))

    def generate_and_show_response(self, message):
        """Generate and display the response after delay using advanced components"""
        # Hide typing indicator
        self.typing_label.config(text="")
        
        message_lower = message.lower()
        response = None
        sentiment = self.analyze_sentiment(message)
        
        # Check for crisis keywords first
        if any(keyword in message_lower for keyword in self.responses["crisis"]["keywords"]):
            response = "\n".join(self.responses["crisis"]["replies"])
            resources = "\n".join(self.responses["crisis"]["resources"])
            full_response = f"{response}\n\nHere are some resources that might help:\n{resources}"
            self.add_message(f"Buddy: {full_response}", "crisis")
            self.log_conversation(message, full_response, "crisis")
            return

        help_keywords = ["website", "resource", "help", "support", "refer", "service"]
        if any(keyword in message_lower for keyword in help_keywords):
          response = "Here are some resources that might help:\n\n"
          response += "University Services:\n" + self.get_help_resources("university") + "\n\n"
          response += "National Support:\n" + self.get_help_resources("national") + "\n\n"
          response += "Self-Help Options:\n" + self.get_help_resources("self_help")
          self.add_message(f"Buddy: {response}", "bot")
          self.log_conversation(message, response, "resource")
          return
        
        
        # Generate appropriate response
        if sentiment == "positive":
            response = self.get_enhanced_response("positive", message)
        else:
            # Check other categories
            matched_category = None
            for category, data in self.responses.items():
                if category not in ["crisis", "positive", "default"]:
                    if any(keyword in message_lower for keyword in data["keywords"]):
                        matched_category = category
                        response = self.get_enhanced_response(category, message)
                        break
            
            if not response:
                response = self.get_enhanced_response("default", message)
        
        # Add follow-up question 30% of the time
        if matched_category and random.random() < 0.3:
            follow_up = self.get_follow_up(matched_category)
            if follow_up:
                response = f"{response}\n\n{follow_up}"
        
        self.add_message(f"Buddy: {response}", "bot")
        
        # Log conversation
        self.log_conversation(message, response, sentiment)

    def analyze_sentiment(self, message):
        """Basic sentiment analysis"""
        message_lower = message.lower()
        
        # Check for positive words
        if any(word in message_lower for word in self.responses["positive"]["keywords"]):
            return "positive"
        
        # Check for negative words in each category
        negative_categories = ["academic", "financial", "anxiety", "depression", "loneliness", "sleep"]
        for category in negative_categories:
            if any(word in message_lower for word in self.responses[category]["keywords"]):
                return "negative"
        
        return "neutral"

    def log_conversation(self, user_message, bot_response, sentiment):
        """Log the conversation to the database"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            self.cursor.execute(
                "INSERT INTO conversations (user_id, timestamp, user_message, bot_response, sentiment) "
                "VALUES (?, ?, ?, ?, ?)",
                (self.user_id, timestamp, user_message, bot_response, sentiment)
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error logging conversation: {e}")

    def add_message(self, message, msg_type):
        """Add message to chat display"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, message + "\n", msg_type)
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def clear_window(self):
        """Clear current window content"""
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    MentalHealthChatbot()