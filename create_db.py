#!/usr/bin/python3
import sqlite3

# create database 
def create_database():
    connection = sqlite3.connect('events.db')
    cursor = connection.cursor()
    #create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS processed_events (
            event_id TEXT PRIMARY KEY,
            event_name TEXT,
            ticket_range TEXT,
            date TEXT,
            image_urls TEXT,
            event_url TEXT,
            genre_name TEXT
            
        )
    ''')
    
    connection.commit()
    connection.close()

if __name__ == '__main__':
    create_database()

