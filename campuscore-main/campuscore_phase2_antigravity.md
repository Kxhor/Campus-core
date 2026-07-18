# CampusCore — Phase 2 Implementation Guide
### Antigravity + Gemini Pro: All Remaining Pages

---

## Current Status

| Layer | Done | Remaining |
|---|---|---|
| CSS Foundation | ✅ design-system.css, layout.css, components.css, responsive.css | — |
| Auth Pages | ✅ login.html | register, reset_password, verify_valid, verify_invalid |
| Student | ✅ dashboard.html, events.html (browse) | event_detail, my_events, announcements, profile, settings |
| Organizer | ✅ dashboard.html | events, event_form, participants, profile, settings, user_settings |
| Admin | ✅ dashboard.html, events.html | analytics, announcements, attendance, audit_logs, event_form, event_stats, profile, settings, students, user_detail, user_form, user_settings, users |
| Email Templates | — | 8 templates (separate track, handled last) |

**Tool:** Antigravity + Gemini Pro for everything. No Kombai.

**Visual reference for every prompt below:** The pages already completed
(`student/dashboard.html`, `admin/dashboard.html`, `student/events.html`,
`organizer/dashboard.html`, `login.html`) are your source of truth for
component patterns and CSS class usage. Every new page must match them.

---

## Step 1 — Smoke Test (Do This Before Writing Any New Page)

Run the app. Spend 20 minutes on this. Fix anything broken before adding new pages.

```
AUTH
□ Login as student → redirects to student dashboard
□ Login as organizer → redirects to organizer dashboard
□ Login as admin → redirects to admin dashboard
□ Logout from sidebar → returns to login page
□ Flash message appears on bad credentials

NAVIGATION
□ Every sidebar link navigates to the correct page for each role
□ Active nav item shows the gold left-bar indicator
□ Breadcrumb in topbar updates on each page
□ Dark mode toggle sets data-theme="dark" on <html>

STUDENT
□ Register for an event → POST succeeds, success flash appears
□ Browse events filter (category) → results update correctly
□ Search field filters event list

SOCKET.IO (open browser DevTools → Console)
□ No "WebSocket connection failed" errors
□ Send a test announcement as admin → floating banner appears on student page

MOBILE (resize browser to 375px)
□ Sidebar is hidden
□ Hamburger appears in topbar
□ Hamburger opens sidebar drawer
□ Overlay tap closes sidebar
```

**If anything above fails, paste this into Antigravity before proceeding:**

```
[CAMPUSCORE DEBUG]

The Flask/Jinja2 app at campuscore-main/ has a completed UI redesign.
The following issue is occurring:

[DESCRIBE THE EXACT ISSUE]

Diagnose in this order:
1. Browser console for JavaScript errors
2. Network tab for 404s on CSS/JS assets
3. Verify url_for() endpoint names in the template match actual Flask route 
   function names in app_legacy.py or blueprint files
4. Verify CSS link order in base.html:
   design-system.css → layout.css → components.css → responsive.css → style.css
5. Verify Jinja2 variables used in the template exist in the route's return 
   render_template() call

Fix only what is broken. Do not refactor anything else. Do not touch Python routes.
```

---

## Step 2 — Remaining Pages (Antigravity Prompts)

Paste each prompt into Antigravity in the order listed. One prompt per session.
After each generation, run the verification prompt at the bottom of this section
before moving to the next page.

---

### PROMPT 1 — Auth: Register Page
**File:** `templates/register.html`

```
CAMPUSCORE REDESIGN — templates/register.html

The login page (templates/login.html) has already been redesigned.
Open it now and study its structure before writing a single line.
The register page uses the IDENTICAL split-panel layout.

LEFT PANEL — copy the dark panel from login.html exactly:
- Same cc-sidebar-bg background, same radial gradient, same logo mark
- Change the hero heading to: "Join the community."
- Change the three feature bullets to:
  * QR-based attendance verified automatically
  * Certificates for every event you attend
  * Live announcements from organisers and admins

RIGHT PANEL — Registration form:
Title: "Create your account"
Subtitle: "Fill in your details to get started"

Before writing the form, open the existing register.html and note the exact
name attribute of every field. Do not change a single name attribute.

Field groups (visual labels, not HTML fieldsets):

GROUP 1 — Personal Information
- Full Name (cc-input)
- Register Number (cc-input)
- Email (cc-input type="email")

GROUP 2 — Academic Details
- Department (cc-select with existing options from current template)
- Year of Study (cc-select: 1st Year | 2nd Year | 3rd Year | 4th Year)
- College name field if it exists in the current form

GROUP 3 — Security
- Password (cc-input type="password" with show/hide toggle — same JS pattern
  as login.html)
- Confirm Password (cc-input type="password")
- Password strength bar below the password field:
  Three segments side by side (each 30% width, gap between them)
  JS logic (no library): count length + check for number + special char
  Red = length < 8, Amber = length >= 8, Green = length >= 8 + number + symbol
  Add this as an inline <script> at the bottom of the form

Submit button: cc-btn cc-btn--primary full-width "Create Account"
Below form: "Already have an account? Sign In" — link to login page

If the current register.html has a Google OAuth button, keep it.
Place it above the field groups with a divider ("or sign up with email").

CONSTRAINTS:
- Every field name attribute must match the current register.html exactly
- Keep the CSRF token — copy the exact pattern from the current template
- Keep the form action URL unchanged
- Keep any existing client-side validation JS
```

---

### PROMPT 2 — Auth: Reset Password Page
**File:** `templates/reset_password.html`

```
CAMPUSCORE REDESIGN — templates/reset_password.html

Open the current reset_password.html before writing anything.
Identify whether it has one state or two (request reset vs set new password).
Keep the Jinja2 conditional logic that determines which state renders.

Layout: Full-page centered, single card.
Background: linear-gradient(135deg, var(--cc-sidebar-bg) 0%, #2E1220 100%)
Card: cc-card cc-card--elevated, max-width 420px, centered with margin auto,
      margin-top: clamp(60px, 10vh, 120px)

Card contents:
- Logo mark (centered): same .cc-sidebar__logo-icon div from base.html,
  display block, margin: 0 auto var(--space-6)
- Title: "Reset Password" — centered, font-size var(--text-xl), 
  font-weight var(--weight-semibold)

STATE 1 — Request reset (if no token in URL / no token variable):
Subtitle: "We'll email you a reset link"
- Email field (cc-label + cc-input)
- Submit: cc-btn cc-btn--primary full-width "Send Reset Link"
- "Back to login" — text link below button

STATE 2 — Set new password (if token exists and is valid):
Subtitle: "Enter your new password"
- New Password (cc-input type="password" with toggle)
- Confirm Password (cc-input type="password")
- Submit: cc-btn cc-btn--primary full-width "Reset Password"

Flash messages: cc-flash component pattern from base.html

CONSTRAINTS:
- All field name attributes unchanged
- All form action URLs unchanged
- CSRF token kept — copy exact pattern from current template
- Jinja2 state detection logic (the existing if/else) kept exactly as-is
```

---

### PROMPT 3 — Auth: Verification Pages
**Files:** `templates/verify_valid.html` AND `templates/verify_invalid.html`

