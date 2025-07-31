# 🏢 Company Brochure Generator API

**An AI-powered Flask API that scrapes company websites and generates beautiful brochures in Markdown and HTML using OpenAI GPT-4o-mini.**

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Flask](https://img.shields.io/badge/Flask-lightgrey)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-blueviolet)
![BeautifulSoup](https://img.shields.io/badge/HTML%20Scraper-BeautifulSoup-yellowgreen)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🚀 Features

- 🌐 Scrapes company website (landing + relevant pages)
- 🔍 Identifies key pages (About, Careers, etc.) using AI
- 🧠 Uses OpenAI GPT-4o-mini to summarize into a brochure
- 📄 Outputs in **Markdown** and **HTML**
- ⚡ CORS-enabled Flask backend for easy frontend integration

---

## 🛠️ Tech Stack

- **Python 3.9+**
- **Flask**
- **OpenAI API**
- **BeautifulSoup**
- **markdown (for Markdown-to-HTML conversion)**
- **dotenv**

---

## 📦 Installation & Setup

```bash
# 1. Clone the repo
git clone https://github.com/your-username/company-brochure-generator.git
cd company-brochure-generator

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your OpenAI API Key
echo "OPENAI_API_KEY=your_openai_key_here" > .env
