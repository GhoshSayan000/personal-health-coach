import random

class HealthCoachAgent:
    def __init__(self):
        self.memory = []
        self.mood_responses = {
            "sad": [
                "I’m really glad you told me this. You’re not weak for feeling this way.",
                "That sounds heavy. I’m here with you, take your time.",
                "It’s okay to feel low sometimes. You’re not alone."
            ],
            "stress": [
                "Stress can quietly affect both mind and body. Let’s slow things down together.",
                "I hear pressure in your words. We’ll break this step by step."
            ],
            "healthy": [
                "That’s great to hear! Let’s see how we can make your routine even better.",
                "Nice! Small improvements can make a big difference."
            ]
        }

    def detect_mood(self, text):
        text = text.lower()
        if any(word in text for word in ["sad", "depressed", "low", "tired", "hopeless"]):
            return "sad"
        if any(word in text for word in ["stress", "anxious", "pressure", "overwhelmed"]):
            return "stress"
        return "healthy"

    def reply(self, user_input):
        mood = self.detect_mood(user_input)
        response = random.choice(self.mood_responses[mood])

        self.memory.append({
            "user": user_input,
            "agent": response,
            "mood": mood
        })

        return response

    def generate_report(self):
        moods = [m["mood"] for m in self.memory]
        summary = {
            "total_messages": len(self.memory),
            "sad_mentions": moods.count("sad"),
            "stress_mentions": moods.count("stress"),
            "healthy_mentions": moods.count("healthy")
        }

        report = f"""
        🩺 Health Interaction Summary

        Total Interactions: {summary['total_messages']}
        Emotional Low Signals: {summary['sad_mentions']}
        Stress Signals: {summary['stress_mentions']}
        Positive/Healthy Signals: {summary['healthy_mentions']}

        ⚠️ This is NOT a medical diagnosis.
        Recommended: Maintain routine, sleep well, hydrate, and consult a professional if symptoms persist.
        """

        return report.strip()
