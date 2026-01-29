/**
 * Mind Cloud Forms - Form Builder JavaScript
 */

// ============ Field Types ============
const FIELD_TYPES = {
    text: { label: 'Text Input', icon: 'T', placeholder: 'Short answer text' },
    textarea: { label: 'Long Text', icon: '\u00b6', placeholder: 'Long answer text' },
    email: { label: 'Email', icon: '@', placeholder: 'email@example.com' },
    number: { label: 'Number', icon: '#', placeholder: '0' },
    select: { label: 'Dropdown', icon: '\u25bc', placeholder: 'Select an option' },
    radio: { label: 'Multiple Choice', icon: '\u25cb', placeholder: '' },
    checkbox: { label: 'Checkboxes', icon: '\u2610', placeholder: '' },
    date: { label: 'Date', icon: '\ud83d\udcc5', placeholder: '' },
};

// ============ Form Builder Class ============
class FormBuilder {
    constructor() {
        this.form = {
            id: null,
            title: 'Untitled Form',
            description: '',
            fields: []
        };
        this.selectedFieldIndex = null;
        this.init();
    }

    init() {
        // Load existing form if editing
        const existingForm = window.EXISTING_FORM;
        if (existingForm) {
            this.form = existingForm;
        }

        this.render();
        this.bindEvents();
    }

