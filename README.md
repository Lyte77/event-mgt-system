🎟️ Event Management System

A lightweight Django + HTMX + Alpine.js + TailwindCSS project for managing events, creating tickets, and tracking attendees.

🚀 Features (Current Progress)
    
    🔐 User Authentication (Signup, Login, Logout)
    
    📝 Event Creation with event creation page
    
    📋 Event Listing in a responsive table layout

    🎨 Modern UI with TailwindCSS

🛠️ Tech Stack

    Backend: Django, Django ORM
    
    Frontend: TailwindCSS, Alpine.js, HTMX
    
    Database: SQLite 
    
    Template Engine: Django Templates
    

📂 Project Structure
    
    event_management_sys/
    │── events/          # Event app (models, views, templates, forms)
    │── accounts/           # User authentication & profiles
    │── templates/       # Shared HTML templates
    │── static/          # TailwindCSS, JS, assets
    │── manage.py


⚙️ Installation & Setup

1. Clone the repo

		git clone https://github.com/yourusername/event-mgt-system.git
		cd event-management_sys

2. Create virtual environment & install dependencies
			python -m venv venv
			source venv/bin/activate   # Linux/Mac
			venv\Scripts\activate      # Windows
			
			pip install -r requirements.txt
   
3. Run migrations
   		python manage.py migrate
   
4. Createsuperuser
   			python manage.py createsuperuser

5. Start development server
   			python manage.py runserver

🤝 Contributing

PRs are welcome! For major changes, please open an issue first to discuss what you’d like to change.
