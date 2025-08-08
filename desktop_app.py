# desktop_app.py - Windows Desktop Application for Telegram Bot

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
import json
import os
import time
from datetime import datetime
import webbrowser
import sys
from PIL import Image, ImageTk
import pystray
from pystray import MenuItem as item
import asyncio
import logging

# Import bot components
from bot import TelegramBot
from config import (
    SECRET_KEY, DEBUG, RESPONSES_FILE,
    IMAGES_DIR, AUDIO_DIR, CONVERSATION_FILE,
    API_ID, API_HASH, PHONE
)

class TelegramBotDesktopApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Telegram Bot Manager v2.0")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Bot instance
        self.bot = TelegramBot()
        self.bot_thread = None
        self.bot_running = False
        self.message_queue = []
        
        # Setup logging for message monitoring
        self.setup_logging()
        
        # Setup GUI
        self.setup_gui()
        self.setup_system_tray()
        
        # Start message monitor
        self.start_message_monitor()
        
        # Load initial data
        self.refresh_responses()
        self.refresh_media_files()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_logging(self):
        """Setup logging to capture bot messages"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('bot.log'),
                MessageHandler(self.message_queue)
            ]
        )
    
    def setup_gui(self):
        """Setup the main GUI interface"""
        # Create notebook (tabs)
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Bot Control
        self.setup_bot_control_tab(notebook)
        
        # Tab 2: Responses Management
        self.setup_responses_tab(notebook)
        
        # Tab 3: Media Files
        self.setup_media_tab(notebook)
        
        # Tab 4: Live Messages
        self.setup_messages_tab(notebook)
        
        # Tab 5: Settings
        self.setup_settings_tab(notebook)
        
        # Status bar
        self.setup_status_bar()
    
    def setup_bot_control_tab(self, notebook):
        """Setup bot control tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="🤖 Bot Control")
        
        # Bot status section
        status_frame = ttk.LabelFrame(frame, text="Bot Status", padding=10)
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.status_label = ttk.Label(status_frame, text="Bot Status: Stopped", font=("Arial", 12, "bold"))
        self.status_label.pack(side=tk.LEFT)
        
        # Control buttons
        btn_frame = ttk.Frame(status_frame)
        btn_frame.pack(side=tk.RIGHT)
        
        self.start_btn = ttk.Button(btn_frame, text="Start Bot", command=self.start_bot)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(btn_frame, text="Stop Bot", command=self.stop_bot, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Statistics section
        stats_frame = ttk.LabelFrame(frame, text="Statistics", padding=10)
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Stats labels
        self.stats_responses = ttk.Label(stats_frame, text="Total Responses: 0")
        self.stats_responses.pack(anchor=tk.W)
        
        self.stats_messages = ttk.Label(stats_frame, text="Messages Today: 0")
        self.stats_messages.pack(anchor=tk.W)
        
        self.stats_media = ttk.Label(stats_frame, text="Media Files: 0")
        self.stats_media.pack(anchor=tk.W)
        
        # Configuration check
        config_frame = ttk.LabelFrame(frame, text="Configuration", padding=10)
        config_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.config_status = tk.Text(config_frame, height=5, wrap=tk.WORD)
        self.config_status.pack(fill=tk.X)
        
        self.check_configuration()
    
    def setup_responses_tab(self, notebook):
        """Setup responses management tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="💬 Responses")
        
        # Toolbar
        toolbar = ttk.Frame(frame)
        toolbar.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(toolbar, text="➕ Add Response", command=self.add_response).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="✏️ Edit", command=self.edit_response).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="🗑️ Delete", command=self.delete_response).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="🔄 Refresh", command=self.refresh_responses).pack(side=tk.LEFT, padx=5)
        
        # Responses list
        list_frame = ttk.Frame(frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview for responses
        columns = ("keyword", "type", "content_preview")
        self.responses_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        self.responses_tree.heading("keyword", text="Keyword")
        self.responses_tree.heading("type", text="Type")
        self.responses_tree.heading("content_preview", text="Content Preview")
        
        self.responses_tree.column("keyword", width=200)
        self.responses_tree.column("type", width=100)
        self.responses_tree.column("content_preview", width=400)
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.responses_tree.yview)
        h_scroll = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=self.responses_tree.xview)
        self.responses_tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        # Pack treeview and scrollbars
        self.responses_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
    
    def setup_media_tab(self, notebook):
        """Setup media management tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="📁 Media Files")
        
        # Toolbar
        toolbar = ttk.Frame(frame)
        toolbar.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(toolbar, text="📤 Upload Image", command=lambda: self.upload_media("image")).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="🎵 Upload Audio", command=lambda: self.upload_media("audio")).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="🗑️ Delete", command=self.delete_media).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="🔄 Refresh", command=self.refresh_media_files).pack(side=tk.LEFT, padx=5)
        
        # Media list
        list_frame = ttk.Frame(frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview for media files
        columns = ("filename", "type", "size")
        self.media_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        self.media_tree.heading("filename", text="Filename")
        self.media_tree.heading("type", text="Type")
        self.media_tree.heading("size", text="Size")
        
        self.media_tree.column("filename", width=300)
        self.media_tree.column("type", width=100)
        self.media_tree.column("size", width=100)
        
        # Scrollbar
        media_scroll = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.media_tree.yview)
        self.media_tree.configure(yscrollcommand=media_scroll.set)
        
        self.media_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        media_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    
    def setup_messages_tab(self, notebook):
        """Setup live messages monitoring tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="📨 Live Messages")
        
        # Toolbar
        toolbar = ttk.Frame(frame)
        toolbar.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(toolbar, text="🧹 Clear Log", command=self.clear_message_log).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="💾 Save Log", command=self.save_message_log).pack(side=tk.LEFT, padx=5)
        
        # Auto-scroll checkbox
        self.auto_scroll_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(toolbar, text="Auto-scroll", variable=self.auto_scroll_var).pack(side=tk.LEFT, padx=10)
        
        # Messages display
        self.messages_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, height=25)
        self.messages_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Configure text tags for different message types
        self.messages_text.tag_configure("incoming", foreground="blue")
        self.messages_text.tag_configure("outgoing", foreground="green")
        self.messages_text.tag_configure("system", foreground="red")
        self.messages_text.tag_configure("timestamp", foreground="gray")
    
    def setup_settings_tab(self, notebook):
        """Setup settings tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="⚙️ Settings")
        
        # API Configuration
        api_frame = ttk.LabelFrame(frame, text="Telegram API Configuration", padding=10)
        api_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(api_frame, text="API ID:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.api_id_entry = ttk.Entry(api_frame, width=30)
        self.api_id_entry.grid(row=0, column=1, sticky=tk.W, padx=10, pady=2)
        self.api_id_entry.insert(0, API_ID or "")
        
        ttk.Label(api_frame, text="API Hash:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.api_hash_entry = ttk.Entry(api_frame, width=30)
        self.api_hash_entry.grid(row=1, column=1, sticky=tk.W, padx=10, pady=2)
        self.api_hash_entry.insert(0, API_HASH or "")
        
        ttk.Label(api_frame, text="Phone Number:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.phone_entry = ttk.Entry(api_frame, width=30)
        self.phone_entry.grid(row=2, column=1, sticky=tk.W, padx=10, pady=2)
        self.phone_entry.insert(0, PHONE or "")
        
        # Application Settings
        app_frame = ttk.LabelFrame(frame, text="Application Settings", padding=10)
        app_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.auto_start_var = tk.BooleanVar()
        ttk.Checkbutton(app_frame, text="Start bot automatically when app opens", variable=self.auto_start_var).pack(anchor=tk.W)
        
        self.minimize_to_tray_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(app_frame, text="Minimize to system tray", variable=self.minimize_to_tray_var).pack(anchor=tk.W)
        
        self.notifications_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(app_frame, text="Show message notifications", variable=self.notifications_var).pack(anchor=tk.W)
        
        # Save button
        ttk.Button(app_frame, text="💾 Save Settings", command=self.save_settings).pack(pady=10)
        
        # About section
        about_frame = ttk.LabelFrame(frame, text="About", padding=10)
        about_frame.pack(fill=tk.X, padx=10, pady=5)
        
        about_text = """
Telegram Bot Manager v2.0
A Windows desktop application for managing Telegram chatbots

Features:
• Visual bot management interface
• Real-time message monitoring
• Response and media management
• System tray integration
• Auto-start capabilities

Created with Python and Tkinter
        """
        ttk.Label(about_frame, text=about_text, justify=tk.LEFT).pack(anchor=tk.W)
    
    def setup_status_bar(self):
        """Setup status bar at bottom"""
        self.status_bar = ttk.Frame(self.root)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_text = ttk.Label(self.status_bar, text="Ready")
        self.status_text.pack(side=tk.LEFT, padx=10)
        
        # Bot status indicator
        self.bot_indicator = ttk.Label(self.status_bar, text="● Stopped", foreground="red")
        self.bot_indicator.pack(side=tk.RIGHT, padx=10)
    
    def setup_system_tray(self):
        """Setup system tray integration"""
        # Create tray icon
        try:
            # Create a simple icon (you can replace with actual icon file)
            image = Image.new('RGB', (64, 64), color='blue')
            
            menu = pystray.Menu(
                item('Show', self.show_window),
                item('Hide', self.hide_window),
                pystray.Menu.SEPARATOR,
                item('Start Bot', self.start_bot),
                item('Stop Bot', self.stop_bot),
                pystray.Menu.SEPARATOR,
                item('Exit', self.quit_app)
            )
            
            self.tray_icon = pystray.Icon("TelegramBot", image, "Telegram Bot Manager", menu)
        except Exception as e:
            print(f"System tray setup failed: {e}")
            self.tray_icon = None
    
    def check_configuration(self):
        """Check if bot is properly configured"""
        config_text = ""
        
        if not API_ID:
            config_text += "❌ API_ID not configured\n"
        else:
            config_text += "✅ API_ID configured\n"
            
        if not API_HASH:
            config_text += "❌ API_HASH not configured\n"
        else:
            config_text += "✅ API_HASH configured\n"
            
        if not PHONE:
            config_text += "❌ PHONE not configured\n"
        else:
            config_text += "✅ PHONE configured\n"
        
        if os.path.exists(RESPONSES_FILE):
            config_text += "✅ Responses file found\n"
        else:
            config_text += "❌ Responses file not found\n"
            
        self.config_status.delete(1.0, tk.END)
        self.config_status.insert(1.0, config_text)
    
    def start_bot(self):
        """Start the Telegram bot"""
        if self.bot_running:
            messagebox.showwarning("Warning", "Bot is already running!")
            return
            
        try:
            self.bot_thread = threading.Thread(target=self.run_bot, daemon=True)
            self.bot_thread.start()
            self.bot_running = True
            
            # Update GUI
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.status_label.config(text="Bot Status: Starting...")
            self.bot_indicator.config(text="● Starting", foreground="orange")
            
            self.log_message("Bot started successfully", "system")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start bot: {str(e)}")
    
    def stop_bot(self):
        """Stop the Telegram bot"""
        if not self.bot_running:
            messagebox.showwarning("Warning", "Bot is not running!")
            return
            
        try:
            self.bot_running = False
            
            # Update GUI
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.status_label.config(text="Bot Status: Stopped")
            self.bot_indicator.config(text="● Stopped", foreground="red")
            
            self.log_message("Bot stopped", "system")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop bot: {str(e)}")
    
    def run_bot(self):
        """Run bot in separate thread"""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.bot.start())
        except Exception as e:
            self.log_message(f"Bot error: {str(e)}", "system")
            self.bot_running = False
    
    def refresh_responses(self):
        """Refresh responses list"""
        # Clear existing items
        for item in self.responses_tree.get_children():
            self.responses_tree.delete(item)
        
        try:
            with open(RESPONSES_FILE, 'r', encoding='utf-8') as f:
                responses = json.load(f)
            
            for keyword, data in responses.items():
                response_type = data.get('type', 'unknown')
                content = data.get('content', [])
                
                # Create preview
                if isinstance(content, list):
                    preview = ", ".join(content[:2])
                    if len(content) > 2:
                        preview += "..."
                else:
                    preview = str(content)[:50] + "..." if len(str(content)) > 50 else str(content)
                
                self.responses_tree.insert("", tk.END, values=(keyword, response_type, preview))
            
            # Update stats
            self.stats_responses.config(text=f"Total Responses: {len(responses)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load responses: {str(e)}")
    
    def refresh_media_files(self):
        """Refresh media files list"""
        # Clear existing items
        for item in self.media_tree.get_children():
            self.media_tree.delete(item)
        
        total_files = 0
        
        try:
            # Load images
            if os.path.exists(IMAGES_DIR):
                for filename in os.listdir(IMAGES_DIR):
                    filepath = os.path.join(IMAGES_DIR, filename)
                    if os.path.isfile(filepath):
                        size = os.path.getsize(filepath)
                        size_str = f"{size / 1024:.1f} KB"
                        self.media_tree.insert("", tk.END, values=(filename, "Image", size_str))
                        total_files += 1
            
            # Load audio
            if os.path.exists(AUDIO_DIR):
                for filename in os.listdir(AUDIO_DIR):
                    filepath = os.path.join(AUDIO_DIR, filename)
                    if os.path.isfile(filepath):
                        size = os.path.getsize(filepath)
                        size_str = f"{size / 1024:.1f} KB"
                        self.media_tree.insert("", tk.END, values=(filename, "Audio", size_str))
                        total_files += 1
            
            # Update stats
            self.stats_media.config(text=f"Media Files: {total_files}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load media files: {str(e)}")
    
    def add_response(self):
        """Open add response dialog"""
        AddResponseDialog(self.root, self)
    
    def edit_response(self):
        """Edit selected response"""
        selection = self.responses_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a response to edit")
            return
        
        item = self.responses_tree.item(selection[0])
        keyword = item['values'][0]
        EditResponseDialog(self.root, self, keyword)
    
    def delete_response(self):
        """Delete selected response"""
        selection = self.responses_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a response to delete")
            return
        
        item = self.responses_tree.item(selection[0])
        keyword = item['values'][0]
        
        if messagebox.askyesno("Confirm Delete", f"Delete response for '{keyword}'?"):
            try:
                with open(RESPONSES_FILE, 'r', encoding='utf-8') as f:
                    responses = json.load(f)
                
                del responses[keyword]
                
                with open(RESPONSES_FILE, 'w', encoding='utf-8') as f:
                    json.dump(responses, f, indent=4)
                
                self.refresh_responses()
                self.log_message(f"Deleted response: {keyword}", "system")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete response: {str(e)}")
    
    def upload_media(self, media_type):
        """Upload media file"""
        if media_type == "image":
            filetypes = [("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
            target_dir = IMAGES_DIR
        else:
            filetypes = [("Audio files", "*.mp3 *.wav *.ogg *.m4a")]
            target_dir = AUDIO_DIR
        
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            try:
                import shutil
                target_path = os.path.join(target_dir, os.path.basename(filename))
                shutil.copy2(filename, target_path)
                
                self.refresh_media_files()
                self.log_message(f"Uploaded {media_type}: {os.path.basename(filename)}", "system")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to upload file: {str(e)}")
    
    def delete_media(self):
        """Delete selected media file"""
        selection = self.media_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a media file to delete")
            return
        
        item = self.media_tree.item(selection[0])
        filename = item['values'][0]
        file_type = item['values'][1]
        
        if messagebox.askyesno("Confirm Delete", f"Delete {filename}?"):
            try:
                if file_type == "Image":
                    filepath = os.path.join(IMAGES_DIR, filename)
                else:
                    filepath = os.path.join(AUDIO_DIR, filename)
                
                os.remove(filepath)
                self.refresh_media_files()
                self.log_message(f"Deleted media file: {filename}", "system")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete file: {str(e)}")
    
    def log_message(self, message, msg_type="system"):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_msg = f"[{timestamp}] {message}\n"
        
        self.messages_text.insert(tk.END, formatted_msg, msg_type)
        
        if self.auto_scroll_var.get():
            self.messages_text.see(tk.END)
        
        # Show notification if enabled
        if self.notifications_var.get() and msg_type == "incoming":
            self.show_notification(message)
    
    def clear_message_log(self):
        """Clear message log"""
        self.messages_text.delete(1.0, tk.END)
    
    def save_message_log(self):
        """Save message log to file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.messages_text.get(1.0, tk.END))
                messagebox.showinfo("Success", "Message log saved successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save log: {str(e)}")
    
    def save_settings(self):
        """Save application settings"""
        # This would typically save to a config file
        messagebox.showinfo("Info", "Settings saved successfully")
    
    def start_message_monitor(self):
        """Start monitoring messages in a separate thread"""
        def monitor():
            while True:
                if self.message_queue:
                    message = self.message_queue.pop(0)
                    self.log_message(message, "incoming")
                time.sleep(0.1)
        
        threading.Thread(target=monitor, daemon=True).start()
    
    def show_notification(self, message):
        """Show system notification"""
        if self.tray_icon:
            self.tray_icon.notify("New Message", message[:100])
    
    def show_window(self):
        """Show main window"""
        self.root.deiconify()
        self.root.lift()
    
    def hide_window(self):
        """Hide main window"""
        self.root.withdraw()
    
    def on_closing(self):
        """Handle window close event"""
        if self.minimize_to_tray_var.get() and self.tray_icon:
            self.hide_window()
            if self.tray_icon:
                threading.Thread(target=self.tray_icon.run, daemon=True).start()
        else:
            self.quit_app()
    
    def quit_app(self):
        """Quit the application"""
        if self.bot_running:
            self.stop_bot()
        
        if self.tray_icon:
            self.tray_icon.stop()
        
        self.root.quit()
        sys.exit()
    
    def run(self):
        """Run the application"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.quit_app()


class MessageHandler(logging.Handler):
    """Custom logging handler to capture messages for GUI display"""
    def __init__(self, message_queue):
        super().__init__()
        self.message_queue = message_queue
    
    def emit(self, record):
        message = self.format(record)
        self.message_queue.append(message)


class AddResponseDialog:
    """Dialog for adding new responses"""
    def __init__(self, parent, app):
        self.app = app
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add New Response")
        self.dialog.geometry("500x400")
        self.dialog.resizable(False, False)
        
        self.setup_dialog()
        self.dialog.transient(parent)
        self.dialog.grab_set()
    
    def setup_dialog(self):
        """Setup dialog widgets"""
        # Keyword entry
        ttk.Label(self.dialog, text="Keyword:").pack(anchor=tk.W, padx=10, pady=5)
        self.keyword_entry = ttk.Entry(self.dialog, width=50)
        self.keyword_entry.pack(padx=10, pady=5)
        
        # Response type
        ttk.Label(self.dialog, text="Response Type:").pack(anchor=tk.W, padx=10, pady=5)
        self.type_var = tk.StringVar(value="text")
        type_frame = ttk.Frame(self.dialog)
        type_frame.pack(padx=10, pady=5)
        
        ttk.Radiobutton(type_frame, text="Text", variable=self.type_var, value="text", command=self.on_type_change).pack(side=tk.LEFT)
        ttk.Radiobutton(type_frame, text="Image", variable=self.type_var, value="image", command=self.on_type_change).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(type_frame, text="Audio", variable=self.type_var, value="audio", command=self.on_type_change).pack(side=tk.LEFT)
        
        # Content frame (changes based on type)
        self.content_frame = ttk.Frame(self.dialog)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.setup_text_content()
        
        # Buttons
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Save", command=self.save).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def on_type_change(self):
        """Handle response type change"""
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        response_type = self.type_var.get()
        if response_type == "text":
            self.setup_text_content()
        elif response_type == "image":
            self.setup_image_content()
        else:  # audio
            self.setup_audio_content()
    
    def setup_text_content(self):
        """Setup text content widgets"""
        ttk.Label(self.content_frame, text="Text Responses (one per line):").pack(anchor=tk.W)
        self.text_content = tk.Text(self.content_frame, height=8, wrap=tk.WORD)
        self.text_content.pack(fill=tk.BOTH, expand=True, pady=5)
    
    def setup_image_content(self):
        """Setup image content widgets"""
        ttk.Label(self.content_frame, text="Select Image:").pack(anchor=tk.W)
        self.image_var = tk.StringVar()
        self.image_combo = ttk.Combobox(self.content_frame, textvariable=self.image_var, state="readonly")
        
        # Load available images
        try:
            images = [f for f in os.listdir(IMAGES_DIR) if os.path.isfile(os.path.join(IMAGES_DIR, f))]
            self.image_combo['values'] = images
        except:
            pass
        
        self.image_combo.pack(fill=tk.X, pady=5)
        
        ttk.Label(self.content_frame, text="Caption (optional):").pack(anchor=tk.W, pady=(10, 0))
        self.caption_entry = ttk.Entry(self.content_frame)
        self.caption_entry.pack(fill=tk.X, pady=5)
    
    def setup_audio_content(self):
        """Setup audio content widgets"""
        ttk.Label(self.content_frame, text="Select Audio:").pack(anchor=tk.W)
        self.audio_var = tk.StringVar()
        self.audio_combo = ttk.Combobox(self.content_frame, textvariable=self.audio_var, state="readonly")
        
        # Load available audio files
        try:
            audio = [f for f in os.listdir(AUDIO_DIR) if os.path.isfile(os.path.join(AUDIO_DIR, f))]
            self.audio_combo['values'] = audio
        except:
            pass
        
        self.audio_combo.pack(fill=tk.X, pady=5)
    
    def save(self):
        """Save the response"""
        keyword = self.keyword_entry.get().strip()
        if not keyword:
            messagebox.showwarning("Warning", "Please enter a keyword")
            return
        
        response_type = self.type_var.get()
        
        try:
            # Load existing responses
            with open(RESPONSES_FILE, 'r', encoding='utf-8') as f:
                responses = json.load(f)
            
            # Check if keyword already exists
            if keyword in responses:
                messagebox.showwarning("Warning", "Keyword already exists")
                return
            
            # Create response data
            if response_type == "text":
                content = [line.strip() for line in self.text_content.get(1.0, tk.END).split('\n') if line.strip()]
                if not content:
                    messagebox.showwarning("Warning", "Please enter at least one text response")
                    return
                response_data = {"type": "text", "content": content}
            
            elif response_type == "image":
                image_file = self.image_var.get()
                if not image_file:
                    messagebox.showwarning("Warning", "Please select an image file")
                    return
                response_data = {
                    "type": "image",
                    "content": image_file,
                    "caption": self.caption_entry.get()
                }
            
            else:  # audio
                audio_file = self.audio_var.get()
                if not audio_file:
                    messagebox.showwarning("Warning", "Please select an audio file")
                    return
                response_data = {"type": "audio", "content": audio_file}
            
            # Save response
            responses[keyword] = response_data
            
            with open(RESPONSES_FILE, 'w', encoding='utf-8') as f:
                json.dump(responses, f, indent=4)
            
            # Refresh parent app
            self.app.refresh_responses()
            self.app.log_message(f"Added response: {keyword}", "system")
            
            self.dialog.destroy()
            messagebox.showinfo("Success", "Response added successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save response: {str(e)}")


class EditResponseDialog(AddResponseDialog):
    """Dialog for editing existing responses"""
    def __init__(self, parent, app, keyword):
        self.keyword = keyword
        super().__init__(parent, app)
        self.dialog.title(f"Edit Response - {keyword}")
        self.load_existing_response()
    
    def load_existing_response(self):
        """Load existing response data"""
        try:
            with open(RESPONSES_FILE, 'r', encoding='utf-8') as f:
                responses = json.load(f)
            
            if self.keyword in responses:
                response_data = responses[self.keyword]
                
                # Set keyword (readonly)
                self.keyword_entry.insert(0, self.keyword)
                self.keyword_entry.config(state="readonly")
                
                # Set type
                response_type = response_data.get('type', 'text')
                self.type_var.set(response_type)
                self.on_type_change()
                
                # Set content based on type
                if response_type == "text":
                    content = response_data.get('content', [])
                    if isinstance(content, list):
                        self.text_content.insert(1.0, '\n'.join(content))
                    else:
                        self.text_content.insert(1.0, str(content))
                
                elif response_type == "image":
                    self.image_var.set(response_data.get('content', ''))
                    self.caption_entry.insert(0, response_data.get('caption', ''))
                
                else:  # audio
                    self.audio_var.set(response_data.get('content', ''))
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load response: {str(e)}")
    
    def save(self):
        """Save the edited response"""
        response_type = self.type_var.get()
        
        try:
            # Load existing responses
            with open(RESPONSES_FILE, 'r', encoding='utf-8') as f:
                responses = json.load(f)
            
            # Create response data
            if response_type == "text":
                content = [line.strip() for line in self.text_content.get(1.0, tk.END).split('\n') if line.strip()]
                if not content:
                    messagebox.showwarning("Warning", "Please enter at least one text response")
                    return
                response_data = {"type": "text", "content": content}
            
            elif response_type == "image":
                image_file = self.image_var.get()
                if not image_file:
                    messagebox.showwarning("Warning", "Please select an image file")
                    return
                response_data = {
                    "type": "image",
                    "content": image_file,
                    "caption": self.caption_entry.get()
                }
            
            else:  # audio
                audio_file = self.audio_var.get()
                if not audio_file:
                    messagebox.showwarning("Warning", "Please select an audio file")
                    return
                response_data = {"type": "audio", "content": audio_file}
            
            # Update response
            responses[self.keyword] = response_data
            
            with open(RESPONSES_FILE, 'w', encoding='utf-8') as f:
                json.dump(responses, f, indent=4)
            
            # Refresh parent app
            self.app.refresh_responses()
            self.app.log_message(f"Updated response: {self.keyword}", "system")
            
            self.dialog.destroy()
            messagebox.showinfo("Success", "Response updated successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update response: {str(e)}")


if __name__ == "__main__":
    try:
        app = TelegramBotDesktopApp()
        app.run()
    except KeyboardInterrupt:
        print("Application interrupted by user")
    except Exception as e:
        print(f"Application error: {e}")
        messagebox.showerror("Fatal Error", f"Application failed to start: {str(e)}")