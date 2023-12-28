from flask import Flask, render_template
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pymysql

app = Flask(__name__)

def get_expense_data():
 
    connection = pymysql.connect(
        host='34.101.238.77',
        user='root',
        password='123456',
        database='final-cloud-run'
    )

    cursor = connection.cursor()

    query = "SELECT category, amount, date FROM transaction"
    cursor.execute(query)

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return data

def create_pie_chart(data):
    categories = {}
    total_expense = 0

    for row in data:
        category, amount, _ = row
        total_expense += amount
        categories[category] = categories.get(category, 0) + amount

    labels = list(categories.keys())
    values = [(amount / total_expense) * 100 for amount in categories.values()]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_layout(title='Expense Percentage per Category')
    return fig

def create_line_chart(data):
    dates = {}
    for row in data:
        _, amount, date = row
        day = date.day
        dates[day] = dates.get(day, 0) + amount

    days = list(dates.keys())
    amounts = list(dates.values())

    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(go.Scatter(x=days, y=amounts, mode='lines+markers', name='Expense per Day'))
    fig.update_layout(title='Expense per Day in the Last Month', xaxis_title='Day', yaxis_title='Expense')
    return fig

@app.route('/visualization')
def index():
    expense_data = get_expense_data()

    pie_chart = create_pie_chart(expense_data)
    line_chart = create_line_chart(expense_data)

    return render_template('index.html', pie_chart=pie_chart, line_chart=line_chart)

if __name__ == '__main__':
    app.run(debug=True)