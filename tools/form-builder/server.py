"""
Mind Cloud Form Builder - A custom form builder with Mind Cloud styling
"""
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Mind Cloud Forms")

# Setup paths
BASE_DIR = Path(__file__).parent
FORMS_DIR = BASE_DIR / "data" / "forms"
RESPONSES_DIR = BASE_DIR / "data" / "responses"

# Ensure directories exist
FORMS_DIR.mkdir(parents=True, exist_ok=True)
RESPONSES_DIR.mkdir(parents=True, exist_ok=True)

# Setup static files and templates
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


def get_form(form_id: str) -> Optional[dict]:
    """Load a form by ID"""
    form_path = FORMS_DIR / f"{form_id}.json"
    if form_path.exists():
        return json.loads(form_path.read_text())
    return None


def save_form(form_data: dict) -> str:
    """Save a form and return its ID"""
    form_id = form_data.get("id") or str(uuid.uuid4())[:8]
    form_data["id"] = form_id
    form_data["updated_at"] = datetime.now().isoformat()
    if "created_at" not in form_data:
        form_data["created_at"] = form_data["updated_at"]

    form_path = FORMS_DIR / f"{form_id}.json"
    form_path.write_text(json.dumps(form_data, indent=2))
    return form_id


def get_all_forms() -> list:
    """Get all forms"""
    forms = []
    for form_path in FORMS_DIR.glob("*.json"):
        form = json.loads(form_path.read_text())
        forms.append(form)
    return sorted(forms, key=lambda x: x.get("updated_at", ""), reverse=True)


def get_responses(form_id: str) -> list:
    """Get all responses for a form"""
    responses_path = RESPONSES_DIR / f"{form_id}.json"
    if responses_path.exists():
        return json.loads(responses_path.read_text())
    return []


def save_response(form_id: str, response_data: dict):
    """Save a form response"""
    responses = get_responses(form_id)
    response_data["id"] = str(uuid.uuid4())[:8]
    response_data["submitted_at"] = datetime.now().isoformat()
    responses.append(response_data)

    responses_path = RESPONSES_DIR / f"{form_id}.json"
    responses_path.write_text(json.dumps(responses, indent=2))


# ============ Pages ============

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Main dashboard - list all forms"""
    forms = get_all_forms()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "forms": forms
    })


@app.get("/builder", response_class=HTMLResponse)
@app.get("/builder/{form_id}", response_class=HTMLResponse)
async def builder(request: Request, form_id: Optional[str] = None):
    """Form builder page"""
    form = None
    if form_id:
        form = get_form(form_id)
        if not form:
            raise HTTPException(status_code=404, detail="Form not found")

    return templates.TemplateResponse("builder.html", {
        "request": request,
        "form": form
    })


@app.get("/f/{form_id}", response_class=HTMLResponse)
async def public_form(request: Request, form_id: str):
    """Public form view for respondents"""
    form = get_form(form_id)
    if not form:
        raise HTTPException(status_code=404, detail="Form not found")

    return templates.TemplateResponse("form.html", {
        "request": request,
        "form": form
    })


@app.get("/responses/{form_id}", response_class=HTMLResponse)
async def view_responses(request: Request, form_id: str):
    """View responses for a form"""
    form = get_form(form_id)
    if not form:
        raise HTTPException(status_code=404, detail="Form not found")

    responses = get_responses(form_id)
    return templates.TemplateResponse("responses.html", {
        "request": request,
        "form": form,
        "responses": responses
    })


# ============ API Endpoints ============

@app.post("/api/forms")
async def create_form(request: Request):
    """Create or update a form"""
    data = await request.json()
    form_id = save_form(data)
    return {"success": True, "id": form_id}


@app.delete("/api/forms/{form_id}")
async def delete_form(form_id: str):
    """Delete a form"""
    form_path = FORMS_DIR / f"{form_id}.json"
    responses_path = RESPONSES_DIR / f"{form_id}.json"

    if form_path.exists():
        form_path.unlink()
    if responses_path.exists():
        responses_path.unlink()

    return {"success": True}


@app.post("/api/forms/{form_id}/submit")
async def submit_form(form_id: str, request: Request):
    """Submit a form response"""
    form = get_form(form_id)
    if not form:
        raise HTTPException(status_code=404, detail="Form not found")

    data = await request.json()
    save_response(form_id, {"answers": data})
    return {"success": True}


@app.get("/api/forms/{form_id}/responses")
async def get_form_responses(form_id: str):
    """Get all responses for a form as JSON"""
    form = get_form(form_id)
    if not form:
        raise HTTPException(status_code=404, detail="Form not found")

    responses = get_responses(form_id)
    return {"form": form, "responses": responses}


@app.get("/api/forms/{form_id}/export")
async def export_responses(form_id: str):
    """Export responses as CSV"""
    form = get_form(form_id)
    if not form:
        raise HTTPException(status_code=404, detail="Form not found")

    responses = get_responses(form_id)

    if not responses:
        return JSONResponse(content={"error": "No responses"}, status_code=404)

    # Build CSV
    fields = form.get("fields", [])
    headers = ["Submitted At"] + [f.get("label", f"Field {i}") for i, f in enumerate(fields)]

    csv_lines = [",".join(f'"{h}"' for h in headers)]

    for resp in responses:
        row = [resp.get("submitted_at", "")]
        answers = resp.get("answers", {})
        for field in fields:
            field_id = field.get("id", "")
            value = answers.get(field_id, "")
            if isinstance(value, list):
                value = "; ".join(value)
            row.append(str(value).replace('"', '""'))
        csv_lines.append(",".join(f'"{v}"' for v in row))

    csv_content = "\n".join(csv_lines)

    return JSONResponse(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{form_id}_responses.csv"'}
    )


if __name__ == "__main__":
    import uvicorn
    print("\n  Mind Cloud Forms")
    print("  ================")
    print("  Dashboard: http://localhost:8000")
    print("  Press Ctrl+C to stop\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
