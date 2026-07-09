import http.server
import socketserver
import json
import sqlite3
import csv
import io
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import urllib.parse
import sys
from datetime import datetime

def get_local_now():
    """Returns the current local timestamp string (Italian time)."""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# ==========================================================
# CONFIGURATION & SMTP EMAIL SETTINGS
# ==========================================================
PORT = 8000

# To send real emails:
# 1. Set SMTP_ENABLED = True
# 2. Update the SMTP_SERVER, SMTP_PORT, SMTP_EMAIL, and SMTP_PASSWORD.
# (For services like Gmail, you must generate an "App Password" in your Google account security settings).
SMTP_ENABLED = False
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_EMAIL = "your-conference-email@gmail.com"
SMTP_PASSWORD = "your-app-password-here"
SMTP_SENDER_NAME = "Sapienza Nano & Tech Secretary"

# ==========================================================
# DATABASE INITIALIZATION & CSV SYNC
# ==========================================================
DB_FILE = "registrations.db"
CSV_FILE = "Sapienza Conference 2026 Registration - Risposte del modulo 1.csv"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            role TEXT NOT NULL,
            workshop TEXT DEFAULT NULL,
            registered_at TIMESTAMP DEFAULT (datetime('now', 'localtime'))
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            affiliation TEXT NOT NULL,
            topic TEXT NOT NULL,
            title TEXT NOT NULL,
            abstract TEXT NOT NULL,
            pass_id TEXT NOT NULL,
            submitted_at TIMESTAMP DEFAULT (datetime('now', 'localtime'))
        )
    """)
    conn.commit()
    conn.close()
    print("SQLite Database initialized successfully (registrations and posters tables).")
    sync_db_and_csv()

def sync_db_and_csv():
    """
    Bi-directional synchronization between SQLite registrations table and the CSV / Excel files.
    If rows were deleted or added in CSV, updates SQLite. If updated in SQLite, rewrites CSV and Excel.
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email, role, workshop, registered_at FROM registrations ORDER BY id ASC")
        db_rows = cursor.fetchall()
        
        # Check if CSV exists and has entries that might differ or if we should sync
        csv_rows = []
        if os.path.exists(CSV_FILE):
            try:
                with open(CSV_FILE, mode='r', encoding='utf-8-sig') as f:
                    reader = csv.reader(f)
                    rows = list(reader)
                    if len(rows) > 1:
                        csv_rows = rows[1:]
            except Exception as e:
                pass
                
        # Write exact db_rows to CSV file to ensure perfect consistency
        with open(CSV_FILE, mode='w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Informazioni cronologiche", "Full Name", "Email Address", "Academic Status / Role", "Day 2 Laboratory Workshop", "Session Attending"])
            for r in db_rows:
                ws_name = r[4] if r[4] else "None (Plenary Only)"
                writer.writerow([r[5], r[1], r[2], r[3], ws_name, "All Plenary & Lab Sessions"])
                
        conn.close()
        
        # Also regenerate master workbook if openpyxl available
        try:
            import generate_workbook
            generate_workbook.create_conference_workbook()
        except Exception:
            pass
    except Exception as e:
        print(f"Sync error: {e}")

# ==========================================================
# EMAIL HELPER DISPATCHER
# ==========================================================
def send_email(email_type, recipient_email, recipient_name, details):
    """
    Sends registration confirmation emails.
    If SMTP_ENABLED is False, it logs the complete email content to the console.
    """
    subject = ""
    html_content = ""
    
    if email_type == "conference":
        subject = "Sapienza Conference 2026 | Conference Pass Confirmed"
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f3f4f6; padding: 20px; color: #1f2937;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #070b14; border: 1px solid #00f0ff; border-radius: 12px; padding: 30px; color: #f3f4f6; box-shadow: 0 4px 10px rgba(0,0,0,0.3);">
                <div style="text-align: center; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 20px; margin-bottom: 20px;">
                    <span style="font-size: 24px; font-weight: bold; color: #00f0ff; letter-spacing: 1px;">SAPIENZA NANO & TECH</span>
                    <div style="font-size: 12px; color: #9ca3af; margin-top: 5px;"><a href="https://ssas.web.uniroma1.it/" target="_blank" style="color: #00f0ff; text-decoration: underline;">Sapienza School of Advanced Studies (SSAS)</a> • Rome 2026</div>
                </div>
                
                <h2 style="color: #ffffff; margin-bottom: 15px;">Registration Confirmed!</h2>
                <p>Dear <strong>{recipient_name}</strong>,</p>
                <p>We are pleased to confirm your registration for the <strong>Sapienza Conference on Nanotechnology, Materials Science & Advanced Engineering</strong>, taking place on <strong>September 17–18, 2026</strong> in Rome.</p>
                
                <div style="background-color: rgba(255,255,255,0.05); border-left: 4px solid #00f0ff; padding: 15px; border-radius: 4px; margin: 20px 0;">
                    <div style="font-size: 12px; color: #00f0ff; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px;">Your Conference Pass</div>
                    <div style="font-size: 18px; font-weight: bold; color: #ffffff;">{recipient_name}</div>
                    <div style="font-size: 14px; color: #9ca3af; margin-top: 2px;">Role: {details.get('role')}</div>
                    <div style="font-size: 14px; color: #9ca3af; margin-top: 2px;">Email: {recipient_email}</div>
                    <div style="font-size: 12px; color: #ff5e7e; margin-top: 8px; font-style: italic;">Admission is free. Please present this email or pass at the check-in desk.</div>
                </div>
                
                <h3 style="color: #ffffff; margin-top: 25px;">Event Location</h3>
                <p style="margin-bottom: 5px;"><strong>Sapienza Università di Roma, Aula Amaldi</strong></p>
                <p style="margin-top: 0; color: #9ca3af; font-size: 14px;">Piazzale Aldo Moro 5, 00185 Rome, Italy</p>
                
                <div style="margin-top: 30px; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 20px; font-size: 13px; color: #9ca3af;">
                    <p style="margin-bottom: 8px;"><strong>Interested in hands-on workshops?</strong></p>
                    <p style="margin-top: 0;">Day 2 afternoon features parallel laboratory training. If you haven't reserved your lab seat yet, you can sign up at: <a href="http://localhost:8000/workshops.html?name={urllib.parse.quote(recipient_name)}&email={urllib.parse.quote(recipient_email)}&role={urllib.parse.quote(details.get('role'))}" style="color: #00f0ff; text-decoration: underline;">Reserve Lab Seat</a></p>
                </div>
                
                <div style="text-align: center; margin-top: 30px; font-size: 11px; color: #6b7280; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 15px;">
                    This is an automated confirmation email. For inquiries, contact the Organizing Secretary at secretary@uniroma1.it.
                </div>
            </div>
        </body>
        </html>
        """
        
    elif email_type == "workshop":
        ws_name = details.get('workshop_name', 'Selected Workshop')
        ws_leader = details.get('workshop_leader', '')
        ws_loc = details.get('workshop_location', 'Sapienza Campus')
        subject = f"Sapienza Conference 2026 | Workshop Seat Reserved - {ws_name}"
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f3f4f6; padding: 20px; color: #1f2937;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #070b14; border: 1px solid #6366f1; border-radius: 12px; padding: 30px; color: #f3f4f6; box-shadow: 0 4px 10px rgba(0,0,0,0.3);">
                <div style="text-align: center; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 20px; margin-bottom: 20px;">
                    <span style="font-size: 24px; font-weight: bold; color: #6366f1; letter-spacing: 1px;">SAPIENZA NANO & TECH</span>
                    <div style="font-size: 12px; color: #9ca3af; margin-top: 5px;"><a href="https://ssas.web.uniroma1.it/" target="_blank" style="color: #6366f1; text-decoration: underline;">Sapienza School of Advanced Studies (SSAS)</a> • Rome 2026</div>
                </div>
                
                <h2 style="color: #ffffff; margin-bottom: 15px;">Laboratory Seat Confirmed!</h2>
                <p>Dear <strong>{recipient_name}</strong>,</p>
                <p>Your seat has been successfully reserved for the hands-on laboratory session during the Sapienza Conference.</p>
                
                <div style="background-color: rgba(255,255,255,0.05); border-left: 4px solid #6366f1; padding: 20px; border-radius: 6px; margin: 20px 0;">
                    <div style="font-size: 11px; color: #6366f1; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 6px;">Laboratory Admission Pass</div>
                    <div style="font-size: 16px; font-weight: bold; color: #ffffff; margin-bottom: 10px;">{ws_name}</div>
                    <div style="font-size: 13px; color: #e5e7eb; margin-bottom: 3px;"><strong>Leader:</strong> {ws_leader}</div>
                    <div style="font-size: 13px; color: #e5e7eb; margin-bottom: 3px;"><strong>Time:</strong> Day 2, Sept 18, 2026, 15:00 - 18:00</div>
                    <div style="font-size: 13px; color: #9ca3af; margin-top: 10px; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 10px;">
                        <strong>Venue:</strong> {ws_loc}
                    </div>
                </div>
                
                <p style="font-size: 14px; color: #e5e7eb; margin-top: 20px;"><strong>Important Guidelines:</strong></p>
                <ul style="font-size: 13px; color: #9ca3af; padding-left: 20px; line-height: 1.6;">
                    <li>Please arrive 10 minutes prior to the workshop start time (14:50).</li>
                    <li>Ensure you bring proper identification matching your conference registration pass.</li>
                    <li>If you cannot attend, please release your seat from your profile or contact us so others on the waiting list can join.</li>
                </ul>
                
                <div style="text-align: center; margin-top: 30px; font-size: 11px; color: #6b7280; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 15px;">
                    This is an automated confirmation email. For inquiries, contact the Organizing Secretary at secretary@uniroma1.it.
                </div>
            </div>
        </body>
        </html>
        """

    if not SMTP_ENABLED:
        print(f"\n[EMAIL SIMULATION] SMTP is disabled. Email that would be sent to {recipient_email}:")
        print(f"Subject: {subject}")
        print(f"Recipient Name: {recipient_name}")
        print(f"Details: {details}")
        print("-" * 50)
        return True

    # Real SMTP email dispatch
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{SMTP_SENDER_NAME} <{SMTP_EMAIL}>"
        msg["To"] = recipient_email
        
        # Attach HTML content
        part = MIMEText(html_content, "html")
        msg.attach(part)
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.sendmail(SMTP_EMAIL, recipient_email, msg.as_string())
        server.quit()
        print(f"Real confirmation email sent successfully to {recipient_email}.")
        return True
    except Exception as e:
        print(f"ERROR: Failed to send confirmation email to {recipient_email}: {e}", file=sys.stderr)
        return False

# ==========================================================
# HTTP REQUEST HANDLER
# ==========================================================
class ConferenceHandler(http.server.BaseHTTPRequestHandler):
    
    def log_message(self, format, *args):
        # Override to prevent spamming the console with standard GET logs
        pass

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        
        # Serve API registrations
        if path == "/api/registrations":
            self.send_json_response(200, self.get_all_registrations())
            return
            
        # Serve API workshop counts
        if path == "/api/workshop-counts":
            self.send_json_response(200, self.get_workshop_counts())
            return
            
        # Serve API posters
        if path == "/api/posters":
            self.send_json_response(200, self.get_all_posters())
            return
            
        # Serve Excel/CSV exports
        if path == "/api/export-excel":
            sync_db_and_csv()
            self.handle_export_excel()
            return
        if path == "/api/export-posters":
            self.handle_export_posters()
            return
            
        # Serve static files and HTML pages
        if path == "/" or path == "/index.html":
            self.serve_static_file("index.html")
            return
            
        # Strip leading slash to serve requested static file safely
        rel_path = path.lstrip('/')
        if os.path.exists(rel_path) and os.path.isfile(rel_path):
            self.serve_static_file(rel_path)
            return
            
        # Default 404 handler
        self.send_error_response(404, "File not found.")

    def do_POST(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        
        # Get content length and parse JSON body
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        try:
            body = json.loads(post_data) if post_data else {}
        except json.JSONDecodeError:
            self.send_json_response(400, {"success": False, "error": "Invalid JSON format"})
            return

        if path == "/api/register":
            self.handle_register_conference(body)
            sync_db_and_csv()
        elif path == "/api/register-workshop":
            self.handle_register_workshop(body)
            sync_db_and_csv()
        elif path == "/api/registrations/add":
            self.handle_add_registrant_manual(body)
            sync_db_and_csv()
        elif path == "/api/registrations/delete":
            self.handle_delete_registrant(body)
            sync_db_and_csv()
        elif path == "/api/posters/submit":
            self.handle_submit_poster(body)
        elif path == "/api/posters/delete":
            self.handle_delete_poster(body)
        else:
            self.send_error_response(404, "Endpoint not found.")

    # ==========================================================
    # API ENDPOINT CONTROLLERS
    # ==========================================================
    def handle_register_conference(self, data):
        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        role = data.get("role", "").strip()
        
        if not name or not email or not role:
            self.send_json_response(400, {"success": False, "error": "Missing required fields."})
            return
            
        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            
            # Upsert logic (insert or update role/name, preserve workshop if exists)
            cursor.execute("SELECT id, workshop FROM registrations WHERE email = ?", (email,))
            existing = cursor.fetchone()
            
            if existing:
                cursor.execute(
                    "UPDATE registrations SET name = ?, role = ?, registered_at = ? WHERE email = ?", 
                    (name, role, get_local_now(), email)
                )
                conn.commit()
                print(f"Updated attendee: {name} ({email})")
            else:
                cursor.execute(
                    "INSERT INTO registrations (name, email, role, registered_at) VALUES (?, ?, ?, ?)",
                    (name, email, role, get_local_now())
                )
                conn.commit()
                print(f"Registered new attendee: {name} ({email})")
                
            conn.close()
            
            # Send confirmation email
            send_email("conference", email, name, {"role": role})
            
            self.send_json_response(200, {"success": True, "message": "Conference registration succeeded."})
        except Exception as e:
            self.send_json_response(500, {"success": False, "error": str(e)})

    def handle_register_workshop(self, data):
        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        role = data.get("role", "").strip()
        workshop = data.get("workshop", "").strip()
        
        if not name or not email or not role or not workshop:
            self.send_json_response(400, {"success": False, "error": "Missing required fields."})
            return
            
        # Workshop visual names data
        ws_details_map = {
            'afm': ('Atomic Force Microscopy (AFM)', 'Ernesto Placidi (Sapienza)', 'AFM Lab, Marconi Physics Building, Sapienza'),
            'nanomedicine': ('Nanomedicine Experience', 'M. Gioia Fabiano & Eleonora D’Intino', 'Formulation Lab, Drug Technologies Dept, Sapienza'),
            'quantum-well': ('Absorption in Quantum Well', 'Leonetta Baldassarre (Sapienza)', 'Infrared Spectroscopy Facility, Fermi Building, Sapienza'),
            'nanowires': ('Semiconductor Nanowires', 'Marta De Luca (Sapienza)', 'Micro-Raman Lab, Physics Department, Sapienza'),
            'heritage-lab': ('HERITAGE-LAB Nanotech', 'Maria Laura Santarelli (Sapienza)', 'Cultural Heritage Lab, Chemical Engineering, Sapienza'),
            'photonics': ('Light and Photonics', 'Marco Felici (Sapienza)', 'Integrated Photonics Lab, Physics Department, Sapienza'),
            'computational-plasmonics': ('Computational Plasmonics', 'Tommaso Giovannini (Tor Vergata)', 'Scientific Computing Lab, Physics Dept, Sapienza')
        }
        
        ws_details = ws_details_map.get(workshop.lower(), (workshop, "", "Sapienza Laboratories"))
        ws_name, ws_leader, ws_loc = ws_details
            
        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            
            cursor.execute("SELECT id FROM registrations WHERE email = ?", (email,))
            existing = cursor.fetchone()
            
            if existing:
                cursor.execute(
                    "UPDATE registrations SET name = ?, role = ?, workshop = ?, registered_at = ? WHERE email = ?",
                    (name, role, workshop, get_local_now(), email)
                )
                conn.commit()
                print(f"Updated attendee workshop: {name} -> {workshop}")
            else:
                cursor.execute(
                    "INSERT INTO registrations (name, email, role, workshop, registered_at) VALUES (?, ?, ?, ?, ?)",
                    (name, email, role, workshop, get_local_now())
                )
                conn.commit()
                print(f"Registered new attendee directly into workshop: {name} -> {workshop}")
                
            conn.close()
            
            # Send confirmation email
            send_email("workshop", email, name, {
                "role": role, 
                "workshop_name": ws_name,
                "workshop_leader": ws_leader,
                "workshop_location": ws_loc
            })
            
            self.send_json_response(200, {"success": True, "message": "Workshop reservation succeeded."})
        except Exception as e:
            self.send_json_response(500, {"success": False, "error": str(e)})

    def handle_add_registrant_manual(self, data):
        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        role = data.get("role", "").strip()
        workshop = data.get("workshop", "").strip() or None
        
        if not name or not email or not role:
            self.send_json_response(400, {"success": False, "error": "Missing required fields."})
            return
            
        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO registrations (name, email, role, workshop, registered_at) VALUES (?, ?, ?, ?, ?)"
                "ON CONFLICT(email) DO UPDATE SET name=excluded.name, role=excluded.role, workshop=excluded.workshop, registered_at=excluded.registered_at",
                (name, email, role, workshop, get_local_now())
            )
            conn.commit()
            conn.close()
            print(f"Admin manually added/updated registrant: {name} ({email})")
            self.send_json_response(200, {"success": True, "message": "Attendee registered successfully."})
        except Exception as e:
            self.send_json_response(500, {"success": False, "error": str(e)})

    def handle_delete_registrant(self, data):
        email = data.get("email", "").strip()
        if not email:
            self.send_json_response(400, {"success": False, "error": "Missing email parameter."})
            return
            
        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM registrations WHERE email = ?", (email,))
            conn.commit()
            conn.close()
            sync_db_and_csv()
            print(f"Admin deleted registrant: {email}")
            self.send_json_response(200, {"success": True, "message": "Attendee removed successfully."})
        except Exception as e:
            self.send_json_response(500, {"success": False, "error": str(e)})

    def get_all_registrations(self):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT name, email, role, workshop, registered_at FROM registrations ORDER BY registered_at DESC")
        rows = cursor.fetchall()
        conn.close()
        
        result = []
        for r in rows:
            result.append({
                "name": r[0],
                "email": r[1],
                "role": r[2],
                "workshop": r[3] if r[3] else "None (Plenary Only)",
                "registered_at": r[4]
            })
        return result

    def get_workshop_counts(self):
        """
        Returns exact counts of reserved seats for each laboratory workshop.
        """
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT workshop, COUNT(*) FROM registrations WHERE workshop IS NOT NULL AND workshop != '' AND workshop != 'None (Plenary Only)' GROUP BY workshop")
        rows = cursor.fetchall()
        conn.close()
        
        counts = {
            'afm': 0, 'nanomedicine': 0, 'quantum-well': 0,
            'nanowires': 0, 'heritage-lab': 0, 'photonics': 0,
            'computational-plasmonics': 0
        }
        
        mapping = {
            'Atomic Force Microscopy': 'afm',
            'Nanomedicine': 'nanomedicine',
            'Quantum Well': 'quantum-well',
            'Nanowires': 'nanowires',
            'HERITAGE': 'heritage-lab',
            'Photonics': 'photonics',
            'Computational': 'computational-plasmonics'
        }
        
        for ws_name, cnt in rows:
            for keyword, key in mapping.items():
                if keyword.lower() in ws_name.lower():
                    counts[key] += cnt
                    break
        return counts

    def handle_submit_poster(self, data):
        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        affiliation = data.get("affiliation", "").strip()
        topic = data.get("topic", "").strip()
        title = data.get("title", "").strip()
        abstract = data.get("abstract", "").strip()
        pass_id = data.get("pass_id", "").strip() or "PSTR-2026-X"
        
        if not name or not email or not title or not abstract:
            self.send_json_response(400, {"success": False, "error": "Missing required poster fields."})
            return
            
        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO posters (name, email, affiliation, topic, title, abstract, pass_id, submitted_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, email, affiliation, topic, title, abstract, pass_id, get_local_now()))
            conn.commit()
            conn.close()
            print(f"New poster submitted: {title} by {name} ({email})")
            self.send_json_response(200, {"success": True, "message": "Poster submitted successfully."})
        except Exception as e:
            self.send_json_response(500, {"success": False, "error": str(e)})

    def get_all_posters(self):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email, affiliation, topic, title, abstract, pass_id, submitted_at FROM posters ORDER BY submitted_at DESC")
        rows = cursor.fetchall()
        conn.close()
        
        result = []
        for r in rows:
            result.append({
                "id": r[0],
                "name": r[1],
                "email": r[2],
                "affiliation": r[3],
                "topic": r[4],
                "title": r[5],
                "abstract": r[6],
                "pass_id": r[7],
                "submitted_at": r[8]
            })
        return result

    def handle_delete_poster(self, data):
        poster_id = data.get("id")
        email = data.get("email", "").strip()
        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            if poster_id:
                cursor.execute("DELETE FROM posters WHERE id = ?", (poster_id,))
            elif email:
                cursor.execute("DELETE FROM posters WHERE email = ?", (email,))
            conn.commit()
            conn.close()
            self.send_json_response(200, {"success": True, "message": "Poster deleted successfully."})
        except Exception as e:
            self.send_json_response(500, {"success": False, "error": str(e)})

    def handle_export_posters(self):
        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, email, affiliation, topic, title, abstract, pass_id, submitted_at FROM posters ORDER BY id ASC")
            rows = cursor.fetchall()
            conn.close()

            output = io.StringIO()
            output.write('\ufeff')
            writer = csv.writer(output)
            writer.writerow(["Poster ID", "Candidate Name", "Email Address", "Affiliation", "Research Topic", "Poster Title", "Abstract Content", "Pass ID", "Submission Date"])
            for r in rows:
                writer.writerow(list(r))

            csv_data = output.getvalue().encode('utf-8')
            output.close()

            self.send_response(200)
            self.send_header('Content-Type', 'text/csv; charset=utf-8')
            self.send_header('Content-Disposition', 'attachment; filename=conference_poster_submissions_2026.csv')
            self.send_header('Content-Length', len(csv_data))
            self.end_headers()
            self.wfile.write(csv_data)
        except Exception as e:
            self.send_json_response(500, {"success": False, "error": f"Failed to export posters: {e}"})

    def handle_export_excel(self):
        """
        Queries all rows and sends them as a downloadable CSV spreadsheet
        compatible with Excel.
        """
        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, email, role, workshop, registered_at FROM registrations ORDER BY id ASC")
            rows = cursor.fetchall()
            conn.close()

            # Output string buffer for CSV
            output = io.StringIO()
            # Excel sometimes needs BOM (Byte Order Mark) to correctly read UTF-8 columns
            output.write('\ufeff')
            
            writer = csv.writer(output)
            # Write columns headers
            writer.writerow(["Attendee ID", "Full Name", "Email Address", "Academic Status / Role", "Day 2 Workshop", "Registration Date"])
            
            # Write row data
            for r in rows:
                ws_name = r[4] if r[4] else "None (Plenary Only)"
                writer.writerow([r[0], r[1], r[2], r[3], ws_name, r[5]])

            csv_data = output.getvalue().encode('utf-8')
            output.close()

            # Send headers
            self.send_response(200)
            self.send_header('Content-Type', 'text/csv; charset=utf-8')
            self.send_header('Content-Disposition', 'attachment; filename=conference_registrations_2026.csv')
            self.send_header('Content-Length', len(csv_data))
            self.end_headers()
            self.wfile.write(csv_data)
        except Exception as e:
            self.send_json_response(500, {"success": False, "error": f"Failed to export: {e}"})

    # ==========================================================
    # STATIC FILE SERVER HELPERS
    # ==========================================================
    def serve_static_file(self, filename):
        """
        Reads a local file and outputs it with appropriate Content-Type.
        Supports binary (images, xlsx, pdf) and text (html, css, js, csv, json).
        """
        if not os.path.exists(filename):
            self.send_error_response(404, f"File {filename} not found.")
            return

        ext = os.path.splitext(filename)[1].lower()
        content_types = {
            '.html': 'text/html; charset=utf-8',
            '.css': 'text/css; charset=utf-8',
            '.js': 'application/javascript; charset=utf-8',
            '.json': 'application/json; charset=utf-8',
            '.csv': 'text/csv; charset=utf-8',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.svg': 'image/svg+xml',
            '.gif': 'image/gif',
            '.ico': 'image/x-icon',
            '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            '.pdf': 'application/pdf'
        }
        content_type = content_types.get(ext, 'application/octet-stream')
        is_binary = ext in ['.png', '.jpg', '.jpeg', '.gif', '.ico', '.xlsx', '.pdf']

        try:
            mode = 'rb' if is_binary else 'r'
            encoding = None if is_binary else 'utf-8'
            with open(filename, mode=mode, encoding=encoding) as f:
                content = f.read()
            
            data = content if is_binary else content.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', len(data))
            self.end_headers()
            self.wfile.write(data)
        except Exception as e:
            self.send_error_response(500, f"Error reading file: {e}")

    # ==========================================================
    # SYSTEM RESPONSES HELPERS
    # ==========================================================
    def send_json_response(self, status, payload):
        response_data = json.dumps(payload).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(response_data))
        self.end_headers()
        self.wfile.write(response_data)

    def send_error_response(self, status, message):
        self.send_json_response(status, {"success": False, "error": message})

# ==========================================================
# MAIN INITIALIZER ENTRY POINT
# ==========================================================
if __name__ == "__main__":
    init_db()
    handler = ConferenceHandler
    
    # Enable threading / address reuse
    socketserver.TCPServer.allow_reuse_address = True
    
    print(f"Starting server on http://localhost:{PORT} ...")
    print("Use Ctrl+C to terminate.")
    
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
            sys.exit(0)
