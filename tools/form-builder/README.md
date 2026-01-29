# Mind Cloud Forms

A custom form builder with Mind Cloud styling - dark theme, elegant typography, and lime green accents.

## Features

- **Visual Form Builder** - Drag-and-drop style interface to create forms
- **Multiple Field Types** - Text, long text, email, number, date, dropdown, multiple choice, checkboxes
- **Response Collection** - Automatically stores all form submissions
- **Response Dashboard** - View and export responses as CSV
- **Mind Cloud Styling** - Beautiful dark theme matching the Mind Cloud aesthetic

## Quick Start

1. Install dependencies:
```bash
cd tools/form-builder
pip install -r requirements.txt
```

2. Run the server:
```bash
python server.py
```

3. Open your browser to `http://localhost:8000`

## Usage

### Creating a Form

1. Click "Create Form" from the dashboard
2. Set your form title and description
3. Add fields by clicking field types in the sidebar
4. Configure each field (label, placeholder, required, options)
5. Click "Save Form"

### Sharing Forms

After saving, share your form using the URL:
```
http://localhost:8000/f/{form-id}
```

### Viewing Responses

1. Go to the dashboard
2. Click "Responses" on any form
3. Export to CSV using the "Export CSV" button

## Field Types

| Type | Description |
|------|-------------|
| Text Input | Single-line text field |
| Long Text | Multi-line textarea |
| Email | Email validation |
| Number | Numeric input |
| Date | Date picker |
| Dropdown | Select from options |
| Multiple Choice | Radio buttons |
| Checkboxes | Multiple selections |

## File Structure

```
form-builder/
├── server.py           # FastAPI backend
├── requirements.txt    # Python dependencies
├── data/
│   ├── forms/         # Form definitions (JSON)
│   └── responses/     # Form responses (JSON)
├── static/
│   ├── css/
│   │   └── style.css  # Mind Cloud styling
│   └── js/
│       └── app.js     # Form builder logic
└── templates/
    ├── base.html      # Base template
    ├── index.html     # Dashboard
    ├── builder.html   # Form builder
    ├── form.html      # Public form view
    └── responses.html # Responses dashboard
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Dashboard |
| GET | `/builder` | Create new form |
| GET | `/builder/{id}` | Edit existing form |
| GET | `/f/{id}` | Public form view |
| GET | `/responses/{id}` | View responses |
| POST | `/api/forms` | Create/update form |
| DELETE | `/api/forms/{id}` | Delete form |
| POST | `/api/forms/{id}/submit` | Submit response |
| GET | `/api/forms/{id}/export` | Export CSV |

## Customization

The styling uses CSS variables in `static/css/style.css`. Key variables:

```css
:root {
    --bg-primary: #0a0a0f;      /* Main background */
    --bg-card: #1a1a24;         /* Card backgrounds */
    --accent: #c8ff00;          /* Lime green accent */
    --text-primary: #ffffff;    /* Main text */
    --font-serif: 'Playfair Display'; /* Headings */
}
```

## License

MIT License - See the main repository LICENSE file.
