Yes — you **can** use Selenium with Python Locust for performance testing, but it should be used carefully and only for specific scenarios.

Locust is normally used for **protocol-level load testing**, especially HTTP requests. Selenium drives a **real browser**, so each virtual user becomes much heavier. That means you cannot simulate thousands of users easily on a single machine.

## Short answer

**Yes, Selenium can be integrated with Locust**, but it is usually better suited for:

- Small-scale browser-level performance tests
- Testing real user browser flows
- Measuring page load or UI interaction timings
- Validating performance of JavaScript-heavy applications
- Checking whether a small number of concurrent browser users experiences slowdowns

It is usually **not ideal** for high-volume load testing because browsers consume a lot of CPU, memory, and OS resources.

---

## When Selenium + Locust makes sense

Use Selenium with Locust when you need to test behavior that only happens in a real browser, for example:

1. **JavaScript-rendered pages**
   - Single-page applications
   - React, Angular, Vue apps
   - Pages that load data dynamically after rendering

2. **User flows involving browser interaction**
   - Login
   - Search
   - Add to cart
   - Checkout
   - Form submission
   - File upload
   - UI navigation

3. **Front-end performance measurement**
   - Page load time
   - Element visibility time
   - Time until a button becomes clickable
   - Time until data appears in the DOM

4. **Browser-specific behavior**
   - Cookies
   - Local storage
   - Session storage
   - Redirects
   - JavaScript execution
   - WebSockets triggered from the UI

---

## When Selenium + Locust is not a good fit

Avoid using Selenium for large-scale performance testing if your goal is to simulate many users, such as:

- 500 users
- 1,000 users
- 10,000 users
- API-level throughput testing
- Backend capacity testing
- Database load testing
- Microservice stress testing

For those cases, prefer Locust’s normal `HttpUser`, or another API-level load testing approach.

A real browser can easily consume hundreds of MBs of RAM and significant CPU. Running hundreds of Selenium browser instances is expensive and often unstable.

---

## Basic example: Selenium with Locust

Here is a simple example showing how to combine Selenium with Locust.

```python
import time
from locust import User, task, between, events
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SeleniumUser(User):
    wait_time = between(1, 3)

    def on_start(self):
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)

    def on_stop(self):
        if hasattr(self, "driver"):
            self.driver.quit()

    @task
    def visit_homepage(self):
        start_time = time.time()

        try:
            self.driver.get("https://example.com/")

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))
            )

            total_time = int((time.time() - start_time) * 1000)

            events.request.fire(
                request_type="SELENIUM",
                name="Homepage load",
                response_time=total_time,
                response_length=0,
                exception=None,
            )

        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)

            events.request.fire(
                request_type="SELENIUM",
                name="Homepage load",
                response_time=total_time,
                response_length=0,
                exception=e,
            )

    @task
    def click_more_information(self):
        start_time = time.time()

        try:
            self.driver.get("https://example.com/")

            link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "More information..."))
            )
            link.click()

            WebDriverWait(self.driver, 10).until(
                EC.url_contains("iana.org")
            )

            total_time = int((time.time() - start_time) * 1000)

            events.request.fire(
                request_type="SELENIUM",
                name="Click More Information",
                response_time=total_time,
                response_length=0,
                exception=None,
            )

        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)

            events.request.fire(
                request_type="SELENIUM",
                name="Click More Information",
                response_time=total_time,
                response_length=0,
                exception=e,
            )
```

Run it with:

```bash
locust -f locust_selenium_example.py
```

Then open:

```text
http://localhost:8089
```

---

## Better example: reusable Selenium Locust user

A cleaner approach is to create a base class for Selenium users.

```python
import time
from locust import User, events
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class BaseSeleniumUser(User):
    abstract = True

    def on_start(self):
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")

        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)

    def on_stop(self):
        if hasattr(self, "driver"):
            self.driver.quit()

    def measure(self, request_name, func):
        start_time = time.time()

        try:
            result = func()
            total_time = int((time.time() - start_time) * 1000)

            events.request.fire(
                request_type="SELENIUM",
                name=request_name,
                response_time=total_time,
                response_length=0,
                exception=None,
            )

            return result

        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)

            events.request.fire(
                request_type="SELENIUM",
                name=request_name,
                response_time=total_time,
                response_length=0,
                exception=e,
            )

            raise
```

Then use it like this:

```python
from locust import task, between
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebUser(BaseSeleniumUser):
    wait_time = between(2, 5)

    @task
    def load_homepage(self):
        def action():
            self.driver.get("https://example.com/")
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))
            )

        self.measure("Homepage load", action)
```

---

## Important: reporting Selenium actions to Locust

Locust normally tracks HTTP requests automatically. Selenium actions are not automatically reported, so you need to manually fire Locust’s request event.

Example:

```python
events.request.fire(
    request_type="SELENIUM",
    name="Login page load",
    response_time=total_time,
    response_length=0,
    exception=None,
)
```

