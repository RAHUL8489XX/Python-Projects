# 🐍 Python Projects

A collection of 4 intermediate-level Python projects showcasing web scraping, database management, cryptography, and natural language processing.

## 📋 Table of Contents
- [Projects Overview](#projects-overview)
- [Project 1: Web Scraper & Data Analyzer](#project-1-web-scraper--data-analyzer)
- [Project 2: Personal Finance Tracker](#project-2-personal-finance-tracker)
- [Project 3: Password Manager](#project-3-password-manager)
- [Project 4: AI Chatbot with NLP](#project-4-ai-chatbot-with-nlp)
- [Installation](#installation)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Projects Overview

| Project | Technologies | Difficulty | Key Features |
|---------|-------------|------------|--------------|
| Web Scraper | BeautifulSoup, Pandas, Matplotlib | ⭐⭐⭐ | Data extraction, analysis, visualization |
| Finance Tracker | SQLite, Matplotlib | ⭐⭐⭐ | Database management, reporting, charts |
| Password Manager | Cryptography, Fernet | ⭐⭐⭐⭐ | Encryption, secure storage, password generation |
| AI Chatbot | NLP, Pattern Matching | ⭐⭐⭐ | Learning capability, context awareness |

---

## Project 1: Web Scraper & Data Analyzer

### 📝 Description
A web scraping tool that extracts quotes from websites, analyzes the data, and creates visualizations. Perfect for learning web scraping fundamentals and data analysis.

### ✨ Features
- Scrapes data from websites using BeautifulSoup
- Extracts quotes, authors, and tags
- Performs data analysis (word counts, frequencies)
- Creates visual charts and graphs
- Exports data to CSV format

### 🛠️ Technologies Used
- **BeautifulSoup4** - HTML parsing
- **Requests** - HTTP requests
- **Pandas** - Data manipulation
- **Matplotlib** - Data visualization

### 📦 Installation
```bash
pip install requests beautifulsoup4 pandas matplotlib
```

### 🚀 Usage
```bash
python web_scraper.py
```

### 📊 Output
- `scraped_quotes.csv` - Extracted data
- `tag_analysis.png` - Visualization chart

### 🎓 Learning Outcomes
- Web scraping techniques
- HTTP requests handling
- Data parsing and cleaning
- Data visualization
- CSV file operations

---

## Project 2: Personal Finance Tracker

### 📝 Description
A command-line finance management application that helps track income and expenses with detailed reporting and visual analytics.

### ✨ Features
- Add income and expense transactions
- Categorize transactions
- Calculate balance automatically
- Generate monthly/yearly summaries
- Create pie charts for expense breakdown
- View transaction history
- SQLite database for persistent storage

### 🛠️ Technologies Used
- **SQLite3** - Database management
- **Matplotlib** - Chart generation
- **datetime** - Date handling

### 📦 Installation
```bash
pip install matplotlib
```

### 🚀 Usage
```bash
python finance_tracker.py
```

### 💾 Database Schema
```sql
transactions (
    id INTEGER PRIMARY KEY,
    date TEXT,
    type TEXT,
    category TEXT,
    amount REAL,
    description TEXT
)
```

### 📊 Output
- `finance.db` - SQLite database
- `expense_breakdown.png` - Visual report

### 🎓 Learning Outcomes
- SQL database operations
- CRUD operations
- Data aggregation and reporting
- Object-oriented programming
- User input validation

---

## Project 3: Password Manager

### 📝 Description
A secure password management system with encryption, master password protection, and automatic password generation capabilities.

### ✨ Features
- Master password authentication with SHA256 hashing
- AES-128 encryption using Fernet
- Generate strong random passwords
- Search and filter saved credentials
- Update/delete passwords
- Export backup functionality
- Case-insensitive service lookup

### 🛠️ Technologies Used
- **Cryptography** - Fernet encryption
- **hashlib** - Password hashing
- **secrets** - Secure random generation
- **getpass** - Secure password input

### 📦 Installation
```bash
pip install cryptography
```

### 🚀 Usage
```bash
python password_manager.py
```

### 🔒 Security Features
- Master password never stored in plain text
- All passwords encrypted with Fernet (AES-128)
- Secure random password generation
- Encrypted file storage

### 📁 Files Created
- `.secret.key` - Encryption key
- `.master.hash` - Master password hash
- `passwords.enc` - Encrypted password database

### ⚠️ Security Notes
- Keep `.secret.key` file safe
- Use a strong master password
- Don't share encrypted files without the key
- Backup your data regularly

### 🎓 Learning Outcomes
- Cryptography fundamentals
- Secure password handling
- Binary file operations
- Security best practices
- User authentication systems

---

## Project 4: AI Chatbot with NLP

### 📝 Description
An intelligent chatbot with natural language processing capabilities that can learn from conversations and provide contextual responses.

### ✨ Features
- Natural language understanding
- Pattern matching and intent recognition
- Learning capability - teach new responses
- Fuzzy text matching for flexibility
- Context-aware conversations
- Name recognition and personalization
- Dynamic time/date responses
- Conversation statistics tracking
- Persistent knowledge base

### 🛠️ Technologies Used
- **JSON** - Knowledge base storage
- **re** - Pattern matching with regex
- **datetime** - Time/date handling
- **collections** - Data structures

### 📦 Installation
```bash
# No external packages required!
python chatbot.py
```

### 🚀 Usage
```bash
python chatbot.py
```

### 🎯 Built-in Intents
- Greetings & farewells
- Name exchange
- Jokes & humor
- Time & date queries
- Help & capabilities
- Thanks & compliments
- Weather (simulated)
- And more!

### 💬 Special Commands
- `learn` - Enter teaching mode
- `stats` - View conversation analytics
- `quit/exit` - End conversation

### 📊 Example Interaction
```
Bot: Hello! I'm a learning chatbot. What's your name?
You: Hi, my name is John

Bot: Nice to meet you, John!
You: Tell me a joke

Bot: Why don't programmers like nature? It has too many bugs! 🐛
You: learn

--- TEACHING MODE ---
What should I respond to? what's your favorite color
What should I say? I love all colors equally!
✓ Thanks! I've learned something new!
```

### 📁 Files Created
- `chatbot_knowledge.json` - Knowledge base with learned responses

### 🎓 Learning Outcomes
- Natural Language Processing basics
- Pattern matching algorithms
- Text similarity calculation
- Context management
- Conversation flow design
- Dynamic response generation
- JSON data persistence

---

## 🔧 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Clone the Repository
```bash
git clone https://github.com/RAHUL8489XX/Python-Projects.git
cd Python-Projects
```

### Install Dependencies
```bash
# For all projects
pip install -r requirements.txt

# Or individually
pip install requests beautifulsoup4 pandas matplotlib  # Project 1
pip install matplotlib                                  # Project 2
pip install cryptography                                # Project 3
# No dependencies for Project 4
```

### Create requirements.txt
```
requests==2.31.0
beautifulsoup4==4.12.2
pandas==2.0.3
matplotlib==3.7.2
cryptography==41.0.3
```

---

## 📂 Project Structure
```
python-projects/
│
├── project1_web_scraper/
│   ├── web_scraper.py
│   └── README.md
│
├── project2_finance_tracker/
│   ├── finance_tracker.py
│   └── README.md
│
├── project3_password_manager/
│   ├── password_manager.py
│   └── README.md
│
├── project4_chatbot/
│   ├── chatbot.py
│   └── README.md
│
├── requirements.txt
└── README.md
```

---

## 🎯 Skills Demonstrated

### Programming Concepts
- Object-Oriented Programming (OOP)
- Error handling and exception management
- File I/O operations
- Data structures and algorithms
- Pattern matching and regex

### Libraries & Frameworks
- Web scraping (BeautifulSoup)
- Data analysis (Pandas)
- Visualization (Matplotlib)
- Database management (SQLite)
- Cryptography (Fernet encryption)

### Software Development
- Clean code principles
- Modular design
- User input validation
- Security best practices
- Documentation

---

## 🚀 Future Enhancements

### Web Scraper
- [ ] Add support for JavaScript-rendered websites
- [ ] Implement concurrent scraping
- [ ] Add more data sources

### Finance Tracker
- [ ] Add budget planning features
- [ ] Implement recurring transactions
- [ ] Create web interface

### Password Manager
- [ ] Add two-factor authentication
- [ ] Implement password strength checker
- [ ] Add browser extension support

### Chatbot
- [ ] Integrate machine learning models
- [ ] Add voice recognition
- [ ] Implement sentiment analysis

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Rahul Yogi**
- GitHub: [@RAHUL8489XX](https://github.com/RAHUL8489XX)
- LinkedIn: [Rahul Yogi](https://www.linkedin.com/in/rahul-yogi-264812270/)
- Email: rahulyogi1106@gmail.com

---

## 🙏 Acknowledgments

- Thanks to [quotes.toscrape.com](http://quotes.toscrape.com) for providing a scraping practice website
- Inspired by real-world applications and learning projects
- Built as part of intermediate Python learning journey

---

## 📝 Notes

- These projects are for educational purposes
- Always respect websites' robots.txt when scraping
- Keep your encryption keys and master passwords secure
- Regular backups are recommended for all data

---

**⭐ If you found these projects helpful, please consider giving them a star!**
