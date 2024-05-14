from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap5
import csv
from csv import writer
import os
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
SECRET_KEY = os.getenv("SECRET_KEY")

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    open_time = StringField('Open', validators=[DataRequired()])
    close_time = StringField('Close', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee', choices=[('☕️', "☕️"), ("☕️☕️", "☕️☕️"), ("☕️☕️☕️", "☕️☕️☕️"),
                                                   ("☕️☕️☕️☕️", "☕️☕️☕️☕️"), ("☕️☕️☕️☕️☕️", "☕️☕️☕️☕️☕️")],
                                validators=[DataRequired()])
    wifi = SelectField('Wifi', choices=[('💪', "💪"), ("💪💪", "💪💪"), ("💪💪💪", "💪💪💪"),
                                        ("💪💪💪💪", "💪💪💪💪"), ("💪💪💪💪💪", "💪💪💪💪💪"), ('✘', "✘")], validators=[DataRequired()])
    power = SelectField('Power', choices=[('🔌', "🔌"), ("🔌🔌", "🔌🔌"), ("🔌🔌🔌", "🔌🔌🔌"),
                                          ("🔌🔌🔌🔌", "🔌🔌🔌🔌"), ("🔌🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"), ('✘', "✘")], validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
        new_line = [form.cafe.data, form.location.data, form.open_time.data, form.close_time.data,
                    form.coffee_rating.data, form.wifi.data, form.power.data]
        with open('cafe-data.csv', 'a') as data:
            write_row_new = writer(data)
            write_row_new.writerow(new_line)
        return render_template("index.html")

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        list_of_rows.pop(0)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
