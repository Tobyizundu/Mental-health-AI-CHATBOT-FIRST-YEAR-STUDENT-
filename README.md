# Mental-health-AI-CHATBOT-FIRST-YEAR-STUDENT-
A compassionate AI chatbot that provides immediate mental health support through empathetic conversations, mood tracking, and coping techniques. Built with care for students by a student.

# Mental Health AI Chatbot - Code Overview

## What This Code Does
This is a desktop application that provides mental health support for university students through an AI-powered chatbot interface.

## Architecture & Key Components

### 1. Database Setup (init_db)
- Creates SQLite database with two tables:
  - users: Stores student profiles (ID, name, password, login history)
  - conversations: Logs all chatbot interactions with timestamps and sentiment analysis

### 2. Smart Response System (setup_responses)
- Keyword-based matching for common student issues:
  - Academic stress, financial worries, anxiety, depression, loneliness, sleep issues
- Crisis detection for urgent situations (self-harm, suicide)
- Enhanced responses with empathy, normalization, and follow-up questions

### 3. User Interface (Tkinter)
- Welcome Screen: Login/Signup options
- Authentication System: 
  - Student ID validation (8 digits starting with "28")
  - Password security
  - Terms & conditions agreement
- Main Menu: Topic selection for different support areas
- Chat Interface: Real-time messaging with the AI

### 4. Advanced Features
- 5-second response delay for more natural conversations
- Typing indicators to simulate human interaction
- Sentiment analysis to tailor responses
- Emergency protocol for crisis situations
- Resource directory with university and national support services

## Safety & Privacy
- Confidential conversations with anonymized data
- Crisis escalation with immediate resource provision
- Secure authentication system
- Clear limitations - not a replacement for professional care

## Target Audience
First-year university students struggling with:
- Transition to university life
- Academic pressure and deadlines  
- Financial stress and budgeting
- Social isolation and homesickness
- Mental health challenges

## Technical Highlights
- Object-oriented design with clear separation of concerns
- Database persistence for conversation history
- Modular response system easy to expand
- User-friendly interface with intuitive navigation

This provides immediate, accessible mental health support while recognizing when professional help is needed - perfect for students who might hesitate to seek traditional counseling.
