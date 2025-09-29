import json
import random
import re
from datetime import datetime
from collections import defaultdict
import os

class SimpleChatbot:
    def __init__(self, knowledge_file='chatbot_knowledge.json'):
        self.knowledge_file = knowledge_file
        self.knowledge = self.load_knowledge()
        self.context = []
        self.user_name = None
        self.conversation_count = 0
        
    def load_knowledge(self) -> dict:
        """Load or create knowledge base"""
        default_knowledge = {
            'greetings': {
                'patterns': ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good evening'],
                'responses': [
                    "Hello! How can I help you today?",
                    "Hi there! What's on your mind?",
                    "Hey! Nice to meet you!",
                    "Greetings! How are you doing?"
                ]
            },
            'farewell': {
                'patterns': ['bye', 'goodbye', 'see you', 'farewell', 'exit', 'quit'],
                'responses': [
                    "Goodbye! Have a great day!",
                    "See you later! Take care!",
                    "Farewell! It was nice chatting with you!",
                    "Bye! Come back soon!"
                ]
            },
            'name_question': {
                'patterns': ['what is your name', 'who are you', 'your name'],
                'responses': [
                    "I'm a friendly chatbot created to assist you!",
                    "You can call me ChatBot! I'm here to help.",
                    "I'm an AI assistant. Nice to meet you!"
                ]
            },
            'user_name': {
                'patterns': ['my name is', 'i am', "i'm", 'call me'],
                'responses': [
                    "Nice to meet you, {name}!",
                    "Hello {name}! Great to know your name!",
                    "Pleasure to meet you, {name}!"
                ]
            },
            'how_are_you': {
                'patterns': ['how are you', 'how do you do', 'how are things', 'whats up', "what's up"],
                'responses': [
                    "I'm doing great, thanks for asking! How about you?",
                    "I'm functioning perfectly! How can I assist you?",
                    "All systems running smoothly! What brings you here?",
                    "I'm wonderful! How are you feeling today?"
                ]
            },
            'thanks': {
                'patterns': ['thank', 'thanks', 'appreciate', 'grateful'],
                'responses': [
                    "You're welcome!",
                    "Happy to help!",
                    "Anytime! That's what I'm here for!",
                    "My pleasure!"
                ]
            },
            'help': {
                'patterns': ['help', 'what can you do', 'commands', 'capabilities'],
                'responses': [
                    "I can chat with you, answer questions, tell jokes, and learn from our conversations! Try asking me about weather, time, jokes, or just chat casually.",
                    "I'm here to assist! You can ask me questions, have a conversation, or teach me new responses. Just type 'learn' to teach me something new!"
                ]
            },
            'weather': {
                'patterns': ['weather', 'temperature', 'forecast', 'raining', 'sunny'],
                'responses': [
                    "I don't have real-time weather data, but I hope it's nice where you are!",
                    "I wish I could check the weather for you! Maybe try a weather app?",
                    "I can't access weather information, but I hope you're having a beautiful day!"
                ]
            },
            'time': {
                'patterns': ['time', 'what time', 'current time', 'clock'],
                'responses': [
                    f"The current time is {datetime.now().strftime('%I:%M %p')}",
                    f"It's {datetime.now().strftime('%I:%M %p')} right now!"
                ]
            },
            'date': {
                'patterns': ['date', 'what date', 'today', 'day'],
                'responses': [
                    f"Today is {datetime.now().strftime('%B %d, %Y')}",
                    f"The current date is {datetime.now().strftime('%A, %B %d, %Y')}"
                ]
            },
            'joke': {
                'patterns': ['joke', 'funny', 'laugh', 'humor'],
                'responses': [
                    "Why don't programmers like nature? It has too many bugs! 🐛",
                    "Why do Python programmers prefer dark mode? Because light attracts bugs! 💡",
                    "What's a programmer's favorite hangout place? The Foo Bar! 🍺",
                    "How many programmers does it take to change a light bulb? None, that's a hardware problem! 💡"
                ]
            },
            'compliment': {
                'patterns': ['you are good', 'you are smart', 'you are awesome', 'love you'],
                'responses': [
                    "Thank you! You're pretty awesome yourself! 😊",
                    "That's so kind of you to say!",
                    "You're making me blush! Thanks! ☺️"
                ]
            },
            'age': {
                'patterns': ['how old', 'your age', 'when were you born'],
                'responses': [
                    "I'm ageless! Just lines of code running eternally.",
                    "Age is just a number... and I don't really have one!",
                    "I was born when this program started, so I'm pretty young!"
                ]
            }
        }
        
        try:
            with open(self.knowledge_file, 'r') as f:
                loaded = json.load(f)
                # Merge with defaults (keep learned responses)
                for key, value in default_knowledge.items():
                    if key not in loaded:
                        loaded[key] = value
                return loaded
        except FileNotFoundError:
            with open(self.knowledge_file, 'w') as f:
                json.dump(default_knowledge, f, indent=2)
            return default_knowledge
    
    def save_knowledge(self):
        """Save updated knowledge base"""
        with open(self.knowledge_file, 'w') as f:
            json.dump(self.knowledge, f, indent=2)
    
    def extract_name(self, text: str) -> str:
        """Extract name from user input"""
        patterns = [
            r"my name is (\w+)",
            r"i am (\w+)",
            r"i'm (\w+)",
            r"call me (\w+)",
            r"this is (\w+)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                return match.group(1).capitalize()
        return None
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate simple word-based similarity"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    def find_intent(self, text: str) -> tuple:
        """Find matching intent from knowledge base"""
        text_lower = text.lower()
        best_match = None
        best_score = 0
        
        for intent, data in self.knowledge.items():
            for pattern in data['patterns']:
                # Exact substring match
                if pattern in text_lower:
                    return intent, data['responses']
                
                # Fuzzy matching
                similarity = self.calculate_similarity(pattern, text_lower)
                if similarity > best_score and similarity > 0.5:
                    best_score = similarity
                    best_match = (intent, data['responses'])
        
        return best_match if best_match else (None, None)
    
    def generate_response(self, user_input: str) -> str:
        """Generate response based on user input"""
        self.conversation_count += 1
        
        # Check for name extraction
        name = self.extract_name(user_input)
        if name:
            self.user_name = name
        
        # Find intent
        intent, responses = self.find_intent(user_input)
        
        if intent:
            response = random.choice(responses)
            
            # Handle time/date responses (update dynamically)
            if intent in ['time', 'date']:
                if 'time' in intent:
                    response = f"The current time is {datetime.now().strftime('%I:%M %p')}"
                else:
                    response = f"Today is {datetime.now().strftime('%A, %B %d, %Y')}"
            
            # Personalize if name is known
            if '{name}' in response and self.user_name:
                response = response.format(name=self.user_name)
            elif self.user_name and random.random() > 0.8:
                response = f"{self.user_name}, {response.lower()}"
            
            self.context.append({'user': user_input, 'bot': response, 'intent': intent})
            return response
        
        # Context-aware default responses
        default_responses = [
            "That's interesting! Tell me more.",
            "I see. Can you elaborate on that?",
            "Hmm, I'm not sure I understand completely. Can you rephrase?",
            "Interesting perspective! What makes you say that?",
            "I'm still learning. Could you teach me more about this?",
            "That's a new one for me! Type 'learn' if you want to teach me.",
            "I don't have a good answer for that yet, but I'm always learning!"
        ]
        
        response = random.choice(default_responses)
        self.context.append({'user': user_input, 'bot': response, 'intent': 'unknown'})
        return response
    
    def learn_from_feedback(self, user_input: str, correct_response: str):
        """Learn from user corrections"""
        # Create new intent or add to existing
        intent_name = f"learned_{len([k for k in self.knowledge.keys() if k.startswith('learned')])}"
        
        # Check if similar pattern exists
        for intent, data in self.knowledge.items():
            for pattern in data['patterns']:
                if self.calculate_similarity(pattern, user_input.lower()) > 0.7:
                    # Add to existing intent
                    if correct_response not in data['responses']:
                        data['responses'].append(correct_response)
                    self.save_knowledge()
                    print("✓ Thanks! I've learned to improve my response!")
                    return
        
        # Create new intent
        self.knowledge[intent_name] = {
            'patterns': [user_input.lower()],
            'responses': [correct_response]
        }
        self.save_knowledge()
        print("✓ Thanks! I've learned something new!")
    
    def get_statistics(self):
        """Get conversation statistics"""
        intent_counts = defaultdict(int)
        for conv in self.context:
            intent_counts[conv.get('intent', 'unknown')] += 1
        
        print("\n=== CONVERSATION STATISTICS ===")
        print(f"Total messages: {self.conversation_count}")
        print(f"Learned intents: {len([k for k in self.knowledge.keys() if k.startswith('learned')])}")
        print(f"\nTop intents:")
        for intent, count in sorted(intent_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  {intent}: {count}")
    
    def chat(self):
        """Main chat loop"""
        print("="*60)
        print("🤖 AI CHATBOT WITH LEARNING")
        print("="*60)
        print("Commands:")
        print("  'learn' - Teach me something new")
        print("  'stats' - View conversation statistics")
        print("  'quit' or 'exit' - End conversation")
        print("="*60)
        
        print("\nBot: Hello! I'm a learning chatbot. What's your name?")
        
        while True:
            user_input = input("\nYou: ").strip()
            
            if not user_input:
                continue
            
            # Check for special commands
            if user_input.lower() in ['quit', 'exit']:
                response = self.generate_response("goodbye")
                print(f"\nBot: {response}")
                self.get_statistics()
                break
            
            if user_input.lower() == 'learn':
                print("\n--- TEACHING MODE ---")
                question = input("What should I respond to? ")
                answer = input("What should I say? ")
                self.learn_from_feedback(question, answer)
                print("--- TEACHING MODE END ---")
                continue
            
            if user_input.lower() == 'stats':
                self.get_statistics()
                continue
            
            # Generate and display response
            response = self.generate_response(user_input)
            print(f"\nBot: {response}")


if __name__ == "__main__":
    bot = SimpleChatbot()
    bot.chat()