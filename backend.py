from flask import Flask, render_template, request, redirect, url_for
from time_table import TimeTable

class TimeTableApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.tb = TimeTable()

        # private variables for adding
        self.__name = None
        self.__sub_hd = None
        self.__TH = None
        self.__sub_code = None

        self.routes()

    def routes(self):
        # ---------- HOME PAGE ---------- #
        @self.app.route('/')
        def home():
            return render_template('IndexT.html')

        # ---------- BUTTON HANDLER ---------- #
        @self.app.route('/button_click', methods=['POST'])
        def button_handle():
            data = request.form.get('btn')
            if data == "display":
                return redirect(url_for('display'))
            elif data == "add":
                return redirect(url_for('add'))
            elif data == "delete":
                return redirect(url_for('delete'))
            elif data == "generate":
                return redirect(url_for('generate'))
            elif data=="reset":
                
                self.tb.reset()
            else:
                return "Invalid Choice"

        # ---------- DISPLAY ---------- #
        @self.app.route('/display')
        def display():
            return render_template(
                "display.html",
                table=self.tb.df.to_html(classes='table table-striped table-bordered', index=True)
            )

        # ---------- ADD ---------- #
        @self.app.route('/add')
        def add():
            return render_template("add.html")

        # ---------- DELETE ---------- #
        @self.app.route('/delete')
        def delete():
            return render_template("delete.html")

        # ---------- GENERATE TIMETABLE ---------- #
        @self.app.route('/generate')
        def generate():
            self.tb.time_table()  # generate timetable
            return render_template(
                "generate.html",
                timetable=self.tb.DT.to_html(classes='table table-striped table-bordered table-hover', index=False)
            )

        # ---------- ADD SUBMIT ---------- #
        @self.app.route('/add_submit', methods=['POST'])
        def add_submit():
            self.__name = request.form.get('name')
            self.__sub_hd = request.form.get('sub_hd')
            self.__TH = int(request.form.get('Total_Hour'))
            self.__sub_code = request.form.get('sub_code')

            self.tb.get_data(
                self.__name,
                self.__sub_hd,
                self.__TH,
                self.__sub_code
            )
            return redirect(url_for('display'))

        # ---------- DELETE SUBMIT ---------- #
        @self.app.route('/delete_submit', methods=['POST'])
        def delete_submit():
            index_str = request.form.get('index')
            try:
                index = int(index_str)
                self.tb.delete(index)
            except (ValueError, TypeError):
                print("Invalid index provided for deletion")
            return redirect(url_for('display'))

    def run(self):
        self.app.run(debug=True)

# ---------- MAIN ---------- #
if __name__ == "__main__":
    app = TimeTableApp()
    app.run()