from website import create_app
from database import setup_database
from insert_data import insert_all_data
import os



def main():
    # Set up the database (create tables, etc.)
    setup_database()

    # Insert data into tables
    insert_all_data()
    
    # Create website
    app = create_app()
    app.run(debug=True)
    
if __name__ == '__main__':
    main()