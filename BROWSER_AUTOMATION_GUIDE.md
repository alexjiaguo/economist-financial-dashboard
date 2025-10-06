# Browser Automation Guide

This guide covers everything you need to know about browser automation, from basic concepts to advanced techniques.

## Table of Contents
1. [What is Browser Automation?](#what-is-browser-automation)
2. [Popular Tools Comparison](#popular-tools-comparison)
3. [Getting Started](#getting-started)
4. [Common Use Cases](#common-use-cases)
5. [Best Practices](#best-practices)
6. [Troubleshooting](#troubleshooting)

## What is Browser Automation?

Browser automation is the process of programmatically controlling web browsers to perform tasks that would normally require human interaction. This includes:

- **Web Scraping**: Extracting data from websites
- **Form Automation**: Filling and submitting forms
- **UI Testing**: Testing web applications
- **Data Entry**: Automating repetitive data entry tasks
- **Monitoring**: Checking websites for changes
- **E-commerce**: Automating purchases or price monitoring

## Popular Tools Comparison

| Tool | Language | Browser Support | Learning Curve | Best For |
|------|----------|----------------|----------------|----------|
| **Playwright** | Python, JS, C#, Java | Chromium, Firefox, Safari | Easy | Modern web apps, cross-browser testing |
| **Selenium** | Python, Java, C#, JS, Ruby | All major browsers | Medium | Enterprise, legacy systems |
| **Puppeteer** | JavaScript/Node.js | Chrome/Chromium only | Easy | Chrome-specific tasks, PDF generation |
| **Beautiful Soup** | Python | N/A (HTML parsing only) | Easy | Static HTML parsing |

## Getting Started

### 1. Setup Environment

Run the setup script to install all dependencies:

```bash
./setup_browser_automation.sh
```

### 2. Basic Playwright Example

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # Set to True for headless mode
    page = browser.new_page()
    page.goto("https://example.com")
    
    # Interact with elements
    page.fill("input[name='search']", "automation")
    page.click("button[type='submit']")
    
    browser.close()
```

### 3. Running the Example Script

```bash
python3 browser_automation_example.py
```

## Common Use Cases

### 1. Web Scraping
Extract data from websites for analysis or monitoring.

```python
# Extract product prices
page.goto("https://example-store.com/products")
prices = page.query_selector_all(".price")
for price in prices:
    print(price.inner_text())
```

### 2. Form Automation
Automate form filling and submission.

```python
# Fill out a contact form
page.fill("input[name='name']", "John Doe")
page.fill("input[name='email']", "john@example.com")
page.select_option("select[name='country']", "US")
page.click("button[type='submit']")
```

### 3. E-commerce Automation
Monitor prices or automate purchases.

```python
# Check product availability
page.goto("https://store.com/product/123")
stock_status = page.query_selector(".stock-status").inner_text()
if "in stock" in stock_status.lower():
    print("Product is available!")
```

### 4. Social Media Automation
Post content or monitor social media.

```python
# Post to social media (be careful with rate limits!)
page.goto("https://twitter.com/compose/tweet")
page.fill("div[data-testid='tweetTextarea_0']", "Hello from automation!")
page.click("div[data-testid='tweetButtonInline']")
```

## Best Practices

### 1. Respect Websites
- **Rate Limiting**: Add delays between requests
- **Robots.txt**: Check and respect robots.txt files
- **Terms of Service**: Always review website ToS
- **User-Agent**: Use realistic user agents

```python
# Add delays
page.wait_for_timeout(2000)  # Wait 2 seconds

# Set realistic user agent
page.set_extra_http_headers({
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
})
```

### 2. Error Handling
Always handle errors gracefully.

```python
try:
    page.goto("https://example.com")
    page.click("button")
except Exception as e:
    print(f"Error occurred: {e}")
    # Take screenshot for debugging
    page.screenshot(path="error_screenshot.png")
```

### 3. Wait for Elements
Don't assume elements are immediately available.

```python
# Wait for element to be visible
page.wait_for_selector("button", state="visible")

# Wait for specific text
page.wait_for_selector("text=Success!")

# Wait for network to be idle
page.wait_for_load_state("networkidle")
```

### 4. Use Headless Mode for Production
```python
# For development (see browser)
browser = p.chromium.launch(headless=False)

# For production (faster, no GUI)
browser = p.chromium.launch(headless=True)
```

### 5. Handle Dynamic Content
```python
# Wait for JavaScript to load
page.wait_for_selector(".dynamic-content")

# Wait for specific condition
page.wait_for_function("() => document.querySelector('.loading').style.display === 'none'")
```

## Advanced Techniques

### 1. Handling Authentication
```python
# Login and save session
page.goto("https://example.com/login")
page.fill("input[name='username']", "your_username")
page.fill("input[name='password']", "your_password")
page.click("button[type='submit']")

# Save cookies for future use
cookies = page.context.cookies()
with open("cookies.json", "w") as f:
    json.dump(cookies, f)
```

### 2. Working with Multiple Tabs
```python
# Open new tab
new_page = browser.new_page()
new_page.goto("https://example2.com")

# Switch between tabs
page.bring_to_front()
```

### 3. File Downloads
```python
# Handle file downloads
with page.expect_download() as download_info:
    page.click("a[href*='download']")
download = download_info.value
download.save_as("downloaded_file.pdf")
```

### 4. Screenshots and Videos
```python
# Take screenshot
page.screenshot(path="screenshot.png")

# Take full page screenshot
page.screenshot(path="full_page.png", full_page=True)

# Record video (Playwright only)
browser = p.chromium.launch(headless=False)
context = browser.new_context(record_video_dir="videos/")
page = context.new_page()
# ... do automation ...
context.close()
```

## Troubleshooting

### Common Issues

1. **Element not found**
   - Use `page.wait_for_selector()` before interacting
   - Check if element is in iframe
   - Verify selector is correct

2. **Slow performance**
   - Use headless mode
   - Disable images: `page.route("**/*.{png,jpg,jpeg}", lambda route: route.abort())`
   - Use `wait_for_load_state("networkidle")`

3. **Anti-bot detection**
   - Use realistic user agents
   - Add random delays
   - Consider using residential proxies

4. **JavaScript errors**
   - Check browser console: `page.on("console", lambda msg: print(msg.text))`
   - Wait for JavaScript to load completely

### Debugging Tips

```python
# Enable debug mode
browser = p.chromium.launch(headless=False, slow_mo=1000)  # Slow down actions

# Log all network requests
page.on("request", lambda request: print(f"Request: {request.url}"))
page.on("response", lambda response: print(f"Response: {response.status}"))

# Take screenshot on error
try:
    page.click("button")
except:
    page.screenshot(path="debug.png")
    raise
```

## Legal and Ethical Considerations

- **Always respect robots.txt**
- **Don't overload servers** with too many requests
- **Respect rate limits** and terms of service
- **Use for legitimate purposes** only
- **Consider the website's resources** and bandwidth
- **Be transparent** about automated access when required

## Resources

- [Playwright Documentation](https://playwright.dev/python/)
- [Selenium Documentation](https://selenium-python.readthedocs.io/)
- [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Web Scraping Best Practices](https://blog.apify.com/web-scraping-best-practices/)

## Example Projects

1. **Price Monitor**: Monitor product prices across multiple sites
2. **Social Media Bot**: Automate social media posting (with rate limits)
3. **Form Filler**: Automate repetitive form submissions
4. **Data Collector**: Gather data from multiple sources
5. **Test Automation**: Automate UI testing for web applications

Remember: Always use browser automation responsibly and in accordance with website terms of service and applicable laws.