```
CAMPUSCORE REDESIGN — verify_valid.html and verify_invalid.html

Do both in one pass. Same layout, different content.

Layout for both:
Same background gradient as reset_password.html.
Single cc-card, max-width 400px, centered.
Card padding: var(--space-10) var(--space-8)
Text alignment: center throughout

verify_valid.html:
Icon circle (72px, border-radius full):
  background: var(--cc-success-bg), border: 2px solid var(--cc-success-border)
  Contents: <i class="fas fa-check" style="font-size:28px;color:var(--cc-success)">
Title: "Email Verified" — font-size var(--text-xl), weight semibold
Body: "Your account is ready. Sign in to get started."
  font-size var(--text-sm), color var(--cc-text-secondary), margin var(--space-4) 0
Button: cc-btn cc-btn--primary full-width → url_for('login') or existing href

verify_invalid.html:
Icon circle: background var(--cc-error-bg), border var(--cc-error-border)
  Contents: <i class="fas fa-times" style="font-size:28px;color:var(--cc-error)">
Title: "Link Expired"
Body: "This verification link is no longer valid. Request a new one below."
Button: cc-btn cc-btn--outline full-width → keep existing href from current template

Keep any Jinja2 variable references (email display, etc.) from the originals.
```

---

### PROMPT 4 — Student: Event Detail Page
**File:** `templates/student/event_detail.html`

```
CAMPUSCORE REDESIGN — templates/student/event_detail.html

Open the current event_detail.html and note every Jinja2 variable used.
Open student/dashboard.html and study the cc-card, cc-date-badge, 
cc-badge, and cc-event-list-item patterns. This page uses the same components.

LAYOUT inside {% block content %}:

SECTION 1 — Event Hero (full-width cc-card, no inner padding, overflow:hidden)
Inner layout: CSS grid, two columns (1fr 1fr), collapse to 1fr on mobile

  Left cell — Event image:
  If event.image_url: <img> with object-fit:cover, height:320px, width:100%
  Else: cc-event-card__image-placeholder (same class from browse events page)
        height:320px, background linear-gradient using --cc-crimson-muted

  Right cell — Event metadata, padding var(--space-8):
  - Badges row: cc-badge cc-badge--[category] + cc-badge cc-badge--[status]
    (status badge: upcoming/active/completed/cancelled using existing status value)
  - Event title: font-family var(--font-display), font-size var(--text-2xl),
    font-weight 700, letter-spacing -0.02em, margin var(--space-4) 0
  - Metadata rows (each row: icon + label pattern, same as cc-event-card__meta-item):
    * Date: fas fa-calendar + formatted date
    * Time: fas fa-clock + start_time to end_time (or just start_time)
    * Venue: fas fa-map-marker-alt + venue name
    * Organizer: fas fa-user + organizer name
    * Registration Deadline: fas fa-hourglass-half + deadline date

SECTION 2 — Content grid (CSS grid: 2fr 1fr, gap var(--space-6), margin-top same)

  LEFT COLUMN:
  
  Card 1 — "About this Event" (cc-card)
  cc-card__header with title
  cc-card__body: event.description in full (no truncation)
  Paragraph spacing: line-height var(--leading-relaxed)
  
  Card 2 — "Tags" (cc-card) — only render if event has tags
  cc-card__body: tag pills using cc-tag class for each tag

  RIGHT COLUMN:
  
  Card — "Registration" (cc-card cc-card--elevated)
  cc-card__header: "Registration"
  cc-card__body:
  
  Capacity display:
    "X / Y seats filled" — font-size var(--text-sm), color var(--cc-text-muted)
    cc-capacity-bar below (same component from browse events page)
    Seats remaining: bold count + "seats available" or "Full" in error color
  
  Divider: border-top 1px solid var(--cc-border-subtle), margin var(--space-4) 0
  
  REGISTRATION STATE (use Jinja2 conditionals — check existing template for variables):
  
  If student is registered (confirmed):
    cc-badge cc-badge--registered full-width centered
    "You are registered for this event"
    If event has QR code: render the existing QR code block exactly as-is
    "Cancel Registration" → cc-btn cc-btn--ghost cc-btn--sm (keep existing form/action)
  
  If student is waitlisted:
    cc-badge cc-badge--pending
    "You are #[waitlist_position] on the waitlist"
    Muted explanation text
  
  If registration is open and seats available:
    cc-btn cc-btn--primary full-width "Register Now"
    Keep the existing POST form — only update button class
  
  If registration deadline passed:
    Muted text: "Registration closed"
  
  If event is completed:
    Muted text: "This event has ended"

CONSTRAINTS:
- Every Jinja2 variable name unchanged
- QR code rendering logic untouched (just wrapped in card)
- Registration form action URL and CSRF token unchanged
- Cancellation form action URL unchanged
- All conditional logic (if registered / if waitlisted / etc.) unchanged
```

---

### PROMPT 5 — Student: My Events Page
**File:** `templates/student/my_events.html`

```
CAMPUSCORE REDESIGN — templates/student/my_events.html

Open the current my_events.html and note every variable and conditional.
Open student/dashboard.html and study cc-event-list-item and cc-date-badge.

LAYOUT inside {% block content %}:

PAGE HEADER:
cc-page-title: "My Events"
cc-page-subtitle: "Your registration history and upcoming attendance"

TAB GROUP (cc-tab-group):
All | Upcoming | Attended | Waitlisted | Cancelled
Pass active tab via URL param — keep existing filter URL pattern exactly.

EVENTS LIST (cc-card, no inner padding on body):
cc-card__header: tab label + count of items in this tab

For each event in the list, use cc-event-list-item layout:
Left: cc-date-badge (day + month from event.date)
Center: 
  cc-event-list-item__name: event title
  cc-event-list-item__meta: venue icon + venue | time icon + time
Right: status badge + action button

STATUS AND ACTION COMBINATIONS:

Registration status = confirmed, event not yet passed:
  cc-badge cc-badge--upcoming "Upcoming"
  Action: cc-btn cc-btn--ghost cc-btn--sm "View" → event detail link

Registration status = confirmed, attendance status = present:
  cc-badge cc-badge--completed "Attended"
  If certificate is available: cc-btn cc-btn--primary cc-btn--sm "Download Certificate"
    Keep existing certificate download href/form exactly
  If not yet available: muted span "Certificate pending"

Registration status = waitlisted:
  cc-badge cc-badge--pending "Waitlisted"
  "Position #[waitlist_position]" — font-size var(--text-xs), muted
  Action: cc-btn cc-btn--ghost cc-btn--sm "Cancel" (keep existing form)

Registration status = cancelled:
  cc-badge cc-badge--cancelled "Cancelled"
  No action button

EMPTY STATE for each empty filtered tab:
cc-empty-state with appropriate icon and message:
  Upcoming empty: fas fa-calendar, "No upcoming events. Browse events to register."
  Attended empty: fas fa-check-circle, "No attended events yet."
  Waitlisted empty: fas fa-hourglass, "You are not on any waitlists."
  Cancelled empty: fas fa-times-circle, "No cancelled registrations."

CONSTRAINTS:
- All Jinja2 loop variables unchanged
- Certificate download href/form unchanged
- Cancellation form action and CSRF token unchanged
- waitlist_position variable reference unchanged
- Tab filter URL param name unchanged
```

---

### PROMPT 6 — Student: Announcements Page
**File:** `templates/student/announcements.html`

