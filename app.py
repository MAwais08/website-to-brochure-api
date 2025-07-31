import json
from typing import List
import os
import requests
from bs4 import BeautifulSoup
import openai
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import markdown

# Load environment variables
load_dotenv(override=True)
api_key = os.getenv("OPENAI_API_KEY")
MODEL = 'gpt-4o-mini'

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

class Website:
    def __init__(self, url):
        self.url = url
        response = requests.get(url, headers=headers)
        self.body = response.content
        soup = BeautifulSoup(self.body, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"
        if soup.body:
            for irrelevant in soup.body(["script", "img", "style", "input"]):
                irrelevant.decompose()
            self.body = soup.body.get_text(separator="\n", strip=True)
        else:
            self.body = ""

        links = soup.find_all('a')
        self.links = [link.get('href') for link in links]
        self.links = [link for link in self.links if link]

    def get_contents(self):
        return f"Website Title \n{self.title}\n\nWebsite Body\n{self.body} \n \n"

link_system_prompt = "You are provided with a list of links found on a webpage. \
You are able to decide which of the links would be most relevant to include in a brochure about the company, \
such as links to an About page, or a Company page, or Careers/Jobs pages.\n"
link_system_prompt += "You should respond in JSON as in this example:"
link_system_prompt += """
{
    "links": [
        {"type": "about page", "url": "https://full.url/goes/here/about"},
        {"type": "careers page": "url": "https://another.full.url/careers"}
    ]
}
"""

def get_links_user_prompt(website):
    user_prompt = f"Here is the list of links on the website of {website.url} - "
    user_prompt += "please decide which of these are relevant web links for a brochure about the company, respond with the full https URL in JSON format. \
    Do not include Terms of Service, Privacy, email links.\n"
    user_prompt += "Links (some might be relative links):\n"
    user_prompt += "\n".join(website.links)
    return user_prompt

def get_links(url):
    website = Website(url)
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": link_system_prompt},
            {"role": "user", "content": get_links_user_prompt(website)}
        ],
        response_format={"type": "json_object"},
    )
    result = response.choices[0].message.content
    return json.loads(result)

def get_all_contents(url):
    result = "Landing Page :\n"
    result += Website(url).get_contents()
    links = get_links(url)

    for link in links["links"]:
        result += Website(link["url"]).get_contents()
    return result

system_prompt = "You are an assistant that analyzes the contents of several relevant pages from a company website \
and creates a short brochure about the company for prospective customers, investors and recruits. Respond in markdown.\
Include details of company culture, customers and careers/jobs if you have the information."

def get_brochure_user_prompt(company_name, url):
    user_prompt = f"You are looking at a company called: {company_name}\n"
    user_prompt += f"Here are the contents of its landing page and other relevant pages; use this information to build a short brochure of the company in markdown.\n"
    user_prompt += get_all_contents(url)
    user_prompt = user_prompt[:5_000]  # Truncate if more than 5,000 characters
    return user_prompt

def create_brochure(company_name, url):
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": get_brochure_user_prompt(company_name, url)}
        ],
    )
    result = response.choices[0].message.content
    return result

# Flask Routes (API only - no HTML templates needed)
@app.route('/generate_brochure', methods=['POST'])
def generate_brochure():
    try:
        data = request.get_json()
        company_name = data.get('company_name', '').strip()
        url = data.get('url', '').strip()
        
        if not company_name or not url:
            return jsonify({'error': 'Company name and URL are required'}), 400
        
        # Generate brochure using your existing logic
        brochure_markdown = create_brochure(company_name, url)
        
        # Convert markdown to HTML for display
        brochure_html = markdown.markdown(brochure_markdown)
        
        return jsonify({
            'success': True,
            'brochure_markdown': brochure_markdown,
            'brochure_html': brochure_html
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)