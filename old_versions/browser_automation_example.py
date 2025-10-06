#!/usr/bin/env python3
"""
Browser Automation Example using Playwright
This script demonstrates common browser automation tasks.
"""

from playwright.sync_api import sync_playwright
import time
import json

def basic_navigation():
    """Basic navigation and interaction example"""
    with sync_playwright() as p:
        # Launch browser (set headless=False to see the browser)
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Navigate to a website
        page.goto("https://httpbin.org/forms/post")
        
        # Fill out a form
        page.fill("input[name='custname']", "John Doe")
        page.fill("input[name='custtel']", "555-1234")
        page.fill("input[name='custemail']", "john@example.com")
        
        # Select from dropdown
        page.select_option("select[name='size']", "large")
        
        # Check checkbox
        page.check("input[name='topping'][value='bacon']")
        
        # Submit form
        page.click("input[type='submit']")
        
        # Wait and take screenshot
        page.wait_for_timeout(2000)
        page.screenshot(path="form_submission.png")
        
        browser.close()
        print("Form submitted successfully!")

def web_scraping_example():
    """Web scraping example"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Navigate to a news site
        page.goto("https://news.ycombinator.com")
        
        # Extract headlines
        headlines = page.query_selector_all(".titleline > a")
        news_data = []
        
        for headline in headlines[:5]:  # Get first 5 headlines
            title = headline.inner_text()
            link = headline.get_attribute("href")
            news_data.append({"title": title, "link": link})
        
        # Save to JSON
        with open("hackernews_headlines.json", "w") as f:
            json.dump(news_data, f, indent=2)
        
        browser.close()
        print(f"Scraped {len(news_data)} headlines!")

def advanced_interactions():
    """Advanced interactions example"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Set viewport size
        page.set_viewport_size({"width": 1920, "height": 1080})
        
        # Navigate to Google
        page.goto("https://www.google.com")
        
        # Handle cookie consent if present
        try:
            page.click("button:has-text('Accept all')", timeout=3000)
        except:
            pass  # No cookie banner
        
        # Search for something
        page.fill("input[name='q']", "browser automation")
        page.press("input[name='q']", "Enter")
        
        # Wait for results
        page.wait_for_selector("#search")
        
        # Get search results
        results = page.query_selector_all("h3")
        print("Search results:")
        for i, result in enumerate(results[:5], 1):
            print(f"{i}. {result.inner_text()}")
        
        # Take screenshot of results
        page.screenshot(path="google_search_results.png")
        
        browser.close()

def handle_dynamic_content():
    """Handle dynamic content and wait for elements"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Navigate to a site with dynamic content
        page.goto("https://quotes.toscrape.com/js/")
        
        # Wait for quotes to load
        page.wait_for_selector(".quote")
        
        # Extract quotes
        quotes = page.query_selector_all(".quote")
        for quote in quotes[:3]:
            text = quote.query_selector(".text").inner_text()
            author = quote.query_selector(".author").inner_text()
            print(f'"{text}" - {author}')
        
        browser.close()

def file_upload_example():
    """File upload example"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Navigate to a file upload test site
        page.goto("https://the-internet.herokuapp.com/upload")
        
        # Create a test file
        with open("test_file.txt", "w") as f:
            f.write("This is a test file for upload.")
        
        # Upload file
        page.set_input_files("input[type='file']", "test_file.txt")
        page.click("input[type='submit']")
        
        # Wait for upload confirmation
        page.wait_for_selector("h3:has-text('File Uploaded!')")
        print("File uploaded successfully!")
        
        browser.close()

if __name__ == "__main__":
    print("Browser Automation Examples")
    print("=" * 30)
    
    while True:
        print("\nChoose an example to run:")
        print("1. Basic Navigation & Form Filling")
        print("2. Web Scraping")
        print("3. Advanced Interactions (Google Search)")
        print("4. Handle Dynamic Content")
        print("5. File Upload")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            basic_navigation()
        elif choice == "2":
            web_scraping_example()
        elif choice == "3":
            advanced_interactions()
        elif choice == "4":
            handle_dynamic_content()
        elif choice == "5":
            file_upload_example()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