```
CAMPUSCORE REDESIGN — templates/student/announcements.html

Open the current template and note all variables before starting.

LAYOUT inside {% block content %}:

PAGE HEADER:
cc-page-title: "Announcements"
cc-page-subtitle: "Platform-wide broadcasts from administrators"

FILTER (inline, above the list):
cc-tab-group: All | Info | Warning | Urgent
Pass filter via URL param — keep existing filter logic.
Right side: unread count badge if > 0 (cc-badge cc-badge--pending)

ANNOUNCEMENTS CARD (cc-card):
cc-card__header: "Broadcasts"
cc-card__body padding 0

For each announcement, one list row:
Row layout: display flex, align-items flex-start, gap var(--space-4)
Padding: var(--space-4) var(--space-5)
Separator: border-bottom 1px solid var(--cc-border-subtle)

If announcement is unread: background var(--cc-crimson-muted-2) on the row

Left: Priority indicator strip
  Width 3px, height 100%, border-radius var(--radius-full)
  Info=var(--cc-info), Warning=var(--cc-warning), Urgent=var(--cc-crimson)

Center: Content
  Priority icon in small colored circle (24px):
    Info: fas fa-info-circle, color var(--cc-info)
    Warning: fas fa-exclamation-triangle, color var(--cc-warning)
    Urgent: fas fa-exclamation-circle, color var(--cc-crimson)
  Message text: font-weight 600 if unread, 400 if read
  Footer row: "Sent by [created_by.name] · [timestamp]"
    font-size var(--text-xs), color var(--cc-text-muted)

Right: priority badge (cc-badge cc-badge--[priority]) — align-self flex-start

EMPTY STATE if no announcements: fas fa-bullhorn icon, "No announcements yet"

If the current template has mark-as-read logic (click or auto on page load),
keep it exactly as-is. Only wrap the existing logic in the new DOM structure.

CONSTRAINTS:
- All Jinja2 variable names unchanged (announcements, priority, is_read, etc.)
- Mark-as-read AJAX or form logic unchanged
- Filter URL param name unchanged
```

---

### PROMPT 7 — Student/Organizer/Admin: Profile Pages
**Files:** `templates/student/profile.html`, `templates/organizer/profile.html`, `templates/admin/profile.html`

```
CAMPUSCORE REDESIGN — Profile pages (do all three in one pass)

The structure is identical for all three roles. Apply it to all.
Open each current profile template and note variables before writing.

LAYOUT inside {% block content %}:

PROFILE HERO CARD (cc-card, overflow hidden, no cc-card__body wrapper):

Top band: height 100px
  background linear-gradient(135deg, var(--cc-crimson) 0%, var(--cc-crimson-dark) 100%)
  position relative

Avatar (overlapping the band):
  position absolute, bottom -32px, left var(--space-8)
  width 72px, height 72px
  background var(--cc-surface), border-radius var(--radius-full)
  border 3px solid var(--cc-surface)
  Inner circle (64px): cc-user-avatar style
    Background: var(--cc-crimson) for student, #7C3AED for organizer, var(--cc-crimson) for admin
    Initials: first letter of name, font-size var(--text-xl), color white

Below band, padding var(--space-8), padding-top calc(32px + var(--space-4)):
Name: font-size var(--text-xl), font-weight var(--weight-semibold)
cc-role-badge immediately below name
Department + Year: font-size var(--text-sm), color var(--cc-text-muted)
Register number (if student): font-size var(--text-xs), color var(--cc-text-muted)

TWO-COLUMN LAYOUT (3fr 2fr, gap var(--space-6), margin-top var(--space-6)):

LEFT:
Card — "Personal Information" (cc-card):
cc-card__header: "Personal Information"
  Right side: "Edit Profile" cc-btn cc-btn--ghost cc-btn--sm 
  → link to settings page or existing edit href

cc-card__body: Info rows table
For each field (Name, Email, Register Number, Department, Year, College):
  Row: display flex, padding var(--space-3) 0
  Label: font-size var(--text-sm), color var(--cc-text-muted), width 40%, font-weight 500
  Value: font-size var(--text-sm), color var(--cc-text), width 60%
  Border-bottom: 1px solid var(--cc-border-subtle) (except last row)

RIGHT:
Card — "Activity" (cc-card):
Three stat rows (stacked, not grid):
Each row: icon (in small colored circle) + label + large number
  Events Attended (fas fa-user-check, --cc-success)
  Events Registered (fas fa-ticket-alt, --cc-info)
  Certificates (fas fa-certificate, --cc-gold)
Padding between rows: var(--space-4), border-bottom var(--cc-border-subtle)

Card — "Quick Actions" (cc-card, margin-top var(--space-5)):
List of action links: Settings, Browse Events, My Events
Same style as the quick access card in student/dashboard.html

CONSTRAINTS:
- All Jinja2 variable names unchanged across all three templates
- Edit form (if inline) keeps all field names and CSRF token
- Profile page route links unchanged
```

---

### PROMPT 8 — Student/Organizer/Admin: Settings Pages
**Files:** `templates/student/settings.html`, `templates/organizer/settings.html`, `templates/organizer/user_settings.html`, `templates/admin/settings.html`, `templates/admin/user_settings.html`

```
CAMPUSCORE REDESIGN — Settings pages (do all five in one pass)

Open all five current settings templates. Note which fields differ between roles.
The layout is identical — only the available fields change per role.

LAYOUT inside {% block content %}:

PAGE HEADER: "Settings"

TWO-COLUMN LAYOUT (220px left nav, flex 1 right content):

LEFT — Settings Navigation (cc-card, padding var(--space-2)):
Vertical list of anchor links:
  Account | Notifications | Appearance | Security
Each link: cc-nav-item style but without the left bar
Active: background var(--cc-surface-3), color var(--cc-text), font-weight 600

RIGHT — Settings Sections (stacked cc-cards with id anchors for scroll):

ACCOUNT SECTION (id="account"):
cc-card:
  cc-card__header: "Account Information"
  cc-card__body: Form with editable profile fields
  Before writing fields: open the existing template and copy field names exactly
  Submit: cc-btn cc-btn--primary "Save Changes"
  Keep form action and CSRF token unchanged

NOTIFICATIONS SECTION (id="notifications"):
cc-card:
  cc-card__header: "Notification Preferences"
  cc-card__body: Toggle rows

Toggle switch component (add to bottom of the page in a <style> block since
this is a new component not in components.css):

.cc-toggle { position:relative; display:inline-block; width:44px; height:24px; }
.cc-toggle input { opacity:0; width:0; height:0; position:absolute; }
.cc-toggle__track { position:absolute; cursor:pointer; inset:0;
  background:var(--cc-border-strong); border-radius:var(--radius-full);
  transition:var(--transition-base); }
.cc-toggle__track::before { content:''; position:absolute; height:18px; width:18px;
  left:3px; bottom:3px; background:white; border-radius:50%;
  transition:var(--transition-base); box-shadow:var(--shadow-xs); }
.cc-toggle input:checked + .cc-toggle__track { background:var(--cc-crimson); }
.cc-toggle input:checked + .cc-toggle__track::before { transform:translateX(20px); }

For each notification preference:
Row: display flex, justify-content space-between, align-items center
  padding var(--space-4) 0, border-bottom 1px solid var(--cc-border-subtle)
  Left: label (font-weight 500) + description (font-size xs, muted, margin-top 2px)
  Right: <label class="cc-toggle"><input type="checkbox" name="[existing name]">
         <span class="cc-toggle__track"></span></label>
Keep all existing checkbox name attributes unchanged.

APPEARANCE SECTION (id="appearance"):
cc-card:
  cc-card__header: "Appearance"
  cc-card__body:
  Dark mode row (same toggle component):
    Label: "Dark Mode"
    Description: "Use the dark theme across the application"
    Toggle: keep existing JS dark mode toggle — only change the HTML wrapper
    The existing JS already toggles data-theme on <html> — do not change it

SECURITY SECTION (id="security"):
cc-card:
  cc-card__header: "Change Password"
  cc-card__body: 
  Current Password | New Password | Confirm New Password
  (cc-input fields, keep existing name attributes)
  Submit: cc-btn cc-btn--primary "Update Password"
  Keep form action and CSRF token unchanged

CONSTRAINTS:
- Field name attributes unchanged across all five templates
- CSRF tokens unchanged in all forms
- Dark mode JS logic unchanged — only update surrounding HTML
- Form action URLs unchanged
- Notification preference field names unchanged
```

