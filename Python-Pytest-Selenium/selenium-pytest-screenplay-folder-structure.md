Upgrading your framework to the **Screenplay Pattern** is a *big leap toward senior-level QA architecture*. It replaces Page Objects with a more expressive, scalable model based on **Actors, Tasks, Interactions, and Questions**.

I’ll give you a **complete upgraded framework template** (Python + Selenium + Pytest) and explain how each layer works in practice.

---

# 🧠 What Changes with Screenplay?

Instead of:

```text
Test → Page → Selenium
```

You get:

```text
Test → Actor → Tasks → Interactions → Selenium
```

👉 Tests become **business-readable stories**, not UI scripts.

---

# 🏗️ New Project Structure (Screenplay Version)

```id="x5t9zx"
selenium_screenplay_framework/
│
├── config/
│   └── config.yaml
│
├── src/
│   ├── core/
│   │   ├── driver_factory.py
│   │   └── base_test.py
│
│   ├── screenplay/
│   │   ├── actors/
│   │   │   └── actor.py
│   │   │
│   │   ├── abilities/
│   │   │   └── browse_the_web.py
│   │   │
│   │   ├── interactions/
│   │   │   ├── click.py
│   │   │   ├── enter_text.py
│   │   │   └── open_url.py
│   │   │
│   │   ├── tasks/
│   │   │   └── login.py
│   │   │
│   │   ├── questions/
│   │   │   └── dashboard.py
│   │
│   ├── locators/
│   │   └── login_locators.py
│
├── tests/
│   └── test_login.py
│
├── conftest.py
├── requirements.txt
└── pytest.ini
```

---

# 🎭 1. Actor (`actors/actor.py`)

```python id="8wy4qz"
class Actor:

    def __init__(self, name):
        self.name = name
        self.abilities = {}

    def can(self, ability):
        self.abilities[type(ability)] = ability
        return self

    def ability_to(self, ability_class):
        return self.abilities.get(ability_class)

    def attempts_to(self, *tasks):
        for task in tasks:
            task.perform_as(self)

    def asks_for(self, question):
        return question.answered_by(self)
```

👉 The **Actor is the user** (e.g., “John”, “Admin”)

---

# 🌐 2. Ability (`abilities/browse_the_web.py`)

```python id="4r4w56"
class BrowseTheWeb:

    def __init__(self, driver):
        self.driver = driver

    @staticmethod
    def using(driver):
        return BrowseTheWeb(driver)
```

👉 Gives the actor the power to use **Selenium**

---

# ⚙️ 3. Interactions (Low-Level Actions)

## click.py

```python id="d0fh1i"
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Click:

    def __init__(self, locator):
        self.locator = locator

    def perform_as(self, actor):
        driver = actor.ability_to(BrowseTheWeb).driver
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(self.locator)
        ).click()
```

---

## enter_text.py

```python id="pjhjtv"
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class EnterText:

    def __init__(self, locator, text):
        self.locator = locator
        self.text = text

    def perform_as(self, actor):
        driver = actor.ability_to(BrowseTheWeb).driver
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(self.locator)
        )
        element.clear()
        element.send_keys(self.text)
```

---

## open_url.py

```python id="36g99r"
class OpenUrl:

    def __init__(self, url):
        self.url = url

    def perform_as(self, actor):
        driver = actor.ability_to(BrowseTheWeb).driver
        driver.get(self.url)
```

---

# 🧩 4. Locators (`locators/login_locators.py`)

```python id="lrdrlk"
from selenium.webdriver.common.by import By

class LoginLocators:
    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")
    LOGIN_BTN = (By.ID, "login")
    DASHBOARD = (By.ID, "dashboard")
```

---

# 🎬 5. Task (Business Logic) (`tasks/login.py`)

```python id="c3gb1l"
from src.screenplay.interactions.enter_text import EnterText
from src.screenplay.interactions.click import Click
from src.locators.login_locators import LoginLocators

class Login:

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def perform_as(self, actor):
        actor.attempts_to(
            EnterText(LoginLocators.USERNAME, self.username),
            EnterText(LoginLocators.PASSWORD, self.password),
            Click(LoginLocators.LOGIN_BTN)
        )

    @staticmethod
    def with_credentials(username, password):
        return Login(username, password)
```

👉 Tasks = **user intentions**

---

# ❓ 6. Question (Assertions) (`questions/dashboard.py`)

```python id="slkfji"
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.locators.login_locators import LoginLocators

class DashboardVisible:

    def answered_by(self, actor):
        driver = actor.ability_to(BrowseTheWeb).driver
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(LoginLocators.DASHBOARD)
            )
            return True
        except:
            return False
```

👉 Questions = **what the user sees/validates**

---

# 🧪 7. Test (`tests/test_login.py`)

```python id="ap3d75"
import pytest
from selenium import webdriver

from src.screenplay.actors.actor import Actor
from src.screenplay.abilities.browse_the_web import BrowseTheWeb
from src.screenplay.interactions.open_url import OpenUrl
from src.screenplay.tasks.login import Login
from src.screenplay.questions.dashboard import DashboardVisible

@pytest.fixture
def actor():
    driver = webdriver.Chrome()
    user = Actor("User").can(BrowseTheWeb.using(driver))
    yield user
    driver.quit()

def test_user_can_login(actor):

    actor.attempts_to(
        OpenUrl("https://example.com"),
        Login.with_credentials("testuser", "password")
    )

    assert actor.asks_for(DashboardVisible())
```

---

# 🔥 What You Gained

## ✅ 1. Readable tests

```text
User opens site → logs in → sees dashboard
```

## ✅ 2. High reusability

* Interactions reused everywhere
* Tasks reused across flows

## ✅ 3. Scalability

Works great for:

* Large teams
* Complex systems
* Microservices UI

---

# ⚠️ Common Mistakes in Screenplay

* Putting locators inside tasks ❌
* Skipping Questions layer ❌
* Making Tasks too small (duplicate interactions) ❌
* Mixing Page Object + Screenplay ❌

---

# 🧠 When to Use Screenplay

Use it when:

* Test suite is large (100+ tests)
* Multiple testers contribute
* Flaky tests need better structure

Avoid it when:

* Very small project
* Quick PoC

---

# 🚀 Optional Upgrades

* Add API abilities (actor calls APIs)
* Add reporting (Allure)
* Add parallel execution via **pytest-xdist**
* Integrate with **Docker** or **Selenium Grid**

---

# 💡 Final Takeaway

Screenplay shifts your mindset:

👉 From **“testing pages”**
👉 To **“modeling user behavior”**

That’s exactly how senior QA engineers design automation systems.

---

If you want next, I can:

* Convert this into a **ready-to-clone GitHub repo**
* Add **API + UI hybrid Screenplay**
* Or show **real-world enterprise examples (banking/e-commerce)**