import random
from datetime import datetime
import re

class HealthCoachAgent:
    def __init__(self):
        self.memory = []
        self.context_memory = []

    # ---------- MAIN REPLY ----------
    def reply(self, user_text: str) -> str:
        text = user_text.lower().strip()
        timestamp = datetime.now().strftime("%H:%M")

        # Analyze input and extract mood, urgency, keywords
        mood = self.detect_mood(text)
        urgency = self.detect_urgency(text)
        keywords = self.extract_keywords(text)

        # Store in memory
        memory_entry = {
            "text": user_text,
            "mood": mood,
            "urgency": urgency,
            "keywords": keywords,
            "time": timestamp
        }
        self.memory.append(memory_entry)
        self.context_memory.append(memory_entry)

        # Generate response based on context
        if urgency == "crisis":
            return self.crisis_response()
        elif mood == "sad":
            return self.generate_sad_response(text, keywords)
        elif mood == "stress":
            return self.generate_stress_response(text, keywords)
        else:
            return self.generate_positive_response(text, keywords)

    # ---------- MOOD DETECTION ----------
    def detect_mood(self, text: str) -> str:
        crisis_words = [
            "want to die", "kill myself", "end my life",
            "please save me", "no reason to live",
            "i can't go on", "suicide", "i hate myself"
        ]
        sad_words = [
            "sad", "lonely", "empty", "hopeless",
            "cry", "tired of life", "broken", "depressed"
        ]
        stress_words = [
            "stressed", "anxious", "overwhelmed",
            "pressure", "panic", "burnout", "tense"
        ]

        for w in crisis_words:
            if w in text:
                return "crisis"
        for w in sad_words:
            if w in text:
                return "sad"
        for w in stress_words:
            if w in text:
                return "stress"
        return "healthy"

    # ---------- URGENCY DETECTION ----------
    def detect_urgency(self, text: str) -> str:
        crisis_patterns = [
            r"i want to die", r"kill myself", r"suicide", r"end my life"
        ]
        for pattern in crisis_patterns:
            if re.search(pattern, text):
                return "crisis"
        return "normal"

    # ---------- KEYWORD EXTRACTION ----------
    def extract_keywords(self, text: str) -> list:
        words = re.findall(r'\b\w+\b', text)
        common_ignore = {"i","am","the","and","a","to","my","it","me","you","is","of"}
        keywords = [w for w in words if w not in common_ignore]
        return keywords[:5]

    # ---------- RESPONSE GENERATORS ----------
    def generate_sad_response(self, text: str, keywords: list) -> str:
        base = [
            "I hear you. Feeling {keywords} can be really heavy.",
            "Your feelings are valid. {keywords} must be hard to go through.",
            "I’m here with you. Can you tell me more about {keywords}?"
        ]
        return random.choice(base).format(keywords=", ".join(keywords) if keywords else "this")

    def generate_stress_response(self, text: str, keywords: list) -> str:
        base = [
            "Stress can really weigh on you. Let’s think through {keywords} together.",
            "It’s okay to feel overwhelmed with {keywords}. I’m listening.",
            "Take a deep breath. Tell me more about {keywords} if you can."
        ]
        return random.choice(base).format(keywords=", ".join(keywords) if keywords else "everything")

    def generate_positive_response(self, text: str, keywords: list) -> str:
        base = [
            "Thanks for sharing. {keywords} sounds interesting, tell me more.",
            "I’m glad you told me that. What else about {keywords}?",
            "I’m listening carefully. How does {keywords} make you feel?"
        ]
        return random.choice(base).format(keywords=", ".join(keywords) if keywords else "that")

    # ---------- CRISIS RESPONSE ----------
    def crisis_response(self) -> str:
        return (
            "I’m really glad you told me this. What you’re feeling is serious, "
            "and you deserve help and care.\n\n"
            "Please reach out immediately to a trusted friend, family member, "
            "or a mental health professional.\n\n"
            "If you are in immediate danger, call your local emergency number "
            "or a suicide prevention hotline.\n\n"
            "You matter. Your life has value. I’m here with you."
        )

    # ---------- CONTEXTUAL MEMORY CLEANUP ----------
    def summarize_context(self):
        # Keep last 20 messages for context
        if len(self.context_memory) > 20:
            self.context_memory = self.context_memory[-20:]

    # ---------- REPORT GENERATION ----------
    def generate_report(self) -> str:
        if not self.memory:
            return "No conversation data available."

        total = len(self.memory)
        crisis = sum(1 for m in self.memory if m["mood"] == "crisis")
        sad = sum(1 for m in self.memory if m["mood"] == "sad")
        stress = sum(1 for m in self.memory if m["mood"] == "stress")
        healthy = total - (crisis + sad + stress)

        # Top keywords used by user
        keywords = []
        for m in self.memory:
            keywords.extend(m.get("keywords", []))
        top_keywords = list(set(keywords))[:10]

        report = (
            "📊 PERSONAL WELLNESS SUMMARY\n"
            "----------------------------\n"
            f"Total interactions: {total}\n"
            f"Crisis signals: {crisis}\n"
            f"Low mood signals: {sad}\n"
            f"Stress indicators: {stress}\n"
            f"Positive/Neutral interactions: {healthy}\n\n"
            f"Top topics mentioned: {', '.join(top_keywords) if top_keywords else 'None'}\n\n"
            "This summary is based on conversation patterns only.\n"
            "It is NOT a medical diagnosis.\n\n"
            "If emotional distress feels intense or persistent, professional support is strongly recommended."
        )
        return report