---

### PROMPT 9 — Organizer: Events List
**File:** `templates/organizer/events.html`

```
CAMPUSCORE REDESIGN — templates/organizer/events.html

Open the current template. Note all variables, filter params, and action URLs.
Open admin/events.html (already redesigned) for the table pattern — 
this page follows the same structure.

LAYOUT inside {% block content %}:

PAGE HEADER:
cc-page-title: "My Events"
cc-page-subtitle: "Manage and track your created events"
Right: cc-btn cc-btn--primary "Create Event" → keep existing href

STAT ROW (compact, cc-grid cc-grid--3):
Three small cc-stat-cards (no hover, reduced padding var(--space-4)):
  My Events total (cc-stat-card--events)
  Total Registrations across my events (cc-stat-card--registered)
  Pending Approval count (cc-stat-card--certs, use warning gold color)

TAB GROUP (cc-tab-group):
All | Draft | Pending | Approved | Active | Completed | Cancelled
Keep existing filter URL param and logic.

FILTER BAR (cc-card, compact):
cc-search-wrapper + Category cc-select + Filter cc-btn --secondary
Keep all existing form field names.

EVENTS TABLE (cc-table-wrapper):
Columns: Event | Date | Registrations | Status | Approval | Actions

Event cell:
  Title (font-weight semibold)
  Category badge (cc-badge cc-badge--[category]) below title

Date cell:
  cc-date-badge style (but inline, not the full component — just day/month display)
  Time below in muted xs text

Registrations cell:
  [count]/[max] text (font-weight semibold)
  cc-capacity-bar below (80px wide)

Status: cc-badge cc-badge--[status]
Approval: cc-badge cc-badge--[approval_status]

Actions cell (right-aligned, display flex gap var(--space-2)):

Show based on Jinja2 conditionals — keep EXISTING conditional logic exactly:

View Stats:
  cc-btn cc-btn--secondary cc-btn--sm cc-btn--icon-only
  fas fa-chart-bar, title="View stats", keep existing href

Edit:
  cc-btn cc-btn--secondary cc-btn--sm cc-btn--icon-only
  fas fa-pencil, keep existing href
  Only show if event is editable (keep existing condition)

Manage Attendance:
  cc-btn cc-btn--primary cc-btn--sm "Attendance"
  Keep existing href
  Only show if event is approved/active (keep existing condition)

Submit for Approval:
  cc-btn cc-btn--outline cc-btn--sm "Submit"
  Keep existing form action and CSRF token
  Only show if draft (keep existing condition)

Delete:
  cc-btn cc-btn--danger cc-btn--sm cc-btn--icon-only
  fas fa-trash, keep existing DELETE form + CSRF + confirm dialog
  Only show if deletable (keep existing condition)

EMPTY STATE: fas fa-calendar-plus, "No events yet. Create your first event."

CONSTRAINTS:
- All action hrefs and form POST actions unchanged
- CSRF tokens on all forms unchanged
- All Jinja2 conditionals for action visibility unchanged
- Filter URL params unchanged
```

---

### PROMPT 10 — Organizer: Event Form (Create/Edit)
**File:** `templates/organizer/event_form.html`

```
CAMPUSCORE REDESIGN — templates/organizer/event_form.html

This is the most complex form in the app.
Open the current template first. List every field name attribute before starting.
Also note: is this used for both create and edit? Check for an `event` variable
that pre-populates values in edit mode.

LAYOUT inside {% block content %}:

PAGE HEADER:
cc-page-title: "Create Event" or "Edit Event: {{ event.title }}" 
  (Jinja2: if event exists use edit title, else create)

Single-column form, max-width 760px, margin: 0 auto

SECTION CARDS (each is cc-card with cc-card__header + cc-card__body):
Arrange into 5 sections:

SECTION 1 — "Basic Information"
cc-card__body display flex flex-direction column gap var(--space-5):
- Event Title: cc-label + cc-input full-width
  value="{{ event.title if event else '' }}"
- Description: cc-label + cc-textarea, min-height 160px, resize vertical
  value="{{ event.description if event else '' }}"
- Category: cc-label + cc-select
  Existing options from current template, keep name attribute unchanged
- Tags: cc-label + cc-input
  placeholder="comma-separated, e.g. coding, hackathon"
  Helper text below (cc-input-hint): "Press enter or use commas to separate tags"

SECTION 2 — "Date & Time"
cc-card__body:
  Grid 3 columns (1fr 1fr 1fr), gap var(--space-4):
  - Event Date (cc-input type="date")
  - Start Time (cc-input type="time")
  - End Time (cc-input type="time")
  Below the grid, full-width:
  - Registration Deadline (cc-input type="datetime-local")
  - cc-input-hint below: "Students cannot register after this deadline"

SECTION 3 — "Venue & Capacity"
cc-card__body:
  Grid 2 columns:
  - Venue: cc-select with existing venue options, OR cc-input if free text
    (check what the current template uses)
  - Max Participants: cc-input type="number" min="1"
  - cc-input-hint: "Recommended: 20–500 for campus events"

SECTION 4 — "Event Image" (only include if image upload exists in current form)
cc-card__body:
  Upload zone:
    border: 2px dashed var(--cc-border-strong)
    border-radius: var(--radius-xl)
    padding: var(--space-10)
    text-align: center
    cursor: pointer
    transition: border-color var(--transition-fast), background var(--transition-fast)
  On hover: border-color var(--cc-crimson), background var(--cc-crimson-muted-2)
  
  Inside zone:
    fas fa-cloud-upload-alt, font-size 32px, color var(--cc-text-muted), mb var(--space-3)
    "Click to upload or drag & drop" — font-weight 500
    "PNG or JPG, max 5MB" — font-size xs, muted
  
  Hidden file input (opacity 0, position absolute, inset 0) triggered by zone click
  Keep existing file input name attribute unchanged
  
  If editing and event.image_url exists:
    Show thumbnail preview (80px height, border-radius md) above the zone
    "Remove image" link below if it exists in current form

SECTION 5 — "Additional Settings" (only if current form has extra fields)
Check current template for any remaining fields.
Wrap them in a cc-card with label "Additional Settings".

STICKY FORM FOOTER:
position sticky, bottom 0, z-index 10
background var(--cc-surface), border-top 1px solid var(--cc-border)
padding var(--space-4) var(--space-8)
Display flex, justify-content flex-end, gap var(--space-3):
- "Cancel" → cc-btn cc-btn--ghost (keep existing href)
- "Save Draft" → cc-btn cc-btn--secondary (keep existing form action)
- "Submit for Approval" → cc-btn cc-btn--primary (keep existing form action)

CONSTRAINTS:
- EVERY field name attribute unchanged — verify one by one against current template
- All form action URLs unchanged
- All pre-population value="{{ event.field if event else '' }}" bindings kept
- Image upload name attribute unchanged
- CSRF token unchanged
- Existing JS for tag input (if any) kept exactly as-is
```

