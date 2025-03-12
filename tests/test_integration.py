name: Selenium Integration Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install Dependencies
        run: |
          pip install selenium pytest pytest-xdist
          pip install -r requirements.txt || true

      - name: Setup Chrome and ChromeDriver
        run: |
          sudo apt-get update
          sudo apt-get install -y google-chrome-stable
          CHROME_VERSION=$(google-chrome --version | awk '{print $3}')
          CHROMEDRIVER_VERSION=$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION)
          wget -N https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip
          unzip chromedriver_linux64.zip
          sudo mv chromedriver /usr/local/bin/
          sudo chmod +x /usr/local/bin/chromedriver

      - name: Run Selenium Tests
        run: pytest tests/ -n 5
