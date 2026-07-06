To use environment variables set on your host machine within your Docker Compose services, you can use **Variable Interpolation**. Docker Comose looks for a `.env` file in the same directory as your `docker-compose.yml` or uses the variables currently exported in your shell.

Here are the three main ways to do this:

### 1. The `.env` File (Recommended)
Create a file named `.env` in the same folder as your `docker-compose.yml`. Docker Compose automatically loads this file.

**`.env` file:**
```env
LOCUST_HOST=http://staging.example.com
NUM_USERS=50
SPAWN_RATE=5
API_KEY=my-secret-key-123
```

**`docker-compose.yml`:**
```yaml
version: '3'
services:
  master:
    image: locustio/locust
    environment:
      - LOCUST_HOST=${LOCUST_HOST}
      - API_KEY=${API_KEY}
    command: -f /mnt/locust/locustfile.py --master -H ${LOCUST_HOST}
```

### 2. Exporting Variables in the Shell
If you don't want a `.env` file, you can export the variables in your terminal before running Docker Compose.

**Terminal:**
```bash
export LOCUST_HOST=http://production.example.com
export NUM_USERS=100
docker compose up
```

Docker Compose will automatically pick up these exported variables and substitute them into your YAML file using the `${VARIABLE_NAME}` syntax.

### 3. Passing Variables Explicitly (`--env-file`)
If your variables are in a file with a different name (e.g., `config.env`), you can specify it when running the command.

**Terminal:**
```bash
docker compose --env-file config.env up
```

---

### How to Access These Inside Your Locust Python Code

Once Docker Compose passes these variables to the container, they become standard OS environment variables. You access them in Python using the `os` module.

**`locustfile.py`:**
```python
import os
from locust import HttpUser, task, between

class MyUser(HttpUser):
    # Get variables with defaults if they aren't set
    host = os.getenv("LOCUST_HOST", "http://localhost:8089")
    api_key = os.getenv("API_KEY")
    
    def on_start(self):
        print(f"Testing against: {self.host}")
        print(f"Using API Key: {self.api_key}")

    @task
    def my_task(self):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        self.client.get("/protected-data", headers=headers)
```

### Important Distinction: Interpolation vs. `environment`

| Syntax | Usage | Example |
| :--- | :--- | :--- |
| `${VAR}` | **Interpolation**: Replaces text in the YAML itself (used in `command`, `image`, `ports`). | `command: -H ${LOCUST_HOST}` |
| `VAR: value` | **Injection**: Passes the variable into the container's OS environment. | `environment: - API_KEY=${API_KEY}` |

### Best Practice for Secrets
If you are using sensitive data like passwords or API keys, avoid putting them directly in the `docker-compose.yml` or printing them in your logs. 

1. Keep them in a `.env` file.
2. Add `.env` to your `.gitignore` so it's never committed to version control.
3. Use `os.getenv()` in Python to retrieve them securely at runtime.