---

### PROMPT 11 — Organizer: Participants & Attendance Portal
**File:** `templates/organizer/participants.html`

```
CAMPUSCORE REDESIGN — templates/organizer/participants.html

This is the most operationally critical page. Organizers use it live during events.
Open the current template. Before writing anything, identify and note:
1. The Socket.IO event listener names (e.g., 'attendance:updated', 'attendance:new')
2. The element IDs updated by Socket.IO (e.g., id="live-count", id="live-rate")
3. The QR scanner initialization code and element IDs
4. The POST form for marking attendance manually
These must all survive the redesign unchanged.

LAYOUT inside {% block content %}:

PAGE HEADER (display flex, justify space-between):
Left: 
  cc-page-title: event title
  cc-page-subtitle: event date + venue (muted, font-size sm)
Right:
  "Mark Event Complete" — cc-btn cc-btn--danger
  Keep existing POST form action and CSRF token

LIVE STATS BAR (cc-grid cc-grid--3, margin-bottom var(--space-6)):
Three cc-stat-cards, reduced padding (no hover animation — this updates live):
  
  Total Registered (cc-stat-card--events):
    Static number from Jinja2
  
  Checked In (cc-stat-card--users):
    Value element must have id="live-count" (Socket.IO writes to this)
    Add green pulsing dot next to "Checked In" label:
      <span style="display:inline-block;width:8px;height:8px;
                   border-radius:50%;background:var(--cc-success);
                   animation:pulse-green 2s infinite;
                   margin-right:var(--space-2);">
    (pulse-green keyframe already exists in components.css)
  
  Attendance Rate (cc-stat-card--registered):
    Value element must have id="live-rate" (Socket.IO writes to this)
    Show as percentage

SEARCH + FILTER BAR (cc-card, compact, margin-bottom var(--space-5)):
Row: cc-search-wrapper (flex 1) + Status tabs (cc-tab-group): All | Present | Absent
Keep existing filter form field names and submit logic.

TWO-COLUMN LAYOUT (3fr 2fr):

LEFT — Participants Table (cc-table-wrapper):
cc-table columns:
  Student: name (font-weight semibold) + reg number (xs, muted) stacked
  Department: font-size sm
  Status badge: 
    cc-badge cc-badge--registered if confirmed
    cc-badge cc-badge--pending if waitlisted
  Attendance:
    cc-badge cc-badge--active "Present" if checked in
    cc-badge cc-badge--cancelled "Absent" if not
  Method: "QR Scan" or "Manual" — cc-badge cc-badge--completed (small)
  Time: check-in timestamp, font-size xs, muted (show dash if not checked in)
  Action:
    If NOT checked in: cc-btn cc-btn--success cc-btn--sm "Mark Present"
      Keep existing POST form action and CSRF token exactly
    If checked in: no button

RIGHT — QR Scanner Panel (cc-card cc-card--elevated):
cc-card__header: "QR Scanner"
  Right: small live indicator dot (green pulsing)

cc-card__body:
  The existing QR scanner HTML goes here exactly as-is.
  Do NOT move, modify, or restructure any QR scanner elements,
  video elements, canvas elements, or scanner initialization scripts.
  Only wrap them in this card structure.

  Below the scanner (keep existing structure):
  Divider: border-top 1px solid var(--cc-border-subtle), margin var(--space-4) 0
  "Or search manually":
  cc-search-wrapper with cc-input for manual lookup
  cc-btn cc-btn--primary full-width "Mark Present"
  Keep existing search/manual attendance form logic unchanged.

CONSTRAINTS:
- id="live-count" and id="live-rate" must remain on their elements exactly
- ALL Socket.IO listeners unchanged — do not touch a single character of the JS
- QR scanner HTML untouched — only its wrapper changes
- Manual attendance POST form action and CSRF unchanged
- Mark Complete POST form action and CSRF unchanged
- Filter form field names unchanged
```

---

### PROMPT 12 — Admin: Users Management
**File:** `templates/admin/users.html`

```
CAMPUSCORE REDESIGN — templates/admin/users.html

Open current template. Note all Jinja2 variables and action URLs.
Open admin/events.html (already redesigned) for the table pattern.

LAYOUT inside {% block content %}:

PAGE HEADER:
cc-page-title: "User Management"
cc-page-subtitle: "Manage student and organiser accounts"
Right: "Add User" — cc-btn cc-btn--primary → keep existing href

STATS ROW (cc-grid cc-grid--3, compact):
cc-stat-card for:
  Total Students (cc-stat-card--users)
  Total Organisers (cc-stat-card--registered)
  Total Admins (cc-stat-card--events)

FILTER BAR (cc-card):
Row: cc-search-wrapper | Role cc-select (All | Student | Organiser | Admin) |
     Status cc-tab-group (Active | Inactive) | Filter cc-btn --secondary
Keep all existing form field names and filter URL params.

USERS TABLE (cc-table-wrapper):
Columns: User | Role | Department | Joined | Status | Events | Actions

User cell:
  Display flex, align-items center, gap var(--space-3):
  Avatar (cc-user-avatar, 36px):
    Student: background var(--cc-info)
    Organiser: background #7C3AED
    Admin: background var(--cc-crimson)
    Initials: first letter of name
  Right of avatar: name (font-weight semibold) + email (xs, muted) stacked

Role: cc-badge
  student → cc-badge background var(--cc-info-bg) color var(--cc-info)
  organiser → background #F5F3FF color #7C3AED
  admin → cc-badge--pending (purple) or cc-badge with crimson

Department: font-size sm, color var(--cc-text-secondary)
Joined: formatted date, font-size sm
Status: cc-badge cc-badge--active or cc-badge--cancelled
Events: registration count, font-weight semibold

Actions (right-aligned, flex gap var(--space-2)):
  View: cc-btn cc-btn--secondary cc-btn--sm cc-btn--icon-only, fas fa-eye
    → keep existing href to user_detail
  Edit: cc-btn cc-btn--secondary cc-btn--sm cc-btn--icon-only, fas fa-pencil
    → keep existing href to user_form
  Disable/Enable: cc-btn cc-btn--danger cc-btn--sm cc-btn--icon-only, fas fa-ban
    Keep existing toggle POST form and CSRF token

EMPTY STATE: fas fa-users, "No users found"

CONSTRAINTS: All hrefs, POST forms, CSRF tokens, Jinja2 variables unchanged.
```

---

### PROMPT 13 — Admin: Announcements Page
**File:** `templates/admin/announcements.html`

