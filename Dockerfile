FROM python:3.7

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY data/ data/

COPY out/ out/

COPY src/ src/

ENV POSTGRES_DBNAME="postgres"
ENV POSTGRES_USER="postgres"

ENV POSTGRES_HOST="postgres"
ENV POSTGRES_PORT="5432"
ENV POSTGRES_PASSWORD="Bigarelli251162"

# ENV POSTGRES_HOST="postgres2.datadriva.com"
# ENV POSTGRES_PORT="5433"
# ENV POSTGRES_PASSWORD="\$h[6;:sqyA4%f6nL[g"

ENV POSTGRES_SCHEMA="cdp"

ENV FTP_HOST="201.55.119.243"
ENV FTP_USER="Driva"
ENV FTP_PASSWORD="@123driva#"

ENV SHEET_CLIENTS="clients"
ENV SHEET_POTENTIALS="potentials"

CMD [ "uvicorn", "src.api:app", "--reload", "--host", "0.0.0.0" ]
