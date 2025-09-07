## Outline → Calendar

Convert university course outlines into a unified calendar automatically.
<img width="1920" height="989" alt="outline-calendar" src="https://github.com/user-attachments/assets/e46eb102-edf1-4612-9202-651fa65c1071" />

## Overview
<hr>

## Key Features  
- 📷 **Timetable to Calendar** – Upload a screenshot, get structured class times and locations.  
- 🗂 **Outline Parsing** – Scrapes course websites for building names, room numbers, lecture types timings.
- 🏫 **Detailed Event Names** – Each calendar event includes course code, lecture type, building, and room number (e.g., *STAT 230 (LEC) @ DC 1351*).  
- 📅 **Instant Calendar Export** – Download `.ics` files and import to Google, Apple, or Outlook.   
- 🌐 **Cross-Platform** – Works across desktop and mobile calendar apps.  

## 🔄 Usage Flow
1. **Upload** – Drag in or upload .html files of your UWaterloo Course Outlines. 
2. **Process** – BeautifulSoup scrapes outlines and extracts structured schedule data
3. **Generate** – The app compiles everything into a unified `.ics` file.  
4. **Import** – Add it to your calendar app of choice — done!

## 🛠 Tech Stack  

**Frontend**  
- HTML/CSS/JSS

**Backend**  
- Python [Flask] – web framework  
- BeautifulSoup – web scraping for outlines  
- datetime (.ics) generation 

  ## 📂 Project Structure  

```text
outlines-to-calendar/
│
├── static/                  # Static assets (CSS, JS, images)
│   ├── images/              # App images and icons
│   ├── scripts/             # Frontend scripts
│   └── styles/              # Stylesheets
│
├── templates/               # HTML templates (Jinja2 for Flask)
│   ├── errors.html          # Error page
│   ├── sections.html        # Parsed sections display
│   └── upload.html          # Upload form
│
├── app.py                   # Main Flask application entry point
├── calendar_utils.py        # Functions for calendar (.ics) file generation
├── forms.py                 # Form handling (Flask-WTF or similar)
├── outline_parser.py        # Scraping/parsing logic for course outlines
├── .gitignore               # Ignored files for Git
```

## 🚀 Getting Started  

Follow these steps to run the project locally.  

### Prerequisites  
- Python 3.9+  
- [pip](https://pip.pypa.io/) (Python package manager)  
- [Flask](https://flask.palletsprojects.com/)  

### Installation  

```bash
# Clone the repository
git clone https://github.com/Keeret-Mahi/outlines-to-calendar.git
cd outlines-to-calendar

# Install dependencies
pip install -r requirements.txt

python3 app.py
```