```
CAMPUSCORE REDESIGN — templates/admin/announcements.html

Open current template. Note form action, field names, existing announcement list variables.
The Socket.IO broadcast happens server-side on form submit — do not add or change 
any Socket.IO logic.

LAYOUT inside {% block content %}:

PAGE HEADER:
cc-page-title: "Announcements"
cc-page-subtitle: "Broadcast real-time messages to all platform users"

TWO-COLUMN LAYOUT (5fr 7fr):

LEFT — Compose Card (cc-card cc-card--elevated):
cc-card__header: "New Announcement"
cc-card__body:
  Form — keep action, CSRF token, all field names unchanged.

  Message textarea:
  cc-label: "Message"
  cc-textarea: min-height 120px, resize vertical, full-width
  Keep existing name attribute.

  Priority selector:
  cc-label: "Priority"
  Three clickable option cards (replace dropdown if one exists):
  
  Layout: display grid, grid-template-columns 1fr 1fr 1fr, gap var(--space-3)
  Each card:
    padding var(--space-3)
    border-radius var(--radius-lg)
    border 2px solid var(--cc-border)
    cursor pointer
    transition border-color var(--transition-fast), background var(--transition-fast)
    Inside: icon (centered) + label (centered, font-weight 600, font-size sm) + 
            description (font-size xs, muted, centered)
    
    Info card: icon fas fa-info-circle, label "Info", desc "General update"
    Warning card: icon fas fa-exclamation-triangle, label "Warning", desc "Important notice"
    Urgent card: icon fas fa-exclamation-circle, label "Urgent", desc "Immediate attention"
    
    Selected state (add class 'selected' via JS onclick):
      Info selected: border-color var(--cc-info), background var(--cc-info-bg)
      Warning selected: border-color var(--cc-warning), background var(--cc-warning-bg)
      Urgent selected: border-color var(--cc-crimson), background var(--cc-crimson-muted)
  
  Under the visual cards: hidden radio inputs (one per priority value)
  Keep existing radio input name attribute unchanged.
  JS to link cards to radio inputs:
  <script>
  document.querySelectorAll('.priority-card').forEach(card => {
    card.addEventListener('click', () => {
      document.querySelectorAll('.priority-card').forEach(c => 
        c.classList.remove('selected'));
      card.classList.add('selected');
      const val = card.dataset.priority;
      document.querySelector(`input[name="priority"][value="${val}"]`).checked = true;
    });
  });
  // Select info by default
  document.querySelector('.priority-card[data-priority="info"]').click();
  </script>
  
  Submit: cc-btn cc-btn--primary full-width "Broadcast Announcement"
    fas fa-bolt icon before text

RIGHT — History Card (cc-card):
cc-card__header: "Broadcast History" + count badge (cc-badge cc-badge--pending)
cc-card__body: padding 0, max-height 600px, overflow-y auto

For each announcement in list:
  Row: display flex, align-items flex-start, gap var(--space-3)
  Padding: var(--space-4) var(--space-5)
  Border-bottom: 1px solid var(--cc-border-subtle)
  
  Left: 3px wide colored bar (full row height):
    Info=var(--cc-info), Warning=var(--cc-warning), Urgent=var(--cc-crimson)
  
  Center (flex 1):
    Message text: font-weight 500, font-size sm, line-height relaxed
    Footer: "Sent by [name] · [timestamp]" — font-size xs, muted, margin-top 2px
  
  Right: cc-badge cc-badge--[priority]

EMPTY STATE (right column): fas fa-bullhorn, "No announcements sent yet"

CONSTRAINTS:
- Form action URL unchanged
- All field name attributes unchanged
- CSRF token unchanged
- Announcement list Jinja2 variables unchanged
```

---

### PROMPT 14 — Admin: Analytics Page
**File:** `templates/admin/analytics.html`

```
CAMPUSCORE REDESIGN — templates/admin/analytics.html

Open current template. Identify every Chart.js canvas element and its id.
Those canvas elements and ALL Chart.js initialization scripts are untouched.
Only their wrapper HTML changes.

LAYOUT inside {% block content %}:

PAGE HEADER:
cc-page-title: "Platform Analytics" (use font-display class for Playfair Display)
cc-page-subtitle: "Aggregated registration, attendance, and engagement metrics"
Right side: date range form (keep existing fields, update inputs to cc-input)

TOP STATS (cc-grid cc-grid--4):
cc-stat-card for each platform-wide metric in the route:
  Total Events (cc-stat-card--events)
  Total Students (cc-stat-card--users)
  Total Registrations (cc-stat-card--registered)
  Overall Attendance Rate as % (cc-stat-card--certs)
(Adjust variable names to match what the route actually passes)

CHART ROW 1 (cc-grid cc-grid--2):
Each chart wrapped in cc-card:
  cc-card__header: chart title
  cc-card__body: existing <canvas id="..."> goes here unchanged

CHART ROW 2 (cc-grid cc-grid--2) — if more charts exist:
Same wrapping pattern

TOP EVENTS TABLE (full-width cc-card):
cc-card__header: "Top Events by Registrations"
cc-table inside:
  Columns: # | Event Title | Category | Registrations | Attendance Rate | Status

CONSTRAINTS:
- Every canvas id attribute unchanged
- All Chart.js script blocks unchanged — do not move them
- All Jinja2 variables for chart data unchanged
- Date range filter field names unchanged
```

---

### PROMPT 15 — Admin: Event Stats Page
**File:** `templates/admin/event_stats.html`

```
CAMPUSCORE REDESIGN — templates/admin/event_stats.html

Open current template. Same canvas-preservation rules as analytics.html.

LAYOUT inside {% block content %}:

PAGE HEADER:
Back link: "← Back to Events" → existing href, font-size sm, color muted
cc-page-title: event title (Jinja2 variable)
Status badge (cc-badge) next to title

STATS ROW (cc-grid cc-grid--4):
cc-stat-card for: Registered | Attended | Waitlisted | Absent

FUNNEL CARD (full-width cc-card):
cc-card__header: "Registration to Attendance Funnel"
cc-card__body:
  Three steps in a horizontal flex row:
  Each step (flex 1): 
    Large number (2rem, bold), label below, percentage of previous step below that
    Color: Registered=var(--cc-info), Attended=var(--cc-success), 
           Certificate=var(--cc-gold)
  Between steps: fas fa-chevron-right, color muted, flex-shrink 0

CHART ROW (cc-grid cc-grid--2):
Wrap existing canvas elements in cc-cards as per analytics.html pattern.

DEPARTMENT BREAKDOWN CARD (cc-card):
cc-card__header: "Registrations by Department"
For each department:
  Row: dept name (40% width) + count (font-weight 600) + 
       cc-capacity-bar (flex 1, show % of total)
  Border-bottom on each row except last

PARTICIPANTS TABLE (full-width cc-card):
cc-card__header: "All Participants"
Read-only version of the participants table (no attendance action buttons)
Same columns as organizer/participants.html but no "Mark Present" column

CONSTRAINTS:
- All canvas ids unchanged
- All Chart.js scripts unchanged
- All Jinja2 variables unchanged
```

---

### PROMPT 16 — Admin: Attendance Page
**File:** `templates/admin/attendance.html`