This makes the Selenium action appear in Locust’s statistics dashboard.

If an exception occurs, pass it like this:

```python
events.request.fire(
    request_type="SELENIUM",
    name="Login page load",
    response_time=total_time,
    response_length=0,
    exception=e,
)
```

---

## Recommended browser settings for load testing

When using Selenium for performance testing, use headless mode and disable unnecessary browser features.

Example Chrome options:

```python
options = Options()

options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")
options.add_argument("--disable-images")
options.add_argument("--disable-javascript")
options.add_argument("--blink-settings=imagesEnabled=false")
options.add_argument("--window-size=1920,1080")
```

Be careful with `--disable-javascript`. If you are testing a JavaScript-heavy application, disabling JavaScript may make the test unrealistic.

---

## Main limitations of Selenium + Locust

### 1. High resource usage

Each browser instance consumes significant memory and CPU.

Approximate practical expectation:

| Virtual browser users | Feasibility |
|---:|---|
| 1 to 10 | Usually fine |
| 10 to 50 | Possible on a strong machine |
| 50 to 100 | Requires careful tuning and strong infrastructure |
| 100+ | Difficult and usually not recommended with Selenium |

The exact number depends on the application, page complexity, machine size, browser, and test scenario.

---

### 2. Lower throughput

Selenium is slower than raw HTTP requests because it includes:

- Browser startup
- Rendering
- JavaScript execution
- DOM interaction
- Network handling
- Painting
- Event handling

This may be good for realism, but bad for scalability.

---

### 3. Flaky tests

UI tests can fail due to:

- Timing issues
- Animations
- Dynamic element locators
- Slow JavaScript
- Network instability
- Browser driver issues
- Modal popups
- Cookie banners
- Authentication redirects

Use explicit waits instead of fixed sleeps.

Prefer:

```python
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "submit"))
)
```

Avoid this where possible:

```python
time.sleep(5)
```

---

### 4. Harder to run in distributed mode

Locust supports distributed load testing, but Selenium browser instances are heavier and more complicated to manage across workers.

If using distributed Locust, make sure each worker machine has:

- Browser installed
- WebDriver installed
- Enough CPU and memory
- Correct environment configuration

---

## Better alternatives depending on your goal

### If you want to test APIs

Use normal Locust:

```python
from locust import HttpUser, task, between


class ApiUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def get_items(self):
        self.client.get("/api/items")
```

This is much more scalable than Selenium.

---

### If you need browser-level load testing

Consider:

- Locust + Selenium, with low user count
- Locust + Playwright
- k6 Browser
- JMeter WebDriver Sampler
- Gatling with browser-based testing, if applicable

Playwright is often more modern and faster for browser automation than Selenium, though it still has browser-level overhead.

---

### If you need front-end performance diagnostics

Use tools such as:

- Lighthouse CI
- WebPageTest
- Playwright tracing
- Chrome DevTools
- Real User Monitoring, such as Datadog RUM, New Relic Browser, Dynatrace, or similar

These tools are often better for detailed page-speed metrics.

---

## Recommended approach

A good performance testing strategy is usually layered:

### 1. API load testing with Locust

Use Locust `HttpUser` for high-volume load testing of backend endpoints.

Example:

```python
from locust import HttpUser, task


class ApiUser(HttpUser):
    @task
    def load_products(self):
        self.client.get("/api/products")
```

This simulates many users efficiently.

---

### 2. Browser smoke performance testing with Selenium

Use Selenium with Locust for a small number of users to verify real browser behavior.

Example:

- 5 browser users
- 10 browser users
- 20 browser users, if infrastructure supports it

This helps identify front-end rendering or JavaScript issues.

---

### 3. Front-end profiling separately

Use Lighthouse, WebPageTest, or browser developer tools to analyze page performance in detail.

---

## Practical recommendation

If your question is:

> Can we use Selenium with Locust?

**Yes.**

If your question is:

> Should we use Selenium with Locust for full performance/load testing?

**Usually no, not for high load.**

Use Selenium with Locust only when you specifically need browser-level testing. For most performance tests, use Locust’s HTTP user or another API-level tool.

---

## Example test design

A balanced performance test could look like this:

```text
Backend API load test:
- Locust HttpUser
- 500 to 2,000 virtual users
- Tests login, search, checkout APIs

Browser performance test:
- Locust SeleniumUser
- 5 to 20 virtual users
- Tests login, search, checkout through real browser

Front-end diagnostics:
- Lighthouse CI
- WebPageTest
- Chrome DevTools
```

This gives you both scalability and browser realism.

---

## Final answer

Yes, you can use Selenium with Python Locust for performance testing by creating a custom Locust `User` class that controls a WebDriver and reports action timings to Locust. However, because Selenium launches real browsers, it is resource-heavy and not suitable for simulating large numbers of users. Use it for small-scale browser-level performance testing, and use normal Locust HTTP users or API-level tests for high-volume load testing.