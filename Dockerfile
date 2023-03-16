FROM python:3.9

WORKDIR /app

COPY requirements.txt ./requirements.txt
COPY main.py ./main.py
COPY get_data.py ./get_data.py
COPY service.py ./service.py

RUN pip install -r requirements.txt

EXPOSE 8501

CMD streamlit run main.py  


