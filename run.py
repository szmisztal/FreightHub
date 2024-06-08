from flask import render_template
from app import create_app

# Create Flask application
app = create_app()

@app.route("/")
def home():
    """
    Renders the home page.

    This route renders the base HTML template for the home page of the application.

    Returns:
        str: Rendered HTML of the base template.
    """
    return render_template("base.html")

if __name__ == "__main__":
    """
    Runs the Flask application in debug mode if this script is executed directly.
    """
    app.run(debug=True)