    bindEvents() {
        // Form title/description
        document.getElementById('form-title')?.addEventListener('input', (e) => {
            this.form.title = e.target.value || 'Untitled Form';
        });

        document.getElementById('form-description')?.addEventListener('input', (e) => {
            this.form.description = e.target.value;
        });

        // Add field buttons
        document.querySelectorAll('.field-type-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const type = btn.dataset.type;
                this.addField(type);
            });
        });

        // Save form
        document.getElementById('save-form')?.addEventListener('click', () => {
            this.saveForm();
        });

        // Preview form
        document.getElementById('preview-form')?.addEventListener('click', () => {
            if (this.form.id) {
                window.open(`/f/${this.form.id}`, '_blank');
            } else {
                alert('Please save the form first');
            }
        });
    }

    addField(type) {
        const field = {
            id: 'field_' + Date.now(),
            type: type,
            label: FIELD_TYPES[type].label,
            placeholder: FIELD_TYPES[type].placeholder,
            required: false,
            options: ['checkbox', 'radio', 'select'].includes(type) ? ['Option 1', 'Option 2'] : []
        };

        this.form.fields.push(field);
        this.render();
        this.selectField(this.form.fields.length - 1);
    }

    removeField(index) {
        this.form.fields.splice(index, 1);
        this.selectedFieldIndex = null;
        this.render();
    }

    moveField(fromIndex, toIndex) {
        if (toIndex < 0 || toIndex >= this.form.fields.length) return;

        const field = this.form.fields.splice(fromIndex, 1)[0];
        this.form.fields.splice(toIndex, 0, field);
        this.selectedFieldIndex = toIndex;
        this.render();
    }

    selectField(index) {
        this.selectedFieldIndex = index;
        this.renderFieldEditor();
    }

    updateField(index, updates) {
        Object.assign(this.form.fields[index], updates);
        this.render();
    }

    render() {
        this.renderFieldsList();
        this.renderFieldEditor();
    }

    renderFieldsList() {
        const container = document.getElementById('fields-list');
        if (!container) return;

        if (this.form.fields.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">\ud83d\udcdd</div>
                    <h3>No fields yet</h3>
                    <p>Click a field type on the right to add it to your form</p>
                </div>
            `;
            return;
        }

        container.innerHTML = this.form.fields.map((field, index) => `
            <div class="field-card ${this.selectedFieldIndex === index ? 'selected' : ''}"
                 data-index="${index}"
                 onclick="builder.selectField(${index})">
                <div class="field-card-header">
                    <span class="field-card-type">${FIELD_TYPES[field.type]?.icon || ''} ${field.type}</span>
                    <div class="field-card-actions">
                        <button class="field-card-btn" onclick="event.stopPropagation(); builder.moveField(${index}, ${index - 1})" ${index === 0 ? 'disabled' : ''}>
                            \u2191
                        </button>
                        <button class="field-card-btn" onclick="event.stopPropagation(); builder.moveField(${index}, ${index + 1})" ${index === this.form.fields.length - 1 ? 'disabled' : ''}>
                            \u2193
                        </button>
                        <button class="field-card-btn delete" onclick="event.stopPropagation(); builder.removeField(${index})">
                            \u2715
                        </button>
                    </div>
                </div>
                <div class="field-card-label">${field.label || 'Untitled Field'}</div>
                ${field.required ? '<span class="text-accent" style="font-size: 0.8rem;">Required</span>' : ''}
            </div>
        `).join('');
    }

    renderFieldEditor() {
        const container = document.getElementById('field-editor');
        if (!container) return;

        if (this.selectedFieldIndex === null || !this.form.fields[this.selectedFieldIndex]) {
            container.innerHTML = `
                <div class="text-muted text-center" style="padding: 2rem;">
                    Select a field to edit its properties
                </div>
            `;
            return;
        }

        const field = this.form.fields[this.selectedFieldIndex];
        const index = this.selectedFieldIndex;

        container.innerHTML = `
            <h3 style="margin-bottom: 1.5rem;">Edit Field</h3>

            <div class="form-group">
                <label class="form-label">Label</label>
                <input type="text" class="form-input" value="${field.label}"
                       onchange="builder.updateField(${index}, {label: this.value})">
            </div>

            ${['text', 'textarea', 'email', 'number'].includes(field.type) ? `
                <div class="form-group">
                    <label class="form-label">Placeholder</label>
                    <input type="text" class="form-input" value="${field.placeholder || ''}"
                           onchange="builder.updateField(${index}, {placeholder: this.value})">
                </div>
            ` : ''}

            ${['select', 'radio', 'checkbox'].includes(field.type) ? `
                <div class="form-group">
                    <label class="form-label">Options (one per line)</label>
                    <textarea class="form-textarea" rows="4"
                              onchange="builder.updateField(${index}, {options: this.value.split('\\n').filter(o => o.trim())})"
                    >${(field.options || []).join('\n')}</textarea>
                </div>
            ` : ''}

            <div class="form-group">
                <label class="form-check">
                    <input type="checkbox" ${field.required ? 'checked' : ''}
                           onchange="builder.updateField(${index}, {required: this.checked})">
                    <span class="form-check-label">Required field</span>
                </label>
            </div>
        `;
    }

    async saveForm() {
        const saveBtn = document.getElementById('save-form');
        saveBtn.disabled = true;
        saveBtn.textContent = 'Saving...';

        try {
            const response = await fetch('/api/forms', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(this.form)
            });

            const result = await response.json();

            if (result.success) {
                this.form.id = result.id;
                // Update URL without reload
                window.history.replaceState({}, '', `/builder/${result.id}`);
                this.showNotification('Form saved successfully!', 'success');
            } else {
                throw new Error('Failed to save');
            }
        } catch (error) {
            this.showNotification('Failed to save form', 'error');
        } finally {
            saveBtn.disabled = false;
            saveBtn.textContent = 'Save Form';
        }
    }

    showNotification(message, type = 'success') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type}`;
        notification.style.cssText = 'position: fixed; top: 1rem; right: 1rem; z-index: 1001; min-width: 250px;';
        notification.textContent = message;
        document.body.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// ============ Public Form Handler ============
class FormSubmitter {
    constructor(formId) {
        this.formId = formId;
        this.init();
    }

    init() {
        const form = document.getElementById('public-form');
        if (!form) return;

        form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.submitForm();
        });
    }

    async submitForm() {
        const form = document.getElementById('public-form');
        const submitBtn = form.querySelector('button[type="submit"]');
        const formData = new FormData(form);
        const data = {};

        // Process form data
        for (let [key, value] of formData.entries()) {
            // Handle checkboxes (multiple values)
            if (data[key]) {
                if (!Array.isArray(data[key])) {
                    data[key] = [data[key]];
                }
                data[key].push(value);
            } else {
                data[key] = value;
            }
        }

        submitBtn.disabled = true;
        submitBtn.textContent = 'Submitting...';

        try {
            const response = await fetch(`/api/forms/${this.formId}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (result.success) {
                this.showSuccess();
            } else {
                throw new Error('Failed to submit');
            }
        } catch (error) {
            alert('Failed to submit form. Please try again.');
            submitBtn.disabled = false;
            submitBtn.textContent = 'Submit';
        }
    }

    showSuccess() {
        const container = document.querySelector('.container-narrow');
        container.innerHTML = `
            <div class="success-page animate-in">
                <div>
                    <div class="success-icon">\u2713</div>
                    <h1>Thank you!</h1>
                    <p style="color: var(--text-secondary);">Your response has been recorded.</p>
                </div>
            </div>
        `;
    }
}

// ============ Dashboard Functions ============
async function deleteForm(formId) {
    if (!confirm('Are you sure you want to delete this form? This cannot be undone.')) {
        return;
    }

    try {
        const response = await fetch(`/api/forms/${formId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            location.reload();
        }
    } catch (error) {
        alert('Failed to delete form');
    }
}

async function exportResponses(formId) {
    window.location.href = `/api/forms/${formId}/export`;
}

// ============ Initialize ============
let builder;

document.addEventListener('DOMContentLoaded', () => {
    // Initialize form builder if on builder page
    if (document.getElementById('fields-list')) {
        builder = new FormBuilder();
    }

    // Initialize form submitter if on public form page
    const publicForm = document.getElementById('public-form');
    if (publicForm) {
        new FormSubmitter(publicForm.dataset.formId);
    }
});
