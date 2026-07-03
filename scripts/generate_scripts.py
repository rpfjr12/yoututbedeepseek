"""
Generates scripts for stick figure Shorts.
Uses pre-written templates so no API key is needed.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SCRIPT_DIR

# Pre-written viral script templates
SCRIPTS = [
    {
        "title": "The Coffee Mistake",
        "lines": [
            "A man buys coffee every day.",
            "Five dollars per day.",
            "He does this for 10 years.",
            "That is 18 thousand dollars.",
            "He could have invested it.",
            "Instead he drank it.",
            "The rich do not buy coffee.",
            "They buy assets.",
            "Be the rich guy.",
        ]
    },
    {
        "title": "She Failed 100 Times",
        "lines": [
            "She applied for 100 jobs.",
            "All 100 said no.",
            "She had no money left.",
            "She started a small blog.",
            "No one read it for months.",
            "Then one post went viral.",
            "Now she makes 10 thousand a month.",
            "Failure is just practice.",
            "Keep going.",
        ]
    },
    {
        "title": "Your Brain Tricks You",
        "lines": [
            "Your brain lies to you every day.",
            "It says you need more stuff.",
            "A new phone will make you happy.",
            "A bigger car will fix your life.",
            "It is not true.",
            "Studies show experiences make you happier.",
            "Not things.",
            "Go outside.",
            "Your brain will thank you.",
        ]
    },
    {
        "title": "The 5 Second Rule",
        "lines": [
            "You have 5 seconds to act.",
            "If you hesitate, your brain talks you out of it.",
            "Fear takes over.",
            "Excuses take over.",
            "Count down from 5.",
            "5, 4, 3, 2, 1.",
            "Move before your brain stops you.",
            "That is how winners win.",
            "Try it right now.",
        ]
    },
    {
        "title": "How to Lose Friends",
        "lines": [
            "Want to lose all your friends?",
            "Here is how.",
            "Only talk about yourself.",
            "Never ask questions.",
            "Always cancel plans last minute.",
            "Borrow money and never pay back.",
            "Do this for one month.",
            "You will have zero friends.",
            "Or just be a good person instead.",
        ]
    },
    {
        "title": "The Millionaire Next Door",
        "lines": [
            "The millionaire lives next door.",
            "He drives a 10 year old car.",
            "He wears cheap shoes.",
            "He does not look rich.",
            "But he has 2 million dollars.",
            "He saved and invested for 30 years.",
            "The guy with the fancy car?",
            "He is renting it.",
            "Do not judge by appearances.",
        ]
    },
    {
        "title": "One Habit Changes Everything",
        "lines": [
            "One habit can change your life.",
            "Read for 20 minutes every day.",
            "That is one book per week.",
            "That is 52 books per year.",
            "In 5 years, you know more than 99 percent of people.",
            "Knowledge compounds like money.",
            "Start today.",
            "Not tomorrow.",
            "Today.",
        ]
    },
    {
        "title": "The Pareto Principle",
        "lines": [
            "20 percent of your effort gives 80 percent of results.",
            "80 percent of your time is wasted.",
            "Find the 20 percent that matters.",
            "Do more of that.",
            "Stop doing the rest.",
            "This is the Pareto Principle.",
            "Apply it to your work.",
            "Apply it to your life.",
            "Work smarter, not harder.",
        ]
    },
    {
        "title": "The Art of Saying No",
        "lines": [
            "Say no more often.",
            "No to bad opportunities.",
            "No to toxic people.",
            "No to things that waste your time.",
            "Every yes is a no to something else.",
            "Protect your time like money.",
            "Because time is money.",
            "Actually time is more valuable.",
            "You cannot make more time.",
        ]
    },
    {
        "title": "The Compound Effect",
        "lines": [
            "Small actions compound over time.",
            "Improving 1 percent every day.",
            "Makes you 37 times better in one year.",
            "One pushup today.",
            "Two pushups tomorrow.",
            "It seems small.",
            "But after one year you are strong.",
            "Start small.",
            "Let time do the work.",
        ]
    },
]

def save_scripts():
    """Save all scripts to text files."""
    os.makedirs(SCRIPT_DIR, exist_ok=True)
    
    for i, script in enumerate(SCRIPTS, 1):
        filename = f"{i:02d}_{script['title'].lower().replace(' ', '_')}.txt"
        filepath = os.path.join(SCRIPT_DIR, filename)
        
        with open(filepath, "w") as f:
            f.write(f"Title: {script['title']}\n")
            f.write(f"Duration: {len(script['lines']) * 3} seconds\n")
            f.write("-" * 30 + "\n")
            for line in script['lines']:
                f.write(line + "\n")
        
        print(f"Saved: {filepath}")
    
    print(f"\nTotal scripts saved: {len(SCRIPTS)}")

if __name__ == "__main__":
    save_scripts()
