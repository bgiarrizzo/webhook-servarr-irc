# ------------------------------------------------------------------------------
# Stage 1 - Build

FROM python:alpine AS BUILD_IMAGE

ARG BUILD=PROD
ENV VENV=/opt/venv

WORKDIR /app/

RUN python -m venv ${VENV} 

ENV PATH="${VENV}/bin:$PATH"
ENV PYTHONPATH="${VENV}/bin:$PYTHONPATH"

RUN pip install --no-cache-dir --upgrade pip pipenv

COPY Pipfile .
COPY Pipfile.lock .

RUN if [ ${BUILD} = "DEV" ]; then pipenv requirements --dev > reqs.txt; fi
RUN if [ ${BUILD} = "PROD" ]; then pipenv requirements > reqs.txt; fi

RUN pip install --no-cache-dir -r reqs.txt

# ------------------------------------------------------------------------------
# Stage 2 - Run

FROM python:alpine AS RUN_IMAGE

ENV VENV=/opt/venv

WORKDIR /app/

EXPOSE 8000

COPY --from=BUILD_IMAGE ${VENV} ${VENV}

ENV PATH="${VENV}/bin:$PATH"
ENV PYTHONPATH="${VENV}/bin:$PYTHONPATH"
ENV PYTHONDONOTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ARG CACHEBUST=1

# Add App
COPY src/handlers/ src/handlers/
COPY src/irc/ src/irc/
COPY src/config.py src/config.py
COPY src/main.py src/main.py

# Run
CMD ["python", "src/main.py"]
