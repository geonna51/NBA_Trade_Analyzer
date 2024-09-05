import sqlite3
import os

db_path = '/Users/georgen/VSCode/Trade Analyzer 2/nba_players.db'
images_directory = '/Users/georgen/VSCode/Trade Analyzer 2/static/nba_headshots'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(nba_players);")
columns = [column[1] for column in cursor.fetchall()]
if 'image' not in columns:
    cursor.execute('ALTER TABLE nba_players ADD COLUMN image BLOB;')

image_files = [f for f in os.listdir(images_directory) if f.endswith('.png')]

for image_file in image_files:
    player_id = os.path.splitext(image_file)[0]
    
    image_path = os.path.join(images_directory, image_file)
    try:
        with open(image_path, 'rb') as file:
            image_blob = file.read()
        
        # First, check if the player exists
        cursor.execute('SELECT id FROM nba_players WHERE player_id = ?', (player_id,))
        result = cursor.fetchone()
        
        if result:
            # Update the database
            cursor.execute('''
                UPDATE nba_players
                SET image = ?
                WHERE player_id = ?
            ''', (image_blob, player_id))
            
            if cursor.rowcount > 0:
                print(f"Successfully updated image for player ID: {player_id}")
            else:
                print(f"No changes made for player ID: {player_id}")
        else:
            print(f"Player ID {player_id} not found in the database")
    
    except Exception as e:
        print(f"Failed to process image {image_file} for player ID: {player_id}, Error: {e}")

conn.commit()
conn.close()