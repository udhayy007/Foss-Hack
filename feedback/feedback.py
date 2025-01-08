import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd
import time

class FeedbackManager:
    def __init__(self):
        self.db_path = "feedback/feedback.db"
        self.setup_database()

    def setup_database(self):
        """Create feedback table if it doesn't exist"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rating INTEGER,
                usability_score INTEGER,
                feature_satisfaction INTEGER,
                missing_features TEXT,
                improvement_suggestions TEXT,
                user_experience TEXT,
                timestamp DATETIME
            )
        ''')
        conn.commit()
        conn.close()

    def save_feedback(self, feedback_data):
        """Save feedback to database"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            INSERT INTO feedback (
                rating, usability_score, feature_satisfaction,
                missing_features, improvement_suggestions,
                user_experience, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            feedback_data['rating'],
            feedback_data['usability_score'],
            feedback_data['feature_satisfaction'],
            feedback_data['missing_features'],
            feedback_data['improvement_suggestions'],
            feedback_data['user_experience'],
            datetime.now()
        ))
        conn.commit()
        conn.close()

    def get_feedback_stats(self):
        """Get feedback statistics"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query("SELECT * FROM feedback", conn)
        conn.close()
        
        if df.empty:
            return {
                'avg_rating': 0,
                'avg_usability': 0,
                'avg_satisfaction': 0,
                'total_responses': 0
            }
        
        return {
            'avg_rating': df['rating'].mean(),
            'avg_usability': df['usability_score'].mean(),
            'avg_satisfaction': df['feature_satisfaction'].mean(),
            'total_responses': len(df)
        }

    def render_feedback_form(self):
        """Render the feedback form"""
        st.markdown("""
            <style>
            .feedback-container {
                background-color: rgba(255, 255, 255, 0.05);
                padding: 20px;
                border-radius: 10px;
                margin: 10px 0;
            }
            .feedback-header {
                color: #E0E0E0;
                font-size: 1.2em;
                margin-bottom: 20px;
                text-align: center;
                padding: 10px;
                background: linear-gradient(90deg, #4CAF50, #2196F3);
                border-radius: 5px;
            }
            .feedback-section {
                margin: 15px 0;
                padding: 15px;
                border-radius: 8px;
                background: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            .feedback-label {
                color: #E0E0E0;
                font-size: 0.9em;
                margin-bottom: 5px;
            }
            .feedback-input {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 5px;
                padding: 10px;
                margin-top: 5px;
            }
            .feedback-submit {
                background: linear-gradient(90deg, #4CAF50, #2196F3);
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                width: 100%;
                margin-top: 20px;
            }
            .feedback-emoji {
                font-size: 1.5em;
                margin-right: 10px;
            }
            .stTextInput>div>div>input {
                background-color: rgba(255, 255, 255, 0.05);
                color: #E0E0E0;
            }
            .stTextArea>div>div>textarea {
                background-color: rgba(255, 255, 255, 0.05);
                color: #E0E0E0;
            }
            </style>
        """, unsafe_allow_html=True)

        st.markdown('<div class="feedback-header">📝 Share Your Feedback</div>', unsafe_allow_html=True)

        with st.form("feedback_form", clear_on_submit=True):
            # Rating Section
            st.markdown('<div class="feedback-section">', unsafe_allow_html=True)
            st.markdown('<div class="feedback-label">⭐ Overall Rating</div>', unsafe_allow_html=True)
            
            # Create star rating with slider
            rating = st.slider("", min_value=1, max_value=5, value=3, key="rating_slider")
            
            # Display stars based on rating
            col1, col2, col3 = st.columns([1, 3, 1])
            with col2:
                st.markdown(
                    f'<div style="text-align: center; font-size: 24px; margin-top: -10px;">'
                    f'{"⭐" * rating}'
                    f'</div>',
                    unsafe_allow_html=True
                )
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Usability Section
            st.markdown('<div class="feedback-section">', unsafe_allow_html=True)
            st.markdown('<div class="feedback-label">🎯 Usability Score</div>', unsafe_allow_html=True)
            usability_options = {
                "Very Poor": "💔",
                "Poor": "😟",
                "Average": "😐",
                "Good": "👍",
                "Excellent": "🎉"
            }
            usability = st.select_slider(
                "",
                options=list(usability_options.keys()),
                value="Average",
                format_func=lambda x: f"{usability_options[x]} {x}",
                key="usability_slider",
                help="How easy was it to use our application?"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Feature Satisfaction
            st.markdown('<div class="feedback-section">', unsafe_allow_html=True)
            st.markdown('<div class="feedback-label">✨ Feature Satisfaction</div>', unsafe_allow_html=True)
            satisfaction_options = {
                "Very Dissatisfied": "😢",
                "Dissatisfied": "😕",
                "Neutral": "😐",
                "Satisfied": "😊",
                "Very Satisfied": "😍"
            }
            satisfaction = st.select_slider(
                "",
                options=list(satisfaction_options.keys()),
                value="Neutral",
                format_func=lambda x: f"{satisfaction_options[x]} {x}",
                key="satisfaction_slider"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Features and Improvements
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div class="feedback-section">', unsafe_allow_html=True)
                st.markdown('<div class="feedback-label">💡 Missing Features</div>', unsafe_allow_html=True)
                missing_features = st.text_area("", placeholder="What features would you like to see?",
                                             help="Tell us what features you think are missing")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="feedback-section">', unsafe_allow_html=True)
                st.markdown('<div class="feedback-label">🔄 Suggestions</div>', unsafe_allow_html=True)
                improvements = st.text_area("", placeholder="How can we improve?",
                                        help="Share your suggestions for improvement")
                st.markdown('</div>', unsafe_allow_html=True)
            
            # User Experience
            st.markdown('<div class="feedback-section">', unsafe_allow_html=True)
            st.markdown('<div class="feedback-label">💭 Your Experience</div>', unsafe_allow_html=True)
            experience = st.text_area("", placeholder="Tell us about your experience...",
                                   help="Share your thoughts about using our application")
            st.markdown('</div>', unsafe_allow_html=True)

            submitted = st.form_submit_button("Submit Feedback 🚀", 
                                           help="Click to submit your feedback",
                                           use_container_width=True)

            if submitted:
                # Create progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Simulate processing with animation
                for i in range(100):
                    progress_bar.progress(i + 1)
                    if i < 30:
                        status_text.text("Processing feedback... 📝")
                    elif i < 60:
                        status_text.text("Analyzing responses... 🔍")
                    elif i < 90:
                        status_text.text("Saving to database... 💾")
                    else:
                        status_text.text("Finalizing... ✨")
                    time.sleep(0.01)

                # Save feedback
                feedback_data = {
                    'rating': rating,
                    'usability_score': list(usability_options.keys()).index(usability) + 1,
                    'feature_satisfaction': list(satisfaction_options.keys()).index(satisfaction) + 1,
                    'missing_features': missing_features,
                    'improvement_suggestions': improvements,
                    'user_experience': experience
                }
                self.save_feedback(feedback_data)
                
                # Clear progress elements
                progress_bar.empty()
                status_text.empty()
                
                # Show success message with animation
                success_container = st.empty()
                success_container.markdown("""
                    <div style="text-align: center; padding: 20px; background: linear-gradient(90deg, rgba(76, 175, 80, 0.1), rgba(33, 150, 243, 0.1)); border-radius: 10px;">
                        <h2 style="color: #4CAF50;">Thank You! 🎉</h2>
                        <p style="color: #E0E0E0;">Your feedback helps us improve Smart Resume AI</p>
                    </div>
                """, unsafe_allow_html=True)
                
                st.balloons()
                time.sleep(3)  # Keep success message visible for 3 seconds
                success_container.empty()  # Clear success message

    def render_feedback_stats(self):
        """Render feedback statistics"""
        stats = self.get_feedback_stats()
        
        st.markdown("""
            <div style="text-align: center; padding: 15px; background: linear-gradient(90deg, rgba(76, 175, 80, 0.1), rgba(33, 150, 243, 0.1)); border-radius: 10px; margin-bottom: 20px;">
                <h3 style="color: #E0E0E0;">Feedback Overview 📊</h3>
            </div>
        """, unsafe_allow_html=True)
        
        cols = st.columns(4)
        metrics = [
            {"label": "Total Responses", "value": f"{stats['total_responses']:,}", "delta": "↗"},
            {"label": "Avg Rating", "value": f"{stats['avg_rating']:.1f}/5.0", "delta": "⭐"},
            {"label": "Usability Score", "value": f"{stats['avg_usability']:.1f}/5.0", "delta": "🎯"},
            {"label": "Satisfaction", "value": f"{stats['avg_satisfaction']:.1f}/5.0", "delta": "😊"}
        ]
        
        for col, metric in zip(cols, metrics):
            col.markdown(f"""
                <div style="background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 8px; text-align: center;">
                    <div style="color: #B0B0B0; font-size: 0.9em;">{metric['label']}</div>
                    <div style="font-size: 1.5em; color: #4CAF50; margin: 5px 0;">{metric['value']}</div>
                    <div style="color: #E0E0E0; font-size: 1.2em;">{metric['delta']}</div>
                </div>
            """, unsafe_allow_html=True)
