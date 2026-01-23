import sys, os, threading, subprocess, json, pyttsx3, psutil, time
from PyQt6.QtWidgets import (QMainWindow, QApplication, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QTextEdit, QLineEdit, QPushButton, 
                             QStackedWidget, QFrame, QMessageBox)
from PyQt6.QtCore import QTimer, Qt, QMetaObject, Q_ARG
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from OpenGL.GL import *
from OpenGL.GLU import *

# --- [1. TACTICAL HUD] ---
class SimpleGlobe(QOpenGLWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.rot = 0; self.scan_mode = False
        self.timer = QTimer(self); self.timer.timeout.connect(self.update); self.timer.start(16)
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT); glLoadIdentity()
        glTranslatef(0, 0, -10); glRotatef(self.rot, 0, 1, 0); glRotatef(25, 1, 0, 0)
        self.rot += 0.8 if not self.scan_mode else 10.0
        color = (1, 0, 0.5) if self.scan_mode else (0.0, 1.0, 0.8)
        glColor4f(color[0], color[1], color[2], 0.2)
        q = gluNewQuadric(); gluQuadricDrawStyle(q, GLU_LINE); gluSphere(q, 4, 24, 24)

# --- [2. THE ELITE KERNEL] ---
class SentinelElite(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SENTINEL_ELITE_EXECUTIVE")
        self.setStyleSheet("background:#000; color:#00f2ff; font-family: 'Consolas';")
        self.db_path = "vault.json"
        self.creds = self.load_credentials()
        
        self.arsenal = {
            "MAXPHISHER": ["https://github.com/KasRoudra/MaxPhisher.git", "magenta"],
            "SEEKER": ["https://github.com/thewhiteh4t/seeker.git", "orange"],
            "SHERLOCK": ["https://github.com/sherlock-project/sherlock.git", "yellow"]
        }

        self.ask_display_mode()
        self.main_stack = QStackedWidget(); self.setCentralWidget(self.main_stack)
        self.init_login_ui()
        self.init_update_ui() 
        self.init_main_os_ui()

    def load_credentials(self):
        if not os.path.exists(self.db_path):
            with open(self.db_path, 'w') as f: json.dump({"user": "admin", "pass": "1234"}, f)
        with open(self.db_path, 'r') as f: return json.load(f)

    def ask_display_mode(self):
        msg = QMessageBox(); msg.setWindowTitle("BOOT_PROTOCOL")
        msg.setText("INITIATE ELITE_HUD FULLSCREEN?")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if msg.exec() == QMessageBox.StandardButton.Yes: self.showFullScreen()
        else: self.resize(1366, 768); self.show()

    def type_text(self, message):
        self.console.clear()
        def effect():
            current = ""
            for char in message:
                current += char
                QMetaObject.invokeMethod(self.console, "setPlainText", Qt.ConnectionType.QueuedConnection, Q_ARG(str, current))
                time.sleep(0.01)
        threading.Thread(target=effect, daemon=True).start()

    # --- DEPLOY & EXECUTE LOGIC ---
    def deploy_tool(self, url, custom_name=None):
        folder = custom_name if custom_name else url.split("/")[-1].replace(".git", "")
        if os.path.exists(folder):
            self.type_text(f"[!] {folder.upper()} ALREADY DEPLOYED.\nType 'run {folder}' to execute.")
        else:
            self.type_text(f"[+] INJECTING REPOSITORY: {url}...")
            threading.Thread(target=self.run_full_install, args=(url, folder), daemon=True).start()

    def run_full_install(self, url, folder):
        try:
            subprocess.run(["git", "clone", url, folder], check=True)
            req_path = os.path.join(folder, "requirements.txt")
            if os.path.exists(req_path):
                subprocess.run([sys.executable, "-m", "pip", "install", "-r", req_path], check=True)
            QMetaObject.invokeMethod(self.console, "append", Qt.ConnectionType.QueuedConnection, 
                                     Q_ARG(str, f"\n[SUCCESS] Deployment Finished.\nUse 'run {folder}' to start."))
        except Exception as e:
            QMetaObject.invokeMethod(self.console, "append", Qt.ConnectionType.QueuedConnection, Q_ARG(str, f"\n[FATAL] Error: {str(e)}"))

    def execute_tool(self, folder):
        # Look for common entry points
        entry_points = ["setup.py", "main.py", "run.py", f"{folder}.py"]
        found = False
        for file in entry_points:
            path = os.path.join(folder, file)
            if os.path.exists(path):
                self.type_text(f"[>] EXECUTING: {path}...\nOpening external terminal shell.")
                subprocess.Popen([sys.executable, path], creationflags=subprocess.CREATE_NEW_CONSOLE)
                found = True
                break
        if not found:
            self.type_text(f"[!] ERROR: No entry point found in {folder}.\nOpen directory manually to inspect.")

    def init_login_ui(self):
        page = QWidget(); lay = QVBoxLayout(page); lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card = QFrame(); card.setFixedSize(450, 350); card.setStyleSheet("border:2px solid #00f2ff; background:#050505; border-radius:20px;")
        cl = QVBoxLayout(card); cl.addWidget(QLabel("ELITE_ACCESS_ONLY"), alignment=Qt.AlignmentFlag.AlignCenter)
        self.u_in = QLineEdit(); self.p_in = QLineEdit(); self.p_in.setEchoMode(QLineEdit.EchoMode.Password)
        style = "background:#000; color:#00f2ff; border:1px solid #111; padding:12px; margin:5px;"
        for i in [self.u_in, self.p_in]: i.setStyleSheet(style)
        btn = QPushButton("AUTHENTICATE"); btn.clicked.connect(self.check_auth)
        btn.setStyleSheet("background:#00f2ff; color:#000; font-weight:bold; padding:15px;")
        cl.addWidget(self.u_in); cl.addWidget(self.p_in); cl.addWidget(btn)
        lay.addWidget(card); self.main_stack.addWidget(page)

    def init_update_ui(self):
        page = QWidget(); lay = QVBoxLayout(page); lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        box = QFrame(); box.setFixedSize(450, 400); box.setStyleSheet("border:2px solid magenta; background:#0a0a0a; border-radius:10px;")
        bl = QVBoxLayout(box); bl.addWidget(QLabel("REWRITE OPERATOR DATA?"), alignment=Qt.AlignmentFlag.AlignCenter)
        self.new_u = QLineEdit(); self.new_p = QLineEdit()
        self.new_u.setPlaceholderText("NEW_ID"); self.new_p.setPlaceholderText("NEW_KEY")
        style = "background:#000; color:magenta; border:1px solid #222; padding:10px; margin:5px;"
        self.new_u.setStyleSheet(style); self.new_p.setStyleSheet(style)
        btn_y = QPushButton("SYNC"); btn_y.clicked.connect(self.save_new_creds)
        btn_y.setStyleSheet("background:magenta; color:#000; padding:10px;")
        btn_n = QPushButton("SKIP"); btn_n.clicked.connect(lambda: self.main_stack.setCurrentIndex(2))
        bl.addWidget(self.new_u); bl.addWidget(self.new_p); bl.addWidget(btn_y); bl.addWidget(btn_n)
        lay.addWidget(box); self.main_stack.addWidget(page)

    def init_main_os_ui(self):
        self.os_page = QWidget(); os_lay = QVBoxLayout(self.os_page)
        hud = QHBoxLayout()
        # ARSENAL PANEL
        self.left_p = QFrame(); self.left_p.setFixedWidth(200); self.left_p.setStyleSheet("background:rgba(0,0,0,0.8); border-right:1px solid #00f2ff;")
        ll = QVBoxLayout(self.left_p); ll.addWidget(QLabel("[ ARSENAL_BAY ]"))
        for name, data in self.arsenal.items():
            t_btn = QPushButton(name)
            t_btn.setStyleSheet(f"background:transparent; border:1px solid {data[1]}; color:{data[1]}; padding:8px;")
            t_btn.clicked.connect(lambda ch, u=data[0], n=name: self.deploy_tool(u, n))
            ll.addWidget(t_btn)
        ll.addStretch(); hud.addWidget(self.left_p)
        # VISUALS
        self.globe = SimpleGlobe(self); hud.addWidget(self.globe, 2)
        self.console = QTextEdit(); self.console.setReadOnly(True); self.console.setStyleSheet("background:transparent; border:none;")
        hud.addWidget(self.console, 1); os_lay.addLayout(hud)
        # CLI
        b_bar = QFrame(); b_bar.setFixedHeight(60); b_bar.setStyleSheet("border-top:1px solid #00f2ff; background:#000;")
        bl = QHBoxLayout(b_bar); self.cmd_in = QLineEdit(); self.cmd_in.setPlaceholderText("Commands: install [url] | run [folder] | scan | exit")
        self.cmd_in.setStyleSheet("background:transparent; border:none; font-size:16px; color:#00f2ff;")
        self.cmd_in.returnPressed.connect(self.run_cmd)
        bl.addWidget(self.cmd_in); os_lay.addWidget(b_bar)
        self.main_stack.addWidget(self.os_page)

    def check_auth(self):
        if self.u_in.text() == self.creds['user'] and self.p_in.text() == self.creds['pass']:
            self.main_stack.setCurrentIndex(1)
        else: self.u_in.setStyleSheet("border:1px solid red;")

    def save_new_creds(self):
        if self.new_u.text() and self.new_p.text():
            self.creds = {"user": self.new_u.text(), "pass": self.new_p.text()}
            with open(self.db_path, 'w') as f: json.dump(self.creds, f)
        self.main_stack.setCurrentIndex(2); self.type_text("Overseer Synchronized.")

    def run_cmd(self):
        text = self.cmd_in.text().strip().lower(); self.cmd_in.clear()
        if text.startswith("install "): self.deploy_tool(text.replace("install ", "").strip())
        elif text.startswith("run "): self.execute_tool(text.replace("run ", "").strip())
        elif "scan" in text:
            self.globe.scan_mode = True
            self.type_text("SCANNING..."); QTimer.singleShot(2000, lambda: setattr(self.globe, 'scan_mode', False))
        elif text == "exit": sys.exit()

if __name__ == "__main__":
    app = QApplication(sys.argv); win = SentinelElite(); sys.exit(app.exec())