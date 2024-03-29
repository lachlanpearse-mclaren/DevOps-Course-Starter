FROM python:3 as base
WORKDIR /app
COPY ./poetry.toml /app
COPY ./pyproject.toml /app
COPY ./todo_app /app/todo_app
RUN pip install poetry

FROM base as production
COPY ./start_todo-app.sh /app
RUN poetry config virtualenvs.create false --local && poetry install && chmod a+x /app/start_todo-app.sh
ENV PORT=5000
EXPOSE 5000
ENTRYPOINT ["sh","./start_todo-app.sh"]

FROM base as test
RUN poetry install && apt-get update && apt-get install wget gnupg unzip -y
# Install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
  && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
  && apt-get update -qqy \
  && apt-get -qqy install google-chrome-stable \
  && rm /etc/apt/sources.list.d/google-chrome.list \
  && rm -rf /var/lib/apt/lists/* /var/cache/apt/*
# Install Chrome WebDriver
RUN apt-get update && apt-get install unzip -y
RUN CHROME_MAJOR_VERSION=$(google-chrome --version | sed -E "s/.* ([0-9]+)(\.[0-9]+){3}.*/\1/") \
  && CHROME_DRIVER_VERSION=$(wget --no-verbose -O - "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_MAJOR_VERSION}") \
  && echo "Using chromedriver version: "$CHROME_DRIVER_VERSION \
  && wget --no-verbose -O /tmp/chromedriver_linux64.zip https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip \
  && rm -rf /opt/selenium/chromedriver \
  && unzip /tmp/chromedriver_linux64.zip -d /opt/selenium \
  && cp /opt/selenium/chromedriver . \
  && rm /tmp/chromedriver_linux64.zip \
  && mv /opt/selenium/chromedriver /opt/selenium/chromedriver-$CHROME_DRIVER_VERSION \
  && chmod 755 /opt/selenium/chromedriver-$CHROME_DRIVER_VERSION \
  && ln -fs /opt/selenium/chromedriver-$CHROME_DRIVER_VERSION /usr/bin/chromedriver
ENV PATH=$PATH:/app
EXPOSE 4444
ENTRYPOINT  ["poetry", "run", "pytest"]
CMD [""]
