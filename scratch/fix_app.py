import re

with open('app_legacy.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Remove duplicate @admin_required
# It usually appears as:
# @app.route(...)
# @admin_required
# @login_required
# @admin_required
code = re.sub(r'(@admin_required\s*@login_required\s*)@admin_required\s*', r'\1', code)

# 2. Fix create_event, edit_event, manage_attendance conflicting @admin_required and @organizer_required
# Example: 
# @app.route('/organizer/events/new'...)
# @admin_required
# @login_required
# @organizer_required
code = re.sub(r'@admin_required(\s*@login_required\s*@organizer_required)', r'\1', code)

# 3. Secure checkin_scan
# @app.route('/organizer/checkin/scan', methods=['POST'])
# @login_required
# def checkin_scan():
code = re.sub(
    r"(@app\.route\('/organizer/checkin/scan', methods=\['POST'\]\)\s*@login_required\s*)",
    r"\1@organizer_required\n",
    code
)

# 4. Secure api_add_signatory and api_remove_signatory
# @app.route('/api/certificates/signatory', methods=['POST'])
# @login_required
code = re.sub(
    r"(@app\.route\('/api/certificates/signatory\w*', methods=\['POST'\]\)\s*@login_required\s*)",
    r"\1@admin_required\n",
    code
)

# 5. Rate limiting on auth
# @app.route('/login', methods=['GET', 'POST'])
# def login():
code = re.sub(
    r"(@app\.route\('/login', methods=\['GET', 'POST'\]\)\s*)",
    r"\1@limiter.limit('5 per minute')\n",
    code
)
code = re.sub(
    r"(@app\.route\('/register', methods=\['GET', 'POST'\]\)\s*)",
    r"\1@limiter.limit('5 per minute')\n",
    code
)
code = re.sub(
    r"(@app\.route\('/reset-password', methods=\['GET', 'POST'\]\)\s*)",
    r"\1@limiter.limit('3 per minute')\n",
    code
)

# 6. Wrap demo data in init_db
# Find where demo data starts (around line 3555: # Seed sample venues)
# We will wrap everything from # Seed sample venues down to before db.session.commit()
demo_start = "# Seed sample venues"
demo_end_marker = "db.session.commit()\n        print(\"✅ Database initialized with demo data.\")"
if demo_start in code and demo_end_marker in code:
    parts = code.split(demo_start, 1)
    before = parts[0]
    rest = parts[1]
    
    parts2 = rest.split(demo_end_marker, 1)
    demo_content = parts2[0]
    after = demo_end_marker + parts2[1]
    
    # Indent demo_content
    indented_demo = "\n".join("    " + line for line in demo_content.split("\n"))
    
    wrapped_demo = f"if os.environ.get('INJECT_DEMO_DATA') == 'True':\n            {demo_start}\n{indented_demo}\n        "
    code = before + wrapped_demo + after


with open('app_legacy.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Done patching app_legacy.py")
