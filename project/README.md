# A personal homepage of mine

#### Video Demo:  <URL HERE>

---

#### Description:
In this homepage you will see functions below:
1. a picture (faded as you scroll the homepage)
2. a frequency recoder (track your study/foucs frequency)
3. a quick navigation (added and deleted are allowed)
4. a to-do list (you are allowed to exporting a txt. file)
5. a timer(via which you can recode your foucs span)

---

## Project Structure

### Root Files
- **app.py** - Main Flask backend application
  - Routes for homepage, records page, heatmap API
  - Manages daily record storage/retrieval in JSON format
  - Export functionality for records as plain text

- **README.md** - Project documentation

### static/ Directory
- **styles.css** - Global stylesheet with dark theme, responsive design, and animations
- **fade.js** - Scroll animations for hero section fade-out effect

### templates/ Directory
- **base.html** - Base template with header navigation and layout
- **index.html** - Homepage with GitHub-style heatmap (52 weeks) and quick navigation
- **records.html** - Daily record system with keywords, todos, plans, insights, and focus mode

### records/ Directory
- Stores JSON files with daily records (named YYYY-MM-DD.json)
- Each file contains: date, keywords, today_done, tomorrow_plan, insights, todos, focus_sessions

---

## Tech Stack
- Backend: Flask
- Frontend: HTML5, CSS3, JavaScript
- Storage: JSON files
- Template Engine: Jinja2