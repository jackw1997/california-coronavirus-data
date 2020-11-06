FROM python:3

# Create the environment:
COPY requirements.txt .
RUN pip3 install -r requirements.txt
ADD visualization.py /
ADD cdph-race-ethnicity.csv /
ADD latimes-state-totals.csv /
CMD ["bokeh", "serve", "--show", "visualization.py"]
