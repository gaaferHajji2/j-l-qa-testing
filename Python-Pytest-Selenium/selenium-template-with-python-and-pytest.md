Here’s a **complete, production-ready Selenium + Python + Pytest framework template** that senior QA engineers actually use. It follows the layered architecture I showed earlier and is ready to scale.

---

# 🏗️ Project Structure (Final Form)

```
selenium_pytest_framework/
│
├── config/
│   ├── config.yaml
│   └── environments/
│       ├── dev.yaml
│       ├── staging.yaml
│       └── prod.yaml
│
├── src/
│   ├── core/
│   │   ├── driver_factory.py
│   │   ├── base_page.py
│   │   ├── base_test.py
│   │   ├── config_reader.py
│   │   └── logger.py
│
│   ├── pages/
│   │   ├── login_page.py
│   │   └── dashboard_page.py
│
│   ├── flows/
│   │   └── login_flow.py
│
│   ├── utils/
│   │   ├── wait_utils.py
│   │   └── data_generator.py
│
│   ├── api/
│   │   └── api_client.py
│
├── tests/
│   └── ui/
│       └── test_login.py
│
├── conftest.py
├── pytest.ini
├── requirements.txt
└── README.md
```

---

# ⚙️ 1. requirements.txt

```txt
selenium
pytest
pytest-xdist
pyyaml
webdriver-manager
allure-pytest
requests
```

---

# ⚙️ 2. Driver Factory (`core/driver_factory.py`)

```python
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def get_driver(browser="chrome"):
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        return webdriver.Chrome(ChromeDriverManager().install(), options=options)
    
    raise Exception(f"Browser {browser} not supported")
```

---

# ⚙️ 3. Base Test (`core/base_test.py`)

```python
import pytest
from src.core.driver_factory import get_driver

class BaseTest:

    @pytest.fixture(autouse=True)
    def setup(self, request):
        self.driver = get_driver()
        request.cls.driver = self.driver
        yield
        self.driver.quit()
```

---

# ⚙️ 4. Base Page (`core/base_page.py`)

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:

    def __init__(self, driver):
        self.driver = driver

    def find(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def click(self, locator):
        self.find(locator).click()

    def type(self, locator, text):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)
```

---

# 📄 5. Page Object (`pages/login_page.py`)

```python
from selenium.webdriver.common.by import By
from src.core.base_page import BasePage

class LoginPage(BasePage):

    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")
    LOGIN_BTN = (By.ID, "login")

    def open(self, url):
        self.driver.get(url)

    def login(self, username, password):
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BTN)
```

---

# 📄 6. Another Page (`pages/dashboard_page.py`)

```python
from selenium.webdriver.common.by import By
from src.core.base_page import BasePage

class DashboardPage(BasePage):

    HEADER = (By.ID, "dashboard")

    def is_loaded(self):
        return self.find(self.HEADER).is_displayed()
```

---

# 🔄 7. Flow Layer (`flows/login_flow.py`) 🚀

```python
from src.pages.login_page import LoginPage
from src.pages.dashboard_page import DashboardPage

class LoginFlow:

    def __init__(self, driver):
        self.driver = driver

    def login_as_user(self, username, password, url):
        login_page = LoginPage(self.driver)
        login_page.open(url)
        login_page.login(username, password)

        return DashboardPage(self.driver)
```

---

# 🧪 8. Test (`tests/ui/test_login.py`)

```python
import pytest
from src.core.base_test import BaseTest
from src.flows.login_flow import LoginFlow

@pytest.mark.usefixtures("setup")
class TestLogin(BaseTest):

    def test_user_can_login(self):
        flow = LoginFlow(self.driver)
        dashboard = flow.login_as_user("testuser", "password", "https://example.com")

        assert dashboard.is_loaded()
```

---

# 🔧 9. Pytest Config (`pytest.ini`)

```ini
[pytest]
addopts = -v --tb=short
testpaths = tests
python_files = test_*.py
```

---

# 🔁 10. Global Fixtures (`conftest.py`)

```python
import pytest

def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="dev")

@pytest.fixture
def env(request):
    return request.config.getoption("--env")
```

---

# ⚙️ 11. Config Example (`config/config.yaml`)

```yaml
base_url: "https://example.com"
browser: "chrome"
timeout: 10
```

---

# ⏱️ 12. Wait Utility (`utils/wait_utils.py`)

```python
from selenium.webdriver.support.ui import WebDriverWait

def wait_for(condition, driver, timeout=10):
    return WebDriverWait(driver, timeout).until(condition)
```

---

# 🎲 13. Data Generator (`utils/data_generator.py`)

```python
import random
import string

def random_email():
    return ''.join(random.choices(string.ascii_lowercase, k=8)) + "@test.com"
```

---

# 🚀 How to Run

```bash
pip install -r requirements.txt
pytest -n 4
```

👉 `-n 4` uses parallel execution via **pytest-xdist**

---

# 📊 Optional: Allure Reporting

```bash
pytest --alluredir=reports
allure serve reports
```

---

# 🧠 Why This Template Is “Senior-Level”

✔ Tests contain **zero Selenium code**
✔ Business logic lives in **flows**
✔ UI logic isolated in **pages**
✔ Reusable utilities prevent duplication
✔ Easy to plug into CI/CD (e.g., pipelines)
✔ Scales to API + UI hybrid testing

---

# 🔥 Next Upgrades You Can Add

* Parallel execution via Selenium Grid
* Dockerized test runs
* Retry logic for flaky tests
* Visual testing (screenshots comparison)
* Test tagging (smoke/regression)

---

If you want, I can next:

* Turn this into a **GitHub-ready repo (copy-paste project)**
* Add **Docker + Selenium Grid setup**
* Or upgrade this to a **Screenplay Pattern framework** 🚀