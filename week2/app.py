# %%
import os
import requests
import json
from typing import List
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display, update_display
import gradio as gr 
import google.generativeai as genai 
import ollama

# %%
load_dotenv()
google_api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=google_api_key)

# %%
import requests
from bs4 import BeautifulSoup
from typing import List, Optional
from urllib.parse import urljoin, urlparse

class Website:
    """
    A utility class to represent and scrape website content with robust error handling.
    """

    def __init__(self, url: str, timeout: int = 10):
        """
        Initialize the Website object by fetching and parsing webpage content.

        Args:
            url (str): The URL of the webpage to scrape
            timeout (int, optional): Request timeout in seconds. Defaults to 10.
        """
        self.url = url
        self.title = "No title found"
        self.text = ""
        self.links = []
        self.relevant_links = []

        try:
            response = self._fetch_webpage(url, timeout)
            if response:
                self._parse_webpage(response)
        except Exception as e:
            print(f"Error processing {url}: {e}")

    def _fetch_webpage(self, url: str, timeout: int) -> Optional[requests.Response]:
        """
        Fetch webpage content with error handling and validation.

        Args:
            url (str): URL to fetch
            timeout (int): Request timeout in seconds

        Returns:
            Optional[requests.Response]: Response object or None
        """
        try:
            # Validate URL
            parsed_url = urlparse(url)
            if not all([parsed_url.scheme, parsed_url.netloc]):
                print(f"Invalid URL: {url}")
                return None

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            return response
        except (requests.RequestException, ValueError) as e:
            print(f"Request failed for {url}: {e}")
            return None

    def _parse_webpage(self, response: requests.Response):
        """
        Parse webpage content using BeautifulSoup.

        Args:
            response (requests.Response): Webpage response
        """
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title
        self.title = soup.title.string if soup.title else "No title found"

        if soup.body:
            for irrelevant in soup.body(["script", "style", "img", "input"]):
                irrelevant.decompose()
            self.text = soup.body.get_text(separator="\n", strip=True)

        links = [urljoin(self.url, link.get('href')) for link in soup.find_all('a') if link.get('href')]
        self.links = list(set(links))  # Remove duplicates
        self.relevant_links = self._filter_relevant_links(self.links)

    def _filter_relevant_links(self, links: List[str]) -> List[str]:
        """
        Filter links based on relevance keywords.

        Args:
            links (List[str]): List of webpage links

        Returns:
            List[str]: Filtered list of relevant links
        """
        relevant_keywords = ["about", "careers", "contact", "company", "jobs"]
        return [link for link in links if any(keyword in link.lower() for keyword in relevant_keywords)]

    def get_contents(self) -> str:
        """
        Get formatted webpage contents.

        Returns:
            str: Formatted string with webpage title and text
        """
        return f"Webpage Title:\n{self.title}\nWebpage Contents:\n{self.text}\n\n"

    def __repr__(self) -> str:
        """
        String representation of the Website object.

        Returns:
            str: Descriptive string about the website
        """
        return f"Website(url='{self.url}', title='{self.title}', links={len(self.links)})"

# %%
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options

# class Website:
#     """
#     A utility class to represent a Website that we have scraped, now with links
#     """

#     def __init__(self, url):
#         self.url = url

#         # Set up Selenium WebDriver options
#         options = Options()
#         options.add_argument("headless")  # Run in headless mode
#         options.add_argument("--no-sandbox")
#         options.add_argument("--disable-dev-shm-usage")

#         # Initialize the WebDriver
#         service = Service("C:/Users/anura/OneDrive/Desktop/llm_engineering/chromedriver-win64/chromedriver.exe")
#         driver = webdriver.Chrome(service=service, options=options)
#         driver.get(url)

#         # Wait for user to complete any manual verification if needed
#         input("Please complete the verification in the browser and press Enter to continue...")

#         # Get the page source after JavaScript execution
#         page_source = driver.page_source
#         driver.quit()

#         # Parse the page source with BeautifulSoup
#         soup = BeautifulSoup(page_source, 'html.parser')
#         self.title = soup.title.string if soup.title else "No title found"
        
#         # Remove irrelevant tags
#         for irrelevant in soup(["script", "style", "img", "input"]):
#             irrelevant.decompose()
        
#         # Extract text content
#         self.text = soup.get_text(separator="\n", strip=True)

#         # Extract and filter links
#         links = [link.get('href') for link in soup.find_all('a')]
#         self.links = [link for link in links if link]
#         self.relevant_links = self.filter_relevant_links(self.links)

#     def filter_relevant_links(self, links: List[str]) -> List[str]:
#         relevant_keywords = ["about", "careers", "contact", "company", "jobs"]
#         return [link for link in links if any(keyword in link.lower() for keyword in relevant_keywords)]

#     def get_contents(self):
#         return f"Webpage Title:\n{self.title}\nWebpage Contents:\n{self.text}\n\n"

# %%

link_system_prompt= "Now You are an assistant that analyzes the contents of several relevant pages from a company website \
and creates a short brochure about the company for prospective customers, investors and recruits. Respond in markdown.\
Include details of company culture, customers and careers/jobs if you have the information. Include hyperlinks of social media platforms."


# %%

def stream_llama(prompt):
    messages = [
        {"role": "system", "content": link_system_prompt},
        {"role": "user", "content": prompt}
      ]
    stream = ollama.chat(
        model='llama3.2',
        messages=messages,
        stream=True
    )
    result = ""
    for chunk in stream:
        result += chunk['message']['content']
        yield result

# %%
def stream_gemma(prompt):
    messages=  [
        {"role": "system", "content": link_system_prompt},
        {"role": "user", "content": prompt}
       ]
    result = ollama.chat(
        model="gemma2",
        messages = messages,
        stream=True
    )
    response = ""
    for chunk in result:
        response+=chunk['message']['content']
        yield response
        
        

# %%
def stream_gemini(prompt):
    model=genai.GenerativeModel(model_name="gemini-1.5-pro",system_instruction=link_system_prompt)
    response=model.generate_content(prompt,stream=True)
    result=""

    for chunks in response:
        if chunks.text:
            result+=chunks.text
            yield result


    

# %%
def stream_brochure(company_name, url, model):
    prompt = f"Please generate a company brochure for {company_name}.\n"
    prompt += Website(url).get_contents()
    if model=="LLAMA3.2":
        result = stream_llama(prompt)
    elif model=="GEMMA2":
        result = stream_gemma(prompt)
    elif model=="GEMINI-1.5-PRO":
        result = stream_gemini(prompt)
    else:
        raise ValueError("Unknown model")
    yield from result

# %%


view = gr.Interface(
    fn=stream_brochure,
    inputs=[
        gr.Textbox(label="Company Name:", placeholder="Enter the company name here"),
        gr.Textbox(label="Landing Page URL:", placeholder="Enter the URL including http:// or https://"),
        gr.Dropdown(["LLAMA3.2", "GEMMA2","GEMINI-1.5-PRO"], label="Select Model")
    ],
    outputs=[gr.Markdown(label="Brochure:")],
    title="Company Brochure Generator",
    description="Generate a professional brochure for your company using AI models. Simply provide the company name, landing page URL, and select the model.",
    theme="default",
    # layout="vertical",
    flagging_mode="never"
)
view.launch()

# %%


# %%