```
CAMPUSCORE REDESIGN — templates/admin/attendance.html

Open current template and note all variables and filter field names.

LAYOUT inside {% block content %}:

PAGE HEADER: "Attendance Records"
Subtitle: "Cross-event attendance log"
Right: Export button if it exists (cc-btn cc-btn--secondary, fas fa-download)

FILTER BAR (cc-card):
Row: Event cc-select | Date From cc-input type=date | Date To cc-input type=date |
     Status cc-select (All | Present | Absent) | Filter cc-btn --secondary
Keep all existing field names.

STATS ROW (cc-grid cc-grid--3):
cc-stat-card: Total Records | Present count | Absent count (with % rate)

ATTENDANCE TABLE (cc-table-wrapper):
Columns: Student | Register No. | Event | Date | Status | Method | Checked In By | Time

Status: cc-badge cc-badge--active "Present" or cc-badge cc-badge--cancelled "Absent"
Method: cc-badge (small): "QR Scan" or "Manual"
Time: font-size xs, monospace fallback

EMPTY STATE: fas fa-clipboard-list, "No attendance records found"

CONSTRAINTS: All filter field names and Jinja2 variables unchanged.
```

---

### PROMPT 17 — Admin: Audit Log
**File:** `templates/admin/audit_logs.html`

```
CAMPUSCORE REDESIGN — templates/admin/audit_logs.html

Open current template and note variables.

LAYOUT inside {% block content %}:

PAGE HEADER: "Audit Log"
Subtitle: "Security and administrative action history"
Right: Export button if exists (cc-btn cc-btn--secondary)

FILTER BAR (cc-card):
Action type cc-select | User cc-input search | Date From | Date To | Filter button

AUDIT TABLE (cc-table-wrapper):
Columns: Timestamp | Action | User | Target | Details | IP

Timestamp: font-family monospace, font-size xs, color muted, white-space nowrap

Action badge (cc-badge):
  CREATE: background var(--cc-success-bg), color var(--cc-success)
  UPDATE: background var(--cc-info-bg), color var(--cc-info)
  DELETE: background var(--cc-error-bg), color var(--cc-error)
  LOGIN/LOGOUT: background var(--cc-surface-3), color var(--cc-text-secondary)
  Other: cc-badge--completed

User cell: name (semibold) + role badge stacked

Target: font-size sm, color var(--cc-text-secondary)

Details: max-width 200px, white-space nowrap, overflow hidden, text-overflow ellipsis
  Add title attribute for full text on hover

IP Address: font-family monospace, font-size xs, color muted

Row background on hover for DELETE rows:
  tr[data-action="delete"]:hover { background: var(--cc-error-bg); }
  Add data-action="{{ log.action }}" to each <tr>

EMPTY STATE: fas fa-shield-alt, "No audit records found"

CONSTRAINTS: All Jinja2 variables unchanged.
```

---

### PROMPT 18 — Admin: User Detail Page
**File:** `templates/admin/user_detail.html`

```
CAMPUSCORE REDESIGN — templates/admin/user_detail.html

Open current template. This is an admin-only view of a specific user.

LAYOUT inside {% block content %}:

PAGE HEADER:
"← Back to Users" link (font-size sm, muted) | user.name as cc-page-title
Right: action buttons (Disable Account | Reset Password)
  Keep all existing form actions, CSRF tokens, button types

TWO-COLUMN LAYOUT (2fr 1fr):

LEFT:
Profile card (same hero-band pattern from profile.html — reuse exactly)

Below profile card: "Event History" (cc-card):
cc-card__header: "Event History"
cc-table:
  Columns: Event | Date | Registration | Attendance | Certificate
  Registration: cc-badge by status
  Attendance: cc-badge--active or cc-badge--cancelled
  Certificate: download link or dash

RIGHT:
Account Status card (cc-card):
  Status: cc-badge--active or cc-badge--cancelled (large, prominent)
  Row list: Joined | Last Login | Role | Google OAuth (Yes/No)
  Same info-row pattern as profile.html

Danger Zone card (cc-card):
  cc-card__header: 
    display flex, align-items center, gap var(--space-2)
    fas fa-exclamation-triangle, color var(--cc-error)
    "Danger Zone" text, color var(--cc-error)
  Border: 1px solid var(--cc-error-border)
  cc-card__body: display flex flex-direction column gap var(--space-3)
    "Disable Account" — cc-btn cc-btn--danger full-width (keep existing form)
    "Force Password Reset" — cc-btn cc-btn--secondary full-width (keep existing form)
    "Delete Account" — cc-btn cc-btn--danger full-width 
      (keep existing form + confirm dialog)

CONSTRAINTS: All form actions, CSRF tokens, Jinja2 variables unchanged.
```

---

### PROMPT 19 — Admin: User Form (Create/Edit)
**File:** `templates/admin/user_form.html`

```
CAMPUSCORE REDESIGN — templates/admin/user_form.html

Open current template. Note all field names and which are shown on create vs edit.

LAYOUT inside {% block content %}:

Single centered card, max-width 600px, margin 0 auto:
cc-card cc-card--elevated:
  cc-card__header: 
    "Create User" or "Edit User: {{ user.name if user else '' }}"
  cc-card__body: form content

SECTIONS (visual grouping via margin/label, not nested cards):

Personal Information:
  Full Name (cc-input)
  Email (cc-input type="email")
  Register Number (cc-input)

Academic Details:
  Role (cc-select): Student | Organiser | Admin
  Department (cc-select or cc-input per existing template)
  Year of Study (cc-select: 1st–4th Year, only if role=student — use existing conditional)
  College (cc-input if editable)

Security (create mode only / per existing template):
  Password (cc-input type="password")
  Confirm Password (cc-input type="password")
  OR "Send password reset email" toggle (keep existing checkbox)

cc-card__footer (display flex, justify flex-end, gap var(--space-3)):
  "Cancel" → cc-btn cc-btn--ghost (keep existing href)
  "Save" → cc-btn cc-btn--primary (keep existing submit)

CONSTRAINTS: All field names, form actions, CSRF tokens unchanged.
All create vs edit conditionals (if user / if not user) unchanged.
```

---

### PROMPT 20 — Admin: Students Page
**File:** `templates/admin/students.html`

```
CAMPUSCORE REDESIGN — templates/admin/students.html

Open the current template. Identify if this is:
A) A filtered view of users (role=student only), OR
B) A separate page with different content

If A: Apply the EXACT pattern from Prompt 12 (admin/users.html) with these changes:
  - Title: "Students"
  - Remove the Role filter column and dropdown (all are students)
  - Add "Year of Study" column to the table
  - Add "Register Number" column
  - Keep all other columns and action buttons unchanged

If B: Describe the actual content in a follow-up and I will write a specific prompt.

CONSTRAINTS: All action URLs, CSRF tokens, Jinja2 variables unchanged.
```

---

### PROMPT 21 — Email Templates
**Files:** All 8 in `templates/email/`

