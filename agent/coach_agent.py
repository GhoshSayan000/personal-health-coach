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

        # ---- Deep analysis ----
        mood = self.detect_mood(text)
        urgency = self.detect_urgency(text)
        keywords = self.extract_keywords(text)

        # ---- Memory construction ----
        memory_entry = {
            "text": user_text,
            "mood": mood,
            "urgency": urgency,
            "keywords": keywords,
            "time": timestamp
        }
        self.memory.append(memory_entry)
        self.context_memory.append(memory_entry)
        self.summarize_context()
        
        # ---- Context synthesis (last few turns) ----
        recent_moods = [m["mood"] for m in self.context_memory[-5:]]
        repeated_sadness = recent_moods.count("sad") >= 2
        repeated_stress = recent_moods.count("stress") >= 2

        # ---- Conversational framing (friend energy) ----
        openers = [
            "Hey, I’m really glad you said that.",
            "Alright, pause with me for a second.",
            "I hear you — and I’m not brushing this off.",
            "Thanks for trusting me with this.",
            "I’m right here with you."
        ]

        reflections = [
            "What you’re describing feels heavy.",
            "That sounds like it’s been sitting with you for a while.",
            "Anyone in your place would feel shaken.",
            "That’s not a small thing to carry.",
            "It makes sense that this is affecting you."
        ]

        gentle_questions = [
            "Do you want to talk about what started this?",
            "What part of this hurts the most right now?",
            "Has this been building up for days, or did something happen today?",
            "What’s been looping in your head lately?",
            "If you had words for the feeling, what would they be?"
        ]

        grounding_lines = [
            "Take a slow breath with me for a moment.",
            "You don’t have to solve everything right now.",
            "We can take this one step at a time.",
            "You’re not weak for feeling this way.",
            "I’m not going anywhere."
        ]

        # ---- Crisis overrides everything ----
        if urgency == "crisis" or mood == "crisis":
            return self.crisis_response()

        # ---- Mood-based reasoning with depth ----

        if mood == "sad":
            response_parts = [
                random.choice(openers),
                random.choice(reflections),
                self.generate_sad_response(text, keywords),
            ]
            if repeated_sadness:
                response_parts.append(
                    "I’ve noticed this feeling coming up more than once. That tells me it really matters."
                )
            response_parts.append(random.choice(gentle_questions))
            response_parts.append(random.choice(grounding_lines))
            return " ".join(response_parts)

        elif mood == "stress":
            response_parts = [
                random.choice(openers),
                "It sounds like your mind has been running nonstop.",
                self.generate_stress_response(text, keywords),
            ]
            if repeated_stress:
                response_parts.append(
                    "When stress keeps repeating like this, it usually means you’ve been pushing yourself too hard."
                )
            response_parts.append(random.choice(gentle_questions))
            response_parts.append(random.choice(grounding_lines))
            return " ".join(response_parts)

        else:
            response_parts = [
                random.choice(openers),
                self.generate_positive_response(text, keywords),
                random.choice([
                    "Tell me more — I’m genuinely curious.",
                    "What made you think about this just now?",
                    "How are you feeling about it in this exact moment?",
                    "That sounds meaningful to you.",
                    "I like the way you’re thinking about this."
                ])
            ]
            return " ".join(response_parts)


        # ---------- MOOD DETECTION ----------

    def detect_mood(self, text: str) -> str:
        """
        Advanced mood detection using contextual cues, sentiment patterns,
        and philosophical/emotional heuristics for nuanced understanding.
        Returns one of: 'crisis', 'sad', 'stress', 'neutral', 'happy'
        """
        text_lower = text.lower()

        # ---- 1. Explicit self-harm intent (strong signals) ----
        explicit_intent_patterns = [
            r"\bi want to die\b", r"\bkill myself\b", r"\bend my life\b",
            r"\bcommit suicide\b", r"\bi will die\b", r"\bi plan to die\b",
            r"\bi don't want to live\b"
        ]

        # ---- 2. Passive death wishes ----
        passive_death_patterns = [
            r"\bi wish i was dead\b", r"\bi wish i wouldn't wake up\b",
            r"\bit would be better if i disappeared\b",
            r"\bi want everything to stop\b",
            r"\btired of existing\b"
        ]

        # ---- 3. Hopelessness / collapse language ----
        hopelessness_patterns = [
            r"\bno future\b", r"\bno way out\b", r"\bnothing will change\b",
            r"\btrapped forever\b", r"\bpointless\b", r"\bmeaningless\b",
            r"\bno reason to live\b"
        ]

        # ---- 4. Self-worth erosion ----
        self_worth_patterns = [
            r"\bworthless\b", r"\bi am a burden\b",
            r"\beveryone would be better without me\b",
            r"\bi hate myself\b", r"\bi am broken\b",
            r"\bi am a failure\b"
        ]

        # ---- 5. Pain intensity markers ----
        pain_intensity_markers = [
            "unbearable", "too much", "can't handle", "over the edge",
            "suffocating", "crushing", "drowning", "breaking apart"
        ]

        # ---- 6. Immediacy markers ----
        immediacy_markers = [
            "right now", "tonight", "today", "soon",
            "can't go on", "at my limit"
        ]

        # ---- 7. Protective language absence (important philosophical cue) ----
        protective_terms = [
            "maybe", "but", "hope", "trying", "getting help",
            "talking to someone", "not sure"
        ]

        # ---- Scoring logic (human-like reasoning) ----
        score = 0


        def match_any(patterns):
            return any(re.search(p, text_lower) for p in patterns)

        if match_any(explicit_intent_patterns):
            score += 5

        if match_any(passive_death_patterns):
            score += 4

        if match_any(hopelessness_patterns):
            score += 3

        if match_any(self_worth_patterns):
            score += 2

        score += sum(1 for w in pain_intensity_markers if w in text_lower)
        score += sum(1 for w in immediacy_markers if w in text_lower)

        # Reduce score slightly if protective language exists (ambivalence signal)
        if any(w in text_lower for w in protective_terms):
            score -= 1

        # ---- Philosophical thresholding ----
        # Crisis is not a word match, it's:
        # intent + hopelessness + intensity + time pressure
        if score >= 6:
            return "crisis"

        # 2️⃣ SAD / LOW MOOD
        sad_patterns = [
            r"\bsad\b", r"\blonely\b", r"\bempty\b", r"\bhopeless\b",
            r"\bcry\b", r"\btired of life\b", r"\bbroken\b", r"\bdepressed\b",
            r"\bheartbroken\b", r"\bdisappointed\b", r"\bmelancholy\b",
            r"\bunhappy\b", r"\bgrief\b"
        ]
        for pattern in sad_patterns:
            if re.search(pattern, text_lower):
                return "sad"

        # 3️⃣ STRESS / ANXIETY
        stress_patterns = [
            r"\bstressed\b", r"\banxious\b", r"\boverwhelmed\b", r"\bworried\b",
            r"\bpressure\b", r"\bpanic\b", r"\bburnout\b", r"\btense\b",
            r"\bfrustrated\b", r"\bnervous\b", r"\bconfused\b"
        ]
        for pattern in stress_patterns:
            if re.search(pattern, text_lower):
                return "stress"

        # 4️⃣ ENHANCED HAPPINESS / POSITIVE MOOD DETECTION
        happy_patterns = [
            r"\bhappy\b", r"\bjoy\b", r"\bexcited\b", r"\brelieved\b",
            r"\bcontent\b", r"\bgrateful\b", r"\boptimistic\b", r"\bpeaceful\b",
            r"\bproud\b", r"\blight-hearted\b", r"\bserene\b", r"\bdelighted\b",
            r"\belated happiness\b", r"\bsmiling\b", r"\blaughing\b"
        ]

        # Contextual positive phrases (implied happiness even without explicit words)
        positive_phrase_patterns = [
            r"felt so much better", r"finally at ease", r"things are looking up",
            r"made progress", r"a new sense of calm", r"improved mood lately",
            r"more confident", r"enjoying life", r"feeling less burdened",
            r"that made my day", r"that helped me", r"light at the end",
            r"positive change"
        ]

        # Relational / connection-based happiness
        connection_patterns = [
            r"feeling loved", r"in love with", r"close to", r"supported by",
            r"filled with hope", r"grateful for", r"cherish", r"thankful for"
        ]


        # Lifestyle / well-being indicators that imply happiness
        wellbeing_patterns = [
            r"good sleep", r"sleeping better", r"healthy habits", r"more energetic",
            r"feeling balanced", r"taking care of myself", r"have inner peace"
        ]

        # Evaluate explicit happy terms
        for pattern in happy_patterns:
            if re.search(pattern, text_lower):
                return "happy"

        # Evaluate positive phrase contexts
        for pattern in positive_phrase_patterns:
            if re.search(pattern, text_lower):
                return "happy"

        # Evaluate relational / connection-based positivity
        for pattern in connection_patterns:
            if re.search(pattern, text_lower):
                return "happy"

        # Evaluate lifestyle/wellbeing based happiness
        for pattern in wellbeing_patterns:
            if re.search(pattern, text_lower):
                return "happy"

        # Subtle heuristic: a mix of many low-level positive words
        low_positive_triggers = [
            "smile", "peace", "fun", "hope", "calm", "relax", "good moments",
            "uplift", "light", "spark", "joyful"
        ]
        pos_sub_count = sum(1 for w in low_positive_triggers if w in text_lower)

        # If multiple low-level positive triggers exist **and no strong negative terms**
        if pos_sub_count >= 2 and not any(
            neg in text_lower for neg in ["sad", "pain", "hurt", "worried", "stressed", "anxious"]
        ):
            return "happy"

        
        # ---- Philosophical fallback (subtle reasoning) ----
        philo_mood = self.philosophical_sentiment_heuristic(text_lower)
        if philo_mood == "healthy":
            return "happy"
        if philo_mood in ["sad", "stress", "neutral"]:
            return philo_mood

            
        # If nothing above matched, do not call it happy
        return "neutral"


        # 5️⃣ PHILOSOPHICAL / CONTEXTUAL SENTIMENT HEURISTICS
        # Inspired by existentialism, stoicism, cognitive appraisal theory, and narrative psychology


    def philosophical_sentiment_heuristic(self, text: str) -> str:
        text_lower = text.lower()

        # --- Existential themes ---
        meaning_words = [
            "meaning", "purpose", "why am i", "what's the point",
            "exist", "existence", "identity", "who am i"
        ]
        nihilism_words = [
            "meaningless", "pointless", "nothing matters",
            "empty", "void", "absurd"
        ]

        # --- Stoic / control dichotomy ---
        control_words = [
            "control", "handle", "manage", "accept", "let go",
            "focus on", "one step", "calm"
        ]
        helpless_words = [
            "can't control", "no control", "powerless",
            "trapped", "stuck", "forced"
        ]

        # --- Cognitive distortion markers (CBT-inspired) ---
        absolutist_words = [
            "always", "never", "everyone", "no one",
            "completely", "totally", "forever"
        ]
        self_blame_words = [
            "my fault", "i failed", "i am useless",
            "i am worthless", "i messed up"
        ]

        # --- Emotional polarity ---
        positive_words = [
            "good", "better", "hope", "love", "relief",
            "peace", "calm", "grateful", "safe"
        ]
        negative_words = [
            "bad", "worse", "pain", "hate", "fear",
            "hurt", "angry", "alone", "tired"
        ]

        # --- Count signals ---
        pos_count = sum(1 for w in positive_words if w in text_lower)
        neg_count = sum(1 for w in negative_words if w in text_lower)

        meaning_count = sum(1 for w in meaning_words if w in text_lower)
        nihilism_count = sum(1 for w in nihilism_words if w in text_lower)

        control_count = sum(1 for w in control_words if w in text_lower)
        helpless_count = sum(1 for w in helpless_words if w in text_lower)

        distortion_count = sum(1 for w in absolutist_words if w in text_lower)
        self_blame_count = sum(1 for w in self_blame_words if w in text_lower)

        # --- Interpretative reasoning ---
        if nihilism_count > 0 and neg_count > 0:
            return "sad"

        if meaning_count > 0 and neg_count > 0:
            return "stress"

        if control_count > helpless_count and pos_count >= neg_count:
            return "healthy"

        if helpless_count > 0 and (distortion_count > 0 or self_blame_count > 0):
            return "stress"

        if pos_count > 0 and neg_count > 0:
            return "stress"

        if pos_count > neg_count and pos_count > 0:
            return "healthy"
        if neg_count > pos_count and neg_count > 0:
            return "sad"

        if meaning_count > 0 and pos_count == 0 and neg_count == 0:
            return "neutral"

        return "neutral"



        # ---------- URGENCY DETECTION ----------
    def detect_urgency(self, text: str) -> str:
        """
        Human-like urgency detection using:
        - intent strength
        - immediacy & time markers
        - emotional intensity
        - first-person risk signals
        - escalation logic
        """

        text = text.lower()

        # Strong self-harm intent (highest risk)
        high_risk_patterns = [
            r"\bi want to die\b",
            r"\bkill myself\b",
            r"\bend my life\b",
            r"\bcommit suicide\b",
            r"\bno reason to live\b",
            r"\bi can't go on\b",
            r"\bi am done\b",
            r"\bi give up\b"
        ]

        # Immediacy indicators (time + action)
        immediacy_markers = [
            r"\bnow\b", r"\btonight\b", r"\btoday\b",
            r"\bright now\b", r"\bimmediately\b",
            r"\bcan't wait\b"
        ]

        # Emotional overload / collapse language
        overload_markers = [
            "overwhelmed", "trapped", "suffocating",
            "unbearable", "too much", "breaking",
            "falling apart", "lost control", "numb"
        ]

        # Hopelessness / existential despair
        hopeless_markers = [
            "nothing will change", "no hope", "pointless",
            "meaningless", "empty inside", "worthless",
            "nobody cares", "alone forever"
        ]

        # First-person vulnerability (raises risk score)
        first_person = ["i", "me", "my", "myself"]

        urgency_score = 0

        # Check high-risk intent
        for p in high_risk_patterns:
            if re.search(p, text):
                urgency_score += 5

        # Check immediacy
        for p in immediacy_markers:
            if re.search(p, text):
                urgency_score += 3

        # Emotional overload
        for w in overload_markers:
            if w in text:
                urgency_score += 2

        # Hopelessness
        for w in hopeless_markers:
            if w in text:
                urgency_score += 2

        # First-person framing increases seriousness
        if any(fp in text.split() for fp in first_person):
            urgency_score += 1

        # Repetition / intensity (exclamation, caps)
        if text.count("!") >= 2:
            urgency_score += 1
        if any(word.isupper() and len(word) > 3 for word in text.split()):
            urgency_score += 1

        # Final interpretation (agent-friendly levels)
        if urgency_score >= 7:
            return "crisis"
        elif urgency_score >= 4:
            return "high"
        elif urgency_score >= 2:
            return "medium"
        else:
            return "normal"



        # ---------- KEYWORD EXTRACTION ----------
    def extract_keywords(self, text: str) -> list:
        """
        More human-like keyword extraction using:
        - semantic weighting
        - emotional salience
        - phrase detection
        - repetition importance
        """

        text = text.lower()

        # Basic cleanup
        words = re.findall(r'\b[a-z]+\b', text)

        # Stopwords (expanded)
        stopwords = {
            "i","am","the","and","a","to","my","it","me","you","is","of","in","on",
            "that","this","for","with","was","are","be","have","has","had","at",
            "but","or","so","if","they","them","we","he","she","his","her","their"
        }

        # Emotionally important words get higher weight
        emotional_words = {
            "sad","lonely","empty","hopeless","tired","broken","anxious","stressed",
            "afraid","panic","hurt","cry","pressure","overwhelmed","fear","pain",
            "worthless","angry","guilty","lost","confused","depressed"
        }

        # Crisis-weighted words (very high importance)
        crisis_words = {
            "die","death","suicide","kill","end","life","save","alone","nobody"
        }

        # Remove stopwords
        filtered = [w for w in words if w not in stopwords]

        # Frequency scoring
        freq = {}
        for w in filtered:
            freq[w] = freq.get(w, 0) + 1

        scored_keywords = {}

        for word, count in freq.items():
            score = count

            # Emotional amplification
            if word in emotional_words:
                score += 3

            # Crisis amplification
            if word in crisis_words:
                score += 6

            # Longer words often carry more meaning
            if len(word) > 6:
                score += 1

            scored_keywords[word] = score

        # Detect meaningful 2-word phrases (mini thought-units)
        phrases = []
        for i in range(len(filtered) - 1):
            w1, w2 = filtered[i], filtered[i + 1]
            if w1 not in stopwords and w2 not in stopwords:
                phrases.append(f"{w1} {w2}")

        # Rank keywords
        ranked = sorted(scored_keywords.items(), key=lambda x: x[1], reverse=True)
        top_words = [w for w, _ in ranked[:4]]

        # Add strongest phrase if meaningful
        if phrases:
            top_words.append(max(phrases, key=len))

        return top_words



       # ---------- RESPONSE GENERATORS ----------
    def generate_sad_response(self, text: str, keywords: list) -> str:
        base = [
            "I hear you. Feeling {keywords} can be really heavy.",
            "Your feelings are valid. {keywords} must be hard to go through.",
            "I’m here with you. Can you tell me more about {keywords}?",
            "It’s okay to feel this way. {keywords} can really weigh on the heart.",
            "I understand. Experiencing {keywords} can be exhausting emotionally.",
            "Thank you for sharing about {keywords}. I can see why it feels difficult.",
            "I can imagine how {keywords} might make things challenging for you.",
            "Feeling {keywords} is natural. Let’s take it one step at a time together.",
            "I’m listening. {keywords} sounds like it’s been tough on you lately.",
            "It sounds like {keywords} is really affecting you. I’m here to understand.",
            "I know it’s not easy to talk about {keywords}, but you’re doing great by sharing.",
            "Sometimes {keywords} can feel overwhelming. I’m here to help process it.",
            "You’re not alone in feeling {keywords}. Let’s explore this together.",
            "I can feel the weight of {keywords} in what you’re saying. Tell me more if you can.",
            "Talking about {keywords} takes courage. I’m glad you shared it with me.",
            "Thank you for trusting me with your thoughts about {keywords}. I’m here for you.",
            "I notice {keywords} is significant for you. Let’s discuss how it impacts your life.",
            "Feeling {keywords} is part of the human experience, and I want to support you through it.",
            "I hear the sadness in {keywords}. You can share more if you feel comfortable.",
            "It’s okay that {keywords} is bothering you. We can unpack this together."
        ]
        return random.choice(base).format(
            keywords=", ".join(keywords) if keywords else "this"
        )


    def generate_stress_response(self, text: str, keywords: list) -> str:
        """
        Generates nuanced, empathetic, and guiding responses for users under stress.
        Uses context, keywords, and human psychology principles to respond meaningfully.
        """
        base = [
            "Stress can weigh heavily on anyone. Let’s carefully think through {keywords} together and find some clarity.",
            "I hear that {keywords} is causing tension. It's completely normal to feel this way. Can you share more details?",
            "Take a slow, deep breath. {keywords} might feel overwhelming now, but we can explore it step by step.",
            "I understand that {keywords} is stressful. Sometimes naming it out loud helps. What part of {keywords} feels hardest?",
            "It’s okay to feel overwhelmed by {keywords}. Let’s focus on what you can control and ease the pressure gradually.",
            "Stress often comes from many layers. {keywords} might be one of them. Can you tell me what’s most pressing?",
            "You’re not alone feeling stressed about {keywords}. Let’s break it down together and see what might help.",
            "I notice {keywords} is creating tension. Reflecting on it can bring insight. What thoughts come to mind when you think about it?",
            "Feeling stressed is a signal from your mind and body. {keywords} is important to discuss. Can you describe your feelings more?",
            "Sometimes stress clouds our perspective. Talking about {keywords} can help release some of that weight. How does it make you feel physically?",
            "Let’s approach {keywords} gently. You deserve calm and understanding as we work through it together.",
            "I’m here with you while you process {keywords}. Naming your stress is the first step to finding balance.",
            "Acknowledging stress is brave. {keywords} might feel heavy now, but together we can find small ways to relieve it.",
            "Let’s explore {keywords} from different angles. What part of it triggers the strongest reaction in you?",
            "It’s okay if {keywords} feels like too much. We can take small steps to untangle this stress slowly."
        ]

        chosen_response = random.choice(base)
        return chosen_response.format(
            keywords=", ".join(keywords) if keywords else "everything"
        )


    def generate_positive_response(self, text: str, keywords: list) -> str:
        base = [
            "Thanks for sharing. {keywords} sounds interesting, tell me more.",
            "I’m glad you told me that. What else about {keywords}?",
            "I’m listening carefully. How does {keywords} make you feel?",
            "Nice! Good going, {keywords} sounds interesting.",
            "That’s really insightful. Can you elaborate more on {keywords}?",
            "I appreciate you opening up about {keywords}. How does it affect your day-to-day?",
            "It’s great that you mentioned {keywords}. What emotions come with it?",
            "Wow, {keywords} seems important. Let’s explore that together.",
            "Your thoughts on {keywords} are valuable. Tell me more.",
            "I hear you about {keywords}. How does it influence your current mood?",
            "Interesting perspective on {keywords}. How long have you felt this way?",
            "I’m curious about your experience with {keywords}. Can you describe it further?",
            "It sounds like {keywords} matters a lot to you. Let’s discuss more.",
            "Thanks for sharing your view on {keywords}. How does it impact you?",
            "I can see why {keywords} would be significant. Let’s unpack it a bit."
        ]

        chosen_response = random.choice(base)
        return chosen_response.format(
            keywords=", ".join(keywords) if keywords else "that"
        )


    # ---------- CRISIS RESPONSE ----------
    def crisis_response(self) -> str:
        responses = [
            (
                "I’m really glad you told me how you’re feeling. What you’re going through sounds overwhelming, "
                "and you don’t have to face it alone.\n\n"
                "You deserve care, understanding, and real support. If you can, please consider reaching out "
                "to someone you trust right now—a close friend, a family member, or a mental health professional.\n\n"
                "If you feel in immediate danger, please contact your local emergency number or a suicide prevention "
                "hotline in your country.\n\n"
                "You matter. Your life has value. I’m here with you, and I’m listening."
            ),
            (
                "Thank you for trusting me with something this heavy. I can hear how much pain you’re in, "
                "and it’s important to take this seriously.\n\n"
                "You deserve help and compassion, not judgment. Please reach out to someone who can be with you "
                "right now—whether that’s a loved one or a trained professional.\n\n"
                "If there’s any immediate risk, please call your local emergency services or a crisis hotline.\n\n"
                "You are not weak for needing help. You are human, and your life matters."
            ),
            (
                "I’m really sorry that you’re feeling this way, and I’m glad you spoke up. These feelings can be "
                "incredibly intense, but they don’t define your worth or your future.\n\n"
                "It’s important to get real-time support. Please consider contacting someone you trust or a mental "
                "health professional as soon as possible.\n\n"
                "If you’re in immediate danger, please call your emergency number or a suicide prevention hotline.\n\n"
                "You are important. You deserve to be here. I’m staying with you and taking you seriously."
            ),
            (
                "I hear you, and I’m really glad you reached out. What you’re experiencing is serious, and you "
                "deserve care, safety, and support.\n\n"
                "Please try to connect with someone right now—a friend, family member, or counselor—so you don’t "
                "have to hold this alone.\n\n"
                "If you feel unsafe, please contact local emergency services or a crisis hotline immediately.\n\n"
                "Your life has meaning, even if it doesn’t feel that way right now. I’m here with you."
            )
        ]

        return random.choice(responses)

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
