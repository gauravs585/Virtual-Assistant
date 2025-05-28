from flask import Flask, render_template, request, jsonify, session
import pyttsx3
import requests
import random
import json
import os
from datetime import datetime, timedelta
import threading
import time
from googletrans import Translator
import openai
import yfinance as yf
from flask_session import Session
try:
    import speech_recognition as sr
    print("Speech recognition loaded successfully")
except ImportError:
    print("Speech recognition not available")
    sr = None

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Initialize components
translator = Translator()
recognizer = sr.Recognizer()

# Global storage (in production, use a database)
user_data = {
    'reminders': [],
    'notes': [],
    'preferences': {},
    'conversation_history': []
}

class VirtualAssistant:
    def __init__(self):
        self.commands = {
            'weather': self.get_weather,
            'news': self.get_news,
            'translate': self.translate_text,
            'reminder': self.set_reminder,
            'note': self.make_note,
            'notes': self.read_notes,
            'workout': self.start_workout,
            'recipe': self.get_recipe,
            'stock': self.get_stock_price,
            'fact': self.get_random_fact,
            'joke': self.tell_joke,
            'time': self.get_time,
            'date': self.get_date,
            'calculate': self.calculate,
            'search': self.web_search,
            'music': self.play_music,
            'movie': self.get_movie_info,
            'book': self.get_book_recommendation,
            'meditation': self.start_meditation,
            'quote': self.get_inspirational_quote,
            'trivia': self.ask_trivia,
            'calendar': self.manage_calendar,
            'email': self.compose_email,
            'password': self.generate_password,
            'color': self.color_psychology,
            'unit': self.convert_units
        }
    
    def process_command(self, command):
        """Process user command and return appropriate response"""
        command = command.lower().strip()
        
        # Store conversation
        user_data['conversation_history'].append({
            'timestamp': datetime.now().isoformat(),
            'user_input': command,
            'type': 'command'
        })
        
        try:
            # Check for specific command patterns
            for keyword, handler in self.commands.items():
                if keyword in command:
                    response = handler(command)
                    self.log_response(response)
                    return response
            
            # If no specific command found, use general AI response
            # If no specific command found, delegate to Gemini
            return self.ask_gemini(command)

            
        except Exception as e:
            error_msg = f"I encountered an error: {str(e)}. Please try again."
            self.log_response(error_msg)
            return error_msg
    
    def log_response(self, response):
        """Log assistant response"""
        user_data['conversation_history'].append({
            'timestamp': datetime.now().isoformat(),
            'assistant_response': response,
            'type': 'response'
        })
    
    def get_weather(self, command):
        """Get weather from Tomorrow.io"""
        import re
        api_key = os.environ.get("TOMORROW_API_KEY")
        if not api_key:
            return "🌦️ Weather service is unavailable. Please check the API key."

        # Extract city name from the command
        match = re.search(r'weather (in|for)? ?(.+)', command)
        city = match.group(2).strip() if match else "Mumbai"

        try:
            url = f"https://api.tomorrow.io/v4/weather/realtime?location={city}&apikey={api_key}"
            response = requests.get(url)
            data = response.json()

            values = data['data']['values']
            temp = values.get('temperature')
            code = values.get('weatherCode')
            condition = f"Weather code {code}"  # You can map to human-readable with Tomorrow.io docs

            return f"🌤️ Weather in {city.title()}:\n🌡️ Temperature: {temp}°C\n📋 Condition: {condition}"
        except Exception as e:
            return f"❌ Unable to fetch weather for {city}. Error: {str(e)}"
    
    def get_news(self, command):
        """Get latest news"""
        api_key = os.environ.get('NEWS_API_KEY')
        if not api_key:
            return "News service is currently unavailable."
        
        try:
            url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
            response = requests.get(url, timeout=10)
            news = response.json()
            
            if news.get('articles'):
                articles = news['articles'][:5]
                headlines = []
                for i, article in enumerate(articles, 1):
                    headlines.append(f"{i}. {article['title']}")
                
                return "📰 Top Headlines:\n" + "\n".join(headlines)
            else:
                return "Unable to fetch news at the moment."
                
        except Exception as e:
            return "News service is temporarily unavailable."
    
    def translate_text(self, command):
        """Translate text"""
        try:
            # Extract text and target language
            if 'to' in command:
                parts = command.split('to')
                if len(parts) >= 2:
                    text_part = parts[0].replace('translate', '').strip()
                    lang_part = parts[1].strip()
                    
                    # Map common language names to codes
                    lang_map = {
                        'spanish': 'es', 'french': 'fr', 'german': 'de',
                        'italian': 'it', 'portuguese': 'pt', 'russian': 'ru',
                        'chinese': 'zh', 'japanese': 'ja', 'korean': 'ko',
                        'arabic': 'ar', 'hindi': 'hi'
                    }
                    
                    target_lang = lang_map.get(lang_part.lower(), lang_part[:2])
                    
                    translation = translator.translate(text_part, dest=target_lang)
                    return f"🌐 Translation: '{text_part}' → '{translation.text}' ({target_lang.upper()})"
            
            return "Please specify what to translate and to which language. Example: 'translate hello to spanish'"
            
        except Exception as e:
            return "Translation service is currently unavailable."
    
    def set_reminder(self, command):
        """Set a reminder"""
        # Extract reminder text
        reminder_text = command.replace('reminder', '').replace('remind me to', '').strip()
        
        if not reminder_text:
            return "What would you like me to remind you about?"
        
        # For simplicity, set reminder for 1 hour from now
        reminder_time = datetime.now() + timedelta(hours=1)
        
        reminder = {
            'text': reminder_text,
            'time': reminder_time.isoformat(),
            'created': datetime.now().isoformat()
        }
        
        user_data['reminders'].append(reminder)
        
        return f"⏰ Reminder set: '{reminder_text}' for {reminder_time.strftime('%I:%M %p')}"
    
    def make_note(self, command):
        """Make a note"""
        note_text = command.replace('note', '').replace('make a note', '').strip()
        
        if not note_text:
            return "What would you like me to note down?"
        
        note = {
            'text': note_text,
            'created': datetime.now().isoformat()
        }
        
        user_data['notes'].append(note)
        
        return f"📝 Note saved: '{note_text}'"
    
    def read_notes(self, command):
        """Read all notes"""
        if not user_data['notes']:
            return "📝 You don't have any notes yet."
        
        notes_text = "📝 Your Notes:\n"
        for i, note in enumerate(user_data['notes'], 1):
            created = datetime.fromisoformat(note['created'])
            notes_text += f"{i}. {note['text']} (Created: {created.strftime('%m/%d %I:%M %p')})\n"
        
        return notes_text
    
    def start_workout(self, command):
        """Start a workout routine"""
        workouts = {
            'beginner': [
                "10 Jumping Jacks",
                "5 Push-ups (modified if needed)",
                "20-second Plank",
                "10 Squats",
                "5 Lunges each leg"
            ],
            'intermediate': [
                "20 Jumping Jacks",
                "10 Push-ups",
                "30-second Plank",
                "15 Squats",
                "10 Lunges each leg",
                "10 Mountain Climbers"
            ],
            'advanced': [
                "30 Jumping Jacks",
                "15 Push-ups",
                "45-second Plank",
                "20 Squats",
                "15 Lunges each leg",
                "20 Mountain Climbers",
                "10 Burpees"
            ]
        }
        
        level = 'beginner'
        if 'intermediate' in command:
            level = 'intermediate'
        elif 'advanced' in command:
            level = 'advanced'
        
        exercises = workouts[level]
        workout_text = f"💪 {level.title()} Workout Session:\n"
        
        for i, exercise in enumerate(exercises, 1):
            workout_text += f"{i}. {exercise}\n"
        
        workout_text += "\nRest 30 seconds between exercises. You've got this! 🔥"
        
        return workout_text
    
    def get_recipe(self, command):
        """Get a recipe suggestion"""
        dish = command.replace('recipe', '').replace('get recipe for', '').strip()
        
        recipes = {
            'pasta': {
                'ingredients': ['Pasta', 'Olive oil', 'Garlic', 'Tomatoes', 'Basil', 'Parmesan'],
                'instructions': '1. Boil pasta 2. Sauté garlic in oil 3. Add tomatoes 4. Mix with pasta 5. Add basil and cheese'
            },
            'sandwich': {
                'ingredients': ['Bread', 'Turkey', 'Cheese', 'Lettuce', 'Tomato', 'Mayo'],
                'instructions': '1. Toast bread 2. Spread mayo 3. Layer turkey and cheese 4. Add vegetables 5. Close sandwich'
            },
            'salad': {
                'ingredients': ['Mixed greens', 'Tomatoes', 'Cucumbers', 'Carrots', 'Dressing'],
                'instructions': '1. Wash greens 2. Chop vegetables 3. Mix together 4. Add dressing 5. Toss and serve'
            }
        }
        
        # Find matching recipe
        for recipe_name, recipe_data in recipes.items():
            if recipe_name in dish.lower():
                ingredients = ', '.join(recipe_data['ingredients'])
                return f"🍳 {recipe_name.title()} Recipe:\n\n📋 Ingredients: {ingredients}\n\n👨‍🍳 Instructions: {recipe_data['instructions']}"
        
        return f"🍳 I don't have a specific recipe for {dish}, but I can help you with pasta, sandwich, or salad recipes!"
    
    def get_stock_price(self, command):
        """Get stock price"""
        # Extract stock symbol
        words = command.split()
        symbol = "AAPL"  # default
        
        for word in words:
            if word.upper() in ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN', 'META', 'NFLX']:
                symbol = word.upper()
                break
        
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            current_price = info.get('currentPrice', 'N/A')
            previous_close = info.get('previousClose', 'N/A')
            
            if current_price != 'N/A' and previous_close != 'N/A':
                change = current_price - previous_close
                change_percent = (change / previous_close) * 100
                arrow = "📈" if change > 0 else "📉"
                
                return f"📊 {symbol} Stock Price:\n💰 Current: ${current_price:.2f}\n{arrow} Change: ${change:.2f} ({change_percent:.2f}%)"
            else:
                return f"Unable to fetch current price for {symbol}"
                
        except Exception as e:
            return f"Stock information for {symbol} is currently unavailable."
    
    def get_random_fact(self, command):
        """Get a random interesting fact"""
        facts = [
            "🦩 A group of flamingos is called a 'flamboyance'",
            "🐙 Octopuses have three hearts and blue blood",
            "🍯 Honey never spoils - edible honey was found in Egyptian tombs",
            "🦈 Sharks have been around longer than trees",
            "🌟 There are more possible games of chess than atoms in the observable universe",
            "🐨 Koalas sleep 18-22 hours per day",
            "🌙 The Moon is moving away from Earth at about 1.5 inches per year",
            "🐧 Penguins can jump 6 feet out of water",
            "🎵 Music can help plants grow faster",
            "🧠 Your brain uses about 20% of your body's energy"
        ]
        
        return f"🤓 Random Fact: {random.choice(facts)}"
    
    def tell_joke(self, command):
        """Tell a joke"""
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything! 😄",
            "Why did the math book look so sad? Because it had too many problems! 📚",
            "What do you call a fake noodle? An impasta! 🍝",
            "Why don't eggs tell jokes? They'd crack each other up! 🥚",
            "What do you call a bear with no teeth? A gummy bear! 🐻",
            "Why did the coffee file a police report? It got mugged! ☕",
            "What's the best thing about Switzerland? I don't know, but the flag is a big plus! 🇨🇭",
            "Why don't some couples go to the gym? Because some relationships don't work out! 💪",
            "What do you call a dinosaur that crashes his car? Tyrannosaurus Wrecks! 🦕",
            "Why did the scarecrow win an award? He was outstanding in his field! 🌾"
        ]
        
        return random.choice(jokes)
    
    def get_time(self, command):
        """Get current time"""
        now = datetime.now()
        return f"🕐 Current time: {now.strftime('%I:%M %p')}"
    
    def get_date(self, command):
        """Get current date"""
        now = datetime.now()
        return f"📅 Today is {now.strftime('%A, %B %d, %Y')}"
    
    def calculate(self, command):
        """Perform calculations"""
        # Extract mathematical expression
        import re
        
        # Find numbers and operators
        expression = re.sub(r'[^0-9+\-*/().\s]', '', command)
        expression = expression.strip()
        
        if not expression:
            return "Please provide a mathematical expression to calculate."
        
        try:
            result = eval(expression)
            return f"🧮 Calculation: {expression} = {result}"
        except:
            return "I couldn't calculate that. Please use numbers and basic operators (+, -, *, /)."
    
    def web_search(self, command):
        """Simulate web search"""
        query = command.replace('search', '').replace('search for', '').strip()
        
        if not query:
            return "What would you like me to search for?"
        
        return f"🔍 I would search for '{query}' on the web. In a full implementation, this would return actual search results!"
    
    def play_music(self, command):
        """Music player simulation"""
        song = command.replace('play', '').replace('music', '').strip()
        
        if not song:
            song = "your favorite playlist"
        
        return f"🎵 Now playing: {song}. Enjoy the music! 🎧"
    
    def get_movie_info(self, command):
        """Get movie information"""
        movie = command.replace('movie', '').replace('tell me about', '').strip()
        
        if not movie:
            return "Which movie would you like to know about?"
        
        return f"🎬 '{movie.title()}' - I'd provide detailed movie information including cast, plot, and ratings in a full implementation!"
    
    def get_book_recommendation(self, command):
        """Get book recommendations"""
        genres = {
            'fiction': ['The Great Gatsby', '1984', 'To Kill a Mockingbird'],
            'sci-fi': ['Dune', 'The Hitchhiker\'s Guide', 'Ender\'s Game'],
            'mystery': ['Gone Girl', 'The Girl with the Dragon Tattoo', 'Sherlock Holmes'],
            'romance': ['Pride and Prejudice', 'The Notebook', 'Me Before You'],
            'fantasy': ['Harry Potter', 'Lord of the Rings', 'Game of Thrones']
        }
        
        # Detect genre
        genre = 'fiction'  # default
        for g in genres.keys():
            if g in command.lower():
                genre = g
                break
        
        books = genres[genre]
        book = random.choice(books)
        
        return f"📚 Book Recommendation ({genre}): '{book}' - A great choice for {genre} lovers!"
    
    def start_meditation(self, command):
        """Start meditation session"""
        return """🧘‍♀️ Meditation Session Starting:
        
1. Find a comfortable position
2. Close your eyes gently
3. Take 3 deep breaths
4. Focus on your breathing
5. Let thoughts pass without judgment
6. Continue for 5-10 minutes

Remember: Meditation is practice, not perfection. 🌸"""
    
    def get_inspirational_quote(self, command):
        """Get inspirational quote"""
        quotes = [
            "The only way to do great work is to love what you do. - Steve Jobs ✨",
            "Life is what happens to you while you're busy making other plans. - John Lennon 🌟",
            "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt 💫",
            "It is during our darkest moments that we must focus to see the light. - Aristotle 🌅",
            "The only impossible journey is the one you never begin. - Tony Robbins 🚀",
            "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill 💪",
            "The way to get started is to quit talking and begin doing. - Walt Disney 🎯",
            "Don't let yesterday take up too much of today. - Will Rogers 🌈",
            "You learn more from failure than from success. Don't let it stop you. Failure builds character. 🔥",
            "Be yourself; everyone else is already taken. - Oscar Wilde 🦋"
        ]
        
        return f"💭 {random.choice(quotes)}"
    
    def ask_trivia(self, command):
        """Ask trivia question"""
        trivia = [
            {"q": "What is the capital of Australia?", "a": "Canberra"},
            {"q": "Which planet is known as the Red Planet?", "a": "Mars"},
            {"q": "What is the largest mammal in the world?", "a": "Blue Whale"},
            {"q": "In which year did World War II end?", "a": "1945"},
            {"q": "What is the chemical symbol for gold?", "a": "Au"},
            {"q": "Which country has the most natural lakes?", "a": "Canada"},
            {"q": "What is the fastest land animal?", "a": "Cheetah"},
            {"q": "How many sides does a hexagon have?", "a": "Six"}
        ]
        
        question = random.choice(trivia)
        return f"🧠 Trivia Question: {question['q']}\n\n(Think about it, then ask me for the answer!)"
    
    def manage_calendar(self, command):
        """Calendar management"""
        return "📅 Calendar feature would integrate with your calendar app to show events, set appointments, and manage your schedule!"
    
    def compose_email(self, command):
        """Email composition helper"""
        return "📧 Email composer would help you draft professional emails with templates and suggestions!"
    
    def generate_password(self, command):
        """Generate secure password"""
        import string
        
        length = 12
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(random.choice(characters) for _ in range(length))
        
        return f"🔐 Generated secure password: {password}\n(Make sure to store it safely!)"
    
    def color_psychology(self, command):
        """Color psychology insights"""
        colors = {
            'red': 'Energy, passion, urgency - stimulates appetite and creates urgency',
            'blue': 'Trust, calm, stability - reduces stress and promotes focus',
            'green': 'Nature, growth, harmony - promotes balance and reduces eye strain',
            'yellow': 'Happiness, optimism, creativity - stimulates mental activity',
            'purple': 'Luxury, creativity, mystery - encourages creativity and deep thinking',
            'orange': 'Enthusiasm, warmth, caution - promotes enthusiasm and social interaction',
            'black': 'Elegance, power, sophistication - creates dramatic effect',
            'white': 'Purity, simplicity, cleanliness - creates sense of space and calm'
        }
        
        color = None
        for c in colors.keys():
            if c in command.lower():
                color = c
                break
        
        if color:
            return f"🎨 Color Psychology - {color.title()}: {colors[color]}"
        else:
            return "🎨 Ask me about the psychology of specific colors: red, blue, green, yellow, purple, orange, black, or white!"
    
    def convert_units(self, command):
        """Unit conversion"""
        # Simple temperature conversion example
        if 'celsius to fahrenheit' in command or 'c to f' in command:
            import re
            numbers = re.findall(r'-?\d+\.?\d*', command)
            if numbers:
                celsius = float(numbers[0])
                fahrenheit = (celsius * 9/5) + 32
                return f"🌡️ {celsius}°C = {fahrenheit}°F"
        
        elif 'fahrenheit to celsius' in command or 'f to c' in command:
            import re
            numbers = re.findall(r'-?\d+\.?\d*', command)
            if numbers:
                fahrenheit = float(numbers[0])
                celsius = (fahrenheit - 32) * 5/9
                return f"🌡️ {fahrenheit}°F = {celsius:.1f}°C"
        
        return "🔄 I can convert temperatures (e.g., '25 celsius to fahrenheit'). More conversions coming soon!"
    
    def list_available_models(self):
        """List available Gemini models for debugging"""
        try:
            import google.generativeai as genai
            
            api_key = os.environ.get("GEMINI_API_KEY")
            if not api_key:
                return "🔑 Gemini API key is not set."
                
            genai.configure(api_key=api_key)
            
            models = []
            for model in genai.list_models():
                if 'generateContent' in model.supported_generation_methods:
                    models.append(model.name)
            
            return f"📋 Available Gemini models: {', '.join(models)}"
            
        except Exception as e:
            return f"❌ Error listing models: {str(e)}"

    def ask_gemini(self, prompt):
        """Use Google Gemini to generate a response"""
        try:
            import google.generativeai as genai

            api_key = os.environ.get("GEMINI_API_KEY")
            if not api_key:
                return "🔑 Gemini API key is not set."

            genai.configure(api_key=api_key)

            # ✅ Try different model names based on current API availability
            model_names = [
                "gemini-1.5-flash-latest",
                "gemini-1.5-flash",
                "gemini-1.5-pro-latest", 
                "gemini-1.5-pro",
                "gemini-1.0-pro-latest",
                "gemini-1.0-pro",
                "gemini-pro"
            ]
            
            model = None
            for model_name in model_names:
                try:
                    model = genai.GenerativeModel(model_name=model_name)
                    break  # Success, use this model
                except Exception as e:
                    continue  # Try next model
            
            if not model:
                return "🤖 No available Gemini models found. Using built-in responses instead."

            # Generate response with proper configuration
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    candidate_count=1,
                    max_output_tokens=1000,
                    temperature=0.7,
                )
            )

            if response.text:
                return f"🤖 Gemini says: {response.text}"
            else:
                return "🤖 Gemini didn't provide a response. Let me help you with my built-in features instead!"
            
        except Exception as e:
            # More detailed error handling
            error_msg = str(e)
            if "404" in error_msg or "not found" in error_msg.lower():
                return "🤖 I'm having trouble connecting to Gemini right now. Let me try to help you with my built-in responses instead!"
            elif "API_KEY" in error_msg or "authentication" in error_msg.lower():
                return "🔑 Gemini API key issue. Please check your API key configuration."
            elif "quota" in error_msg.lower() or "limit" in error_msg.lower():
                return "🤖 Gemini usage limit reached. Let me help you with my built-in features instead!"
            else:
                return f"🤖 I encountered an issue with Gemini. Let me help you with my built-in features instead!"
            
