from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'  # Change in production!

# Sample events data (in-memory)
EVENTS = [
    {
        'id': 1,
        'title': '🎨 Community Art Class',
        'date': '2026-01-20',
        'time': '10:00 AM',
        'location': 'Downtown Community Center',
        'description': 'Join us for a relaxing watercolor painting session. All materials provided!',
        'tags': ['art', 'creative', 'indoor'],
        'accessibility_level': 5,
        'social_level': 4,
        'noise_level': 2,
        'transportation_needs': 1,
        'physical_difficulty': 1,
        'distance_miles': 2.3
    },
    {
        'id': 2,
        'title': '📚 Book Club: Classic Literature',
        'date': '2026-01-22',
        'time': '2:00 PM',
        'location': 'Public Library',
        'description': 'This month we\'re discussing "To Kill a Mockingbird". Tea and cookies provided.',
        'tags': ['books', 'discussion', 'indoor'],
        'accessibility_level': 5,
        'social_level': 5,
        'noise_level': 2,
        'transportation_needs': 2,
        'physical_difficulty': 1,
        'distance_miles': 1.5
    },
    {
        'id': 3,
        'title': '🚶 Morning Walk Group',
        'date': '2026-01-21',
        'time': '8:00 AM',
        'location': 'Riverside Park',
        'description': 'Gentle morning walk along the riverside trail. All fitness levels welcome!',
        'tags': ['exercise', 'outdoor', 'nature'],
        'accessibility_level': 3,
        'social_level': 3,
        'noise_level': 1,
        'transportation_needs': 2,
        'physical_difficulty': 3,
        'distance_miles': 3.1
    },
    {
        'id': 4,
        'title': '🎵 Live Jazz Music Night',
        'date': '2026-01-23',
        'time': '7:00 PM',
        'location': 'The Blue Note Cafe',
        'description': 'Enjoy live jazz music with local musicians. Light refreshments available.',
        'tags': ['music', 'entertainment', 'indoor'],
        'accessibility_level': 4,
        'social_level': 3,
        'noise_level': 4,
        'transportation_needs': 3,
        'physical_difficulty': 1,
        'distance_miles': 4.2
    },
    {
        'id': 5,
        'title': '🌱 Gardening Workshop',
        'date': '2026-01-24',
        'time': '11:00 AM',
        'location': 'Community Garden',
        'description': 'Learn about winter gardening and indoor plant care. Get your hands dirty!',
        'tags': ['gardening', 'outdoor', 'educational'],
        'accessibility_level': 3,
        'social_level': 4,
        'noise_level': 2,
        'transportation_needs': 2,
        'physical_difficulty': 3,
        'distance_miles': 2.8
    },
    {
        'id': 6,
        'title': '🍰 Baking & Social Hour',
        'date': '2026-01-25',
        'time': '3:00 PM',
        'location': 'Senior Center Kitchen',
        'description': 'Bake cookies together and share stories. Perfect for making new friends!',
        'tags': ['cooking', 'social', 'indoor'],
        'accessibility_level': 5,
        'social_level': 5,
        'noise_level': 3,
        'transportation_needs': 1,
        'physical_difficulty': 2,
        'distance_miles': 1.2
    },
    {
        'id': 7,
        'title': '🧘 Gentle Yoga',
        'date': '2026-01-26',
        'time': '9:00 AM',
        'location': 'Wellness Studio',
        'description': 'Chair yoga for all abilities. Focus on flexibility and relaxation.',
        'tags': ['exercise', 'wellness', 'indoor'],
        'accessibility_level': 5,
        'social_level': 2,
        'noise_level': 1,
        'transportation_needs': 2,
        'physical_difficulty': 2,
        'distance_miles': 2.0
    },
    {
        'id': 8,
        'title': '🎬 Classic Movie Matinee',
        'date': '2026-01-27',
        'time': '1:00 PM',
        'location': 'Historic Theater',
        'description': 'Enjoy "Casablanca" on the big screen. Popcorn included!',
        'tags': ['movies', 'entertainment', 'indoor'],
        'accessibility_level': 5,
        'social_level': 2,
        'noise_level': 3,
        'transportation_needs': 2,
        'physical_difficulty': 1,
        'distance_miles': 3.5
    }
]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    session['user'] = {
        'name': data.get('name'),
        'phone': data.get('phone')
    }
    return jsonify({'success': True, 'message': 'Logged in successfully'})

@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    data = request.json
    session['user'].update(data)
    session.modified = True
    return jsonify({'success': True, 'message': 'Profile updated'})

@app.route('/discover')
def discover():
    if 'user' not in session:
        return redirect(url_for('home'))
    return render_template('discover.html', user=session['user'])

@app.route('/event/<int:event_id>')
def event_page(event_id):
    if 'user' not in session:
        return redirect(url_for('home'))
    
    event = next((e for e in EVENTS if e['id'] == event_id), None)
    if not event:
        return "Event not found", 404
    
    return render_template('event.html', event=event, user=session['user'])

@app.route('/filter_events', methods=['POST'])
def filter_events():
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    filters = request.json
    filtered = EVENTS.copy()
    
    # Filter by search term
    search = filters.get('search', '').lower()
    if search:
        filtered = [e for e in filtered if 
                   search in e['title'].lower() or 
                   search in e['description'].lower() or
                   any(search in tag for tag in e['tags'])]
    
    # Filter by tags
    tags = filters.get('tags', [])
    if tags:
        filtered = [e for e in filtered if any(tag in e['tags'] for tag in tags)]
    
    # Filter by accessibility level (minimum)
    if 'accessibility_level' in filters:
        min_access = int(filters['accessibility_level'])
        filtered = [e for e in filtered if e['accessibility_level'] >= min_access]
    
    # Filter by social level
    if 'social_level' in filters:
        social = int(filters['social_level'])
        filtered = [e for e in filtered if abs(e['social_level'] - social) <= 1]
    
    # Filter by noise level
    if 'noise_level' in filters:
        noise = int(filters['noise_level'])
        filtered = [e for e in filtered if abs(e['noise_level'] - noise) <= 1]
    
    # Filter by physical difficulty
    if 'physical_difficulty' in filters:
        difficulty = int(filters['physical_difficulty'])
        filtered = [e for e in filtered if e['physical_difficulty'] <= difficulty]
    
    # Filter by distance
    if 'max_distance' in filters:
        max_dist = float(filters['max_distance'])
        filtered = [e for e in filtered if e['distance_miles'] <= max_dist]
    
    return jsonify({'success': True, 'events': filtered})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)