```
CAMPUSCORE EMAIL TEMPLATES REDESIGN — All 8 files in one pass

EMAIL CLIENT RULES (strictly enforce, no exceptions):
- Inline styles only — no external CSS, no CSS variables, no class attributes
- Table-based layouts only — no flexbox, no grid (Outlook does not support them)
- Max width 600px
- Font stack: Arial, sans-serif (no Google Fonts)
- Hex values only for colors — no CSS custom properties
- No border-radius above 8px
- No background-image in CSS

BRAND COLORS (hex only, no variables):
  Crimson:   #8B1538
  Gold:      #C9A84C
  Background:#F4F6F9
  Surface:   #FFFFFF
  Text:      #111827
  Muted:     #6B7280
  Success:   #059669
  Border:    #E5E7EB

STEP 1: Redesign base_email.html

Keep the existing {% block %} structure that child templates extend.
Replace the visual HTML with:

<table width="100%" cellpadding="0" cellspacing="0" 
       style="background:#F4F6F9; min-height:100vh;">
  <tr>
    <td align="center" style="padding:40px 16px;">
      <table width="600" cellpadding="0" cellspacing="0"
             style="max-width:600px; background:#FFFFFF; 
                    border-radius:8px; overflow:hidden;">
        
        <!-- Header -->
        <tr>
          <td style="background:#8B1538; padding:20px 32px;">
            <table width="100%" cellpadding="0" cellspacing="0">
              <tr>
                <td>
                  <table cellpadding="0" cellspacing="0">
                    <tr>
                      <td style="background:#FFFFFF; border-radius:6px; 
                                 padding:4px 8px; vertical-align:middle;">
                        <span style="font-size:16px;">🎓</span>
                      </td>
                      <td style="padding-left:8px; vertical-align:middle;">
                        <span style="color:#FFFFFF; font-size:16px; 
                                     font-weight:600; font-family:Arial,sans-serif;">
                          CampusCore
                        </span>
                      </td>
                    </tr>
                  </table>
                </td>
                <td align="right">
                  <span style="color:rgba(255,255,255,0.7); font-size:11px;
                               font-family:Arial,sans-serif;">
                    SIST Portal
                  </span>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- Body block (child templates fill this) -->
        <tr>
          <td style="padding:32px;">
            {% block email_body %}{% endblock %}
          </td>
        </tr>

        <!-- Footer -->
        <tr>
          <td style="background:#F4F6F9; padding:20px 32px;
                     border-top:1px solid #E5E7EB;">
            <p style="color:#9CA3AF; font-size:11px; margin:0; 
                      text-align:center; font-family:Arial,sans-serif;
                      line-height:1.6;">
              This email was sent by CampusCore —<br>
              Sathyabama Institute of Science and Technology<br>
              {% block email_footer %}{% endblock %}
            </p>
          </td>
        </tr>

      </table>
    </td>
  </tr>
</table>

STEP 2: Apply this inline-style email body pattern to each child template:

For event_registration_confirmation.html:
{% block email_body %}
<h2 style="color:#111827;font-size:20px;margin:0 0 8px;
            font-family:Arial,sans-serif;">
  You're registered! 🎉
</h2>
<p style="color:#4B5563;font-size:14px;line-height:1.6;
          margin:0 0 24px;font-family:Arial,sans-serif;">
  Hi {{ student_name }}, your spot at 
  <strong>{{ event_name }}</strong> is confirmed.
</p>
<!-- Event detail box -->
<table width="100%" cellpadding="0" cellspacing="0"
       style="background:#F4F6F9;border-radius:6px;
              border-left:4px solid #8B1538;margin:0 0 24px;">
  <tr>
    <td style="padding:16px 20px;">
      <p style="margin:0 0 8px;font-size:13px;color:#6B7280;
               font-family:Arial,sans-serif;">
        📅 <strong style="color:#111827;">Date:</strong> {{ event_date }}
      </p>
      <p style="margin:0 0 8px;font-size:13px;color:#6B7280;
               font-family:Arial,sans-serif;">
        🕐 <strong style="color:#111827;">Time:</strong> {{ event_time }}
      </p>
      <p style="margin:0;font-size:13px;color:#6B7280;
               font-family:Arial,sans-serif;">
        📍 <strong style="color:#111827;">Venue:</strong> {{ event_venue }}
      </p>
    </td>
  </tr>
</table>
<p style="color:#4B5563;font-size:14px;margin:0 0 24px;
          font-family:Arial,sans-serif;">
  Show your QR code at the venue for attendance verification.
</p>
<!-- CTA button -->
<table cellpadding="0" cellspacing="0">
  <tr>
    <td style="background:#8B1538;border-radius:6px;">
      <a href="{{ event_url if event_url is defined else '#' }}"
         style="color:#FFFFFF;font-size:14px;font-weight:600;
                padding:10px 24px;display:inline-block;
                text-decoration:none;font-family:Arial,sans-serif;">
        View Event Details →
      </a>
    </td>
  </tr>
</table>
{% endblock %}

Apply the SAME inline-style approach to the remaining 6 child templates.
Adapt the content per template purpose:

new_event_notification.html → "New event available" + event card + Register CTA
event_update_notification.html → "Event updated" + what changed + View CTA
new_user_notification.html → "Welcome" onboarding + getting started steps
password_reset_notification.html → "Reset your password" + Reset Link CTA (gold button)
force_password_reset.html → "Security: Password reset required" (warning tone, 
  use #D97706 border on event box instead of crimson)
account_update_notification.html → "Account updated" confirmation, no CTA needed

CONSTRAINTS FOR ALL EMAIL TEMPLATES:
- Every Jinja2 variable name unchanged ({{ student_name }}, {{ event_name }}, etc.)
- Every {% block %} structure that extends base_email.html unchanged
- Every {% if %} conditional unchanged
- CSRF tokens: email templates do not have forms, so this does not apply
- Keep any existing url_for() or variable-based URL references
```

---

## Step 3 — After Each Prompt: Verification Checklist

Run this in Antigravity immediately after generating each page:

```
CAMPUSCORE POST-GENERATION VERIFICATION — [template name]

I just redesigned [template name]. Before I close this session:

1. Open the newly generated template and the original template side by side

2. FIELD AUDIT — verify these match exactly between old and new:
   - Every <input name="..."> attribute
   - Every <select name="..."> attribute  
   - Every <textarea name="..."> attribute
   - Every <form action="..."> attribute
   - Every CSRF token input
   - Every <a href="..."> that links to a Flask route

3. VARIABLE AUDIT — verify every {{ variable }} in the new template 
   exists in the route's render_template() call in app_legacy.py or 
   the blueprint file

4. SCRIPT AUDIT — verify no <script> blocks were removed or modified
   (especially Socket.IO listeners and QR scanner code)

5. Run the app and navigate to this page as the appropriate role.
   Confirm it renders without a Jinja2 TemplateError or Python traceback.

Report every discrepancy found. Fix only discrepancies — do not refactor anything else.
```

---

## Step 4 — Final Checklist

Run this after all 21 prompts are complete:

```
FUNCTIONALITY
□ All 3 roles complete their full workflow end-to-end
□ Event lifecycle: Create → Approve → Register → Attend → Certificate
□ Socket.IO: Live attendance counter updates on participants page
□ Socket.IO: Announcement banner appears on student/organiser pages  
□ QR scanner initialises on participants page
□ Certificate PDF generates and downloads
□ Email sends on registration (check Node.js microservice logs)

DESIGN CONSISTENCY
□ No page still shows the old maroon/cream Bootstrap look
□ All flash messages use cc-flash components
□ Sidebar active state (gold left bar) works on every page
□ Dark mode (data-theme="dark") works on every new page
□ All buttons use cc-btn classes

SECURITY (verify the 10 original audit fixes survived)
□ Single CSRF token on login page
□ Remember-me unchecked by default
□ novalidate removed from login form
□ Dark mode uses fetch with X-CSRFToken (not sendBeacon)
□ CSRF token present on organiser delete form

MOBILE
□ All pages responsive at 375px
□ Sidebar drawer works on all pages
□ Participants page QR scanner usable on mobile

ACCESSIBILITY
□ Skip link in base.html on every page
□ All icon-only buttons have aria-label
□ Page title format: "[Page] — CampusCore SIST" on every template
```
