# 🤖 Pratik AI - Advanced Virtual Assistant

A comprehensive, feature-rich virtual assistant built with Flask, designed for deployment on Render.com. Pratik AI combines voice recognition, text processing, and multiple API integrations to provide a seamless conversational experience.

## ✨ Features

### 🗣️ **Communication**
- **Voice Recognition**: Speak directly to the assistant using Web Speech API
- **Text-to-Speech**: Get audio responses for accessibility
- **Text Input**: Traditional chat interface for text-based interaction
- **Conversation History**: Track and review past interactions

### 🌟 **Core Capabilities**

#### 📊 **Information Services**
- **Weather Reports**: Real-time weather data for any city
- **News Updates**: Latest headlines and breaking news
- **Stock Prices**: Real-time stock market information
- **Random Facts**: Educational and entertaining trivia
- **Time & Date**: Current time and date information

#### 🛠️ **Productivity Tools**
- **Smart Reminders**: Set and manage personal reminders
- **Note Taking**: Create and retrieve personal notes
- **Password Generator**: Create secure passwords
- **Calculator**: Perform mathematical calculations
- **Unit Conversion**: Convert between different units (temperature, etc.)

#### 🎭 **Entertainment**
- **Jokes**: A collection of clean, family-friendly humor
- **Inspirational Quotes**: Motivational content for daily inspiration
- **Trivia Questions**: Interactive knowledge challenges
- **Book Recommendations**: Curated suggestions by genre
- **Movie Information**: Details about films and entertainment

#### 🏃‍♂️ **Health & Wellness**
- **Workout Routines**: Customized exercise plans (beginner, intermediate, advanced)
- **Meditation Guide**: Guided relaxation and mindfulness sessions
- **Recipe Suggestions**: Healthy meal ideas and cooking instructions

#### 🌍 **Utility Services**
- **Language Translation**: Multi-language translation support
- **Color Psychology**: Insights into color meanings and effects
- **Web Search**: Intelligent search assistance
- **Email Composer**: Help with professional email drafting

### 🎨 **User Interface**
- **Modern Design**: Clean, responsive interface with gradient effects
- **Glass Morphism**: Contemporary visual effects and styling
- **Mobile Responsive**: Optimized for all device sizes
- **Quick Actions**: One-click access to common commands
- **Modal Dialogs**: Organized capability and history views

## 🚀 Deployment on Render

### Prerequisites
- GitHub account
- Render.com account

### Step-by-Step Deployment

1. **Prepare Your Repository**
   ```bash
   git clone <your-repo>
   cd virtual-assistant
   ```

2. **Create Required Files**
   - Ensure all files are in your repository:
     - `app.py` (main application)
     - `requirements.txt` (dependencies)
     - `Dockerfile` (container configuration)
     - `templates/index.html` (web interface)

3. **Deploy to Render**
   - Connect your GitHub repository to Render
   - Choose "Web Service" deployment
   - Configure environment variables (optional API keys)
   - Deploy automatically

4. **Environment Variables** (Optional)
   Set these in Render's dashboard for full functionality:
   ```
   SECRET_KEY=your-secure-secret-key
   OPENWEATHER_API_KEY=your-weather-api-key
   NEWS_API_KEY=your-news-api-key
   OPENAI_API_KEY=your-openai-key
   ```

### 🔑 API Keys Setup (Optional)

The assistant works without API keys but has enhanced features when configured:

- **OpenWeatherMap** (Weather): [Sign up here](https://openweathermap.org/api)
- **NewsAPI** (News): [Sign up here](https://newsapi.org/)
- **OpenAI** (Enhanced AI): [Sign up here](https://platform.openai.com/)

## 💻 Local Development

### Setup
```bash
# Clone repository
git clone <your-repo>
cd virtual-assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables (optional)
cp .env.example .env
# Edit .env with your API keys

# Run application
python app.py
```

### Development Server
The app will run on `http://localhost:5000`

## 🎯 Usage Examples

### Voice Commands
- "What's the weather in New York?"
- "Tell me a joke"
- "Set a reminder to call mom"
- "Translate hello to Spanish"
- "Start a beginner workout"

### Text Commands
- Type any question or command in the chat interface
- Use quick action buttons for common requests
- View capabilities and conversation history via modal dialogs

## 🏗️ Architecture

### Backend (Flask)
- **RESTful API**: Clean endpoints for all assistant functions
- **Modular Design**: Organized command processing system
- **Error Handling**: Robust error management and user feedback
- **Session Management**: Conversation state and user data storage

### Frontend (HTML/JavaScript)
- **Progressive Web App**: Modern web technologies
- **Real-time Communication**: AJAX-based chat interface
- **Voice Integration**: Web Speech API for voice recognition
- **Responsive Design**: Mobile-first approach

### Data Flow
1. User input (voice/text) → Frontend
2. Frontend → Flask API endpoint
3. Flask processes command → External APIs (if needed)
4. Response formatted → Frontend
5. Display to user + optional text-to-speech

## 🔧 Customization

### Adding New Commands
1. Add command handler to `VirtualAssistant` class in `app.py`
2. Register command in the `commands` dictionary
3. Update capabilities endpoint if needed