# Initialize assistant
assistant = VirtualAssistant()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        response = assistant.process_command(user_message)
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/capabilities')
def get_capabilities():
    capabilities = {
        'categories': {
            'Information': ['weather', 'news', 'stock prices', 'time', 'date', 'facts', 'trivia'],
            'Productivity': ['reminders', 'notes', 'calendar', 'email composer', 'password generator'],
            'Entertainment': ['jokes', 'music', 'movie info', 'book recommendations', 'quotes'],
            'Health & Wellness': ['workout routines', 'meditation', 'recipes'],
            'Utilities': ['translation', 'calculator', 'unit conversion', 'color psychology', 'web search']
        },
        'sample_commands': [
            "What's the weather in New York?",
            "Tell me a joke",
            "Set a reminder to call mom",
            "Translate hello to Spanish",
            "Start a beginner workout",
            "Get me some news",
            "What's Apple's stock price?",
            "Make a note about the meeting",
            "Tell me a random fact",
            "Generate a password",
            "What can you do?"
        ]
    }
    
    return jsonify(capabilities)

@app.route('/api/history')
def get_history():
    return jsonify(user_data['conversation_history'][-20:])  # Last 20 interactions

@app.route('/api/notes')
def get_notes():
    return jsonify(user_data['notes'])

@app.route('/api/reminders')
def get_reminders():
    return jsonify(user_data['reminders'])

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
