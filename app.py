# -*- coding: utf-8 -*-
"""
Email Marketing Application - Desktop GUI
Professional Email Marketing Platform
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext, simpledialog
from datetime import datetime
import json
import threading
import os

from database import init_db, EmailOpen
from contact_manager import ContactManager
from campaign_manager import CampaignManager
from template_manager import TemplateManager
from analytics import AnalyticsManager
from email_sender import EmailSender
from tracking_server import start_tracking_server, get_tracking_server, stop_tracking_server
from tracking_hash import TrackingHashGenerator
from bounce_handler import BounceHandler
from unsubscribe_handler import UnsubscribeHandler
from segment_manager import SegmentManager
from reports_manager import ReportsManager
from list_hygiene import ListHygieneManager
from advanced_segmentation import AdvancedSegmentation
from compliance_manager import ComplianceManager
from multi_language_support import MultiLanguageBridge
from professional_tools_library import ProfessionalToolsLibrary
from smtp_providers import SMTPProviders

class EmailMarketingApp:
    """Main Application Window"""
    
    def __init__(self, root):
        print("__init__ started")
        self.root = root
        self.root.title("Email Marketing Pro - Professional Email Marketing Platform")
        self.root.geometry("1400x800")
        self.root.minsize(1200, 700)
        
        # Ultra-Modern Professional Color Scheme - Maximum Visibility
        self.colors = {
            'primary': '#2563eb',           # Bright blue (very visible)
            'secondary': '#3b82f6',         # Medium blue
            'accent': '#00d9ff',            # Bright cyan (very bright)
            'highlight': '#ff6b9d',         # Pink accent
            'success': '#10b981',           # Green
            'warning': '#f59e0b',           # Orange
            'danger': '#ef4444',            # Red
            'info': '#8b5cf6',              # Purple
            'background': '#1e293b',        # Dark blue-gray (visible)
            'surface': '#475569',           # Lighter surface (more visible)
            'card': '#64748b',              # Card background (much lighter, very visible)
            'text': '#ffffff',              # White text (pure white)
            'text_secondary': '#f1f5f9',    # Very light gray (highly visible)
            'border': '#94a3b8',            # Border color (much brighter)
            'hover': '#00d9ff',             # Hover color
            'gradient_start': '#667eea',    # Gradient start
            'gradient_end': '#764ba2'       # Gradient end
        }
        
        # Configure root background - WHITE for maximum visibility
        self.root.configure(bg='white')
        print("[OK] Root configured")
    
    def create_modern_header(self):
        """Create beautiful modern header with gradient effect"""
        header_frame = tk.Frame(self.root, 
                               bg=self.colors['primary'],
                               height=100)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)
        
        # Gradient accent line
        accent_line = tk.Frame(header_frame, 
                              bg=self.colors['accent'],
                              height=4)
        accent_line.pack(fill=tk.X, side=tk.TOP)
        
        # Content frame
        content_frame = tk.Frame(header_frame, bg=self.colors['primary'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
        
        # Left side - Title
        title_frame = tk.Frame(content_frame, bg=self.colors['primary'])
        title_frame.pack(side=tk.LEFT)
        
        title_label = tk.Label(title_frame,
                              text="📧 Email Marketing Pro",
                              font=('Segoe UI', 26, 'bold'),
                              bg=self.colors['primary'],
                              fg=self.colors['accent'])
        title_label.pack(side=tk.LEFT)
        
        subtitle_label = tk.Label(title_frame,
                                 text="Professional Email Marketing Platform",
                                 font=('Segoe UI', 11),
                                 bg=self.colors['primary'],
                                 fg=self.colors['text_secondary'])
        subtitle_label.pack(side=tk.LEFT, padx=(20, 0))
        
        # Right side - Status
        status_frame = tk.Frame(content_frame, bg=self.colors['primary'])
        status_frame.pack(side=tk.RIGHT)
        
        status_dot = tk.Label(status_frame,
                             text="●",
                             font=('Segoe UI', 24),
                             bg=self.colors['primary'],
                             fg=self.colors['success'])
        status_dot.pack(side=tk.LEFT, padx=(0, 10))
        
        status_text = tk.Label(status_frame,
                              text="System Ready",
                              font=('Segoe UI', 11, 'bold'),
                              bg=self.colors['primary'],
                              fg=self.colors['text'])
        status_text.pack(side=tk.LEFT)
        
        # Configure style
        self.setup_styles()
        
        # Set window icon
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "app_icon.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
            self.root.iconname("Email Marketing Pro")
        except Exception as e:
            pass
        
        # Labels removed - focus on tabs
        
        # Initialize managers - with error handling
        try:
            print("Initializing managers...")
            self.contact_mgr = ContactManager()
            self.campaign_mgr = CampaignManager()
            self.template_mgr = TemplateManager()
            self.analytics_mgr = AnalyticsManager()
            self.email_sender = EmailSender()
            self.bounce_handler = BounceHandler()
            self.unsubscribe_handler = UnsubscribeHandler()
            self.segment_mgr = SegmentManager()
            self.reports_mgr = ReportsManager()
            self.list_hygiene = ListHygieneManager()
            self.advanced_segmentation = AdvancedSegmentation()
            self.compliance_mgr = ComplianceManager()
            self.multi_lang_bridge = MultiLanguageBridge()
            self.tools_library = ProfessionalToolsLibrary()
            self.smtp_providers = SMTPProviders()
            print("[OK] All managers initialized")
        except Exception as e:
            print(f"Error initializing managers: {e}")
            import traceback
            traceback.print_exc()
            error_label = tk.Label(self.root, text=f"Manager Error: {str(e)}", fg='red', bg='yellow')
            error_label.pack(pady=5)
            # Set to None to avoid errors later
            self.tools_library = None
        
        # Initialize database FIRST (before creating tabs that query it)
        try:
            print("Initializing database...")
            self.init_database_silent()
            print("[OK] Database initialized")
        except Exception as e:
            print(f"Database init error: {e}")
            error_label = tk.Label(self.root, text=f"Database Error: {str(e)}", fg='red', bg='yellow')
            error_label.pack(pady=5)
        
        # Create menu bar
        try:
            print("Creating menu...")
            self.create_menu()
            print("[OK] Menu created")
        except Exception as e:
            print(f"Menu error: {e}")
        
        # Create notebook (tabs) with modern styling
        try:
            print("Creating notebook...")
            # CRITICAL: Use self.root not root
            self.notebook = ttk.Notebook(self.root)
            print("[OK] Notebook object created")
            
            # TEST: Add a simple test tab FIRST
            test_tab_frame = tk.Frame(self.notebook, bg='red')
            test_label = tk.Label(test_tab_frame, 
                                 text="TEST TAB - IF YOU SEE THIS, TABS WORK!",
                                 font=('Arial', 40, 'bold'),
                                 fg='white',
                                 bg='red')
            test_label.pack(expand=True, fill=tk.BOTH)
            self.notebook.add(test_tab_frame, text="TEST")
            print("[OK] Test tab added")
            
            self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            print("[OK] Notebook packed")
            
            # Configure notebook style to ensure visibility
            style = ttk.Style()
            style.configure('TNotebook', background='white')
            style.configure('TNotebook.Tab', background='lightgray', foreground='black', padding=[20, 10])
            style.map('TNotebook.Tab', background=[('selected', 'blue')], foreground=[('selected', 'white')])
            
            # Create tabs - with error handling for each
            print("Creating tabs...")
            try:
                self.create_dashboard_tab()
                print("[OK] Dashboard tab created")
            except Exception as e:
                print(f"Error creating dashboard tab: {e}")
                import traceback
                traceback.print_exc()
            
            try:
                self.create_contacts_tab()
                print("[OK] Contacts tab created")
            except Exception as e:
                print(f"Error creating contacts tab: {e}")
            
            try:
                self.create_campaigns_tab()
                print("[OK] Campaigns tab created")
            except Exception as e:
                print(f"Error creating campaigns tab: {e}")
            
            try:
                self.create_templates_tab()
                print("[OK] Templates tab created")
            except Exception as e:
                print(f"Error creating templates tab: {e}")
            
            try:
                self.create_analytics_tab()
                print("[OK] Analytics tab created")
            except Exception as e:
                print(f"Error creating analytics tab: {e}")
            
            try:
                self.create_tracking_tab()
                print("[OK] Tracking tab created")
            except Exception as e:
                print(f"Error creating tracking tab: {e}")
            
            try:
                self.create_reports_tab()
                print("[OK] Reports tab created")
            except Exception as e:
                print(f"Error creating reports tab: {e}")
            
            try:
                self.create_segments_tab()
                print("[OK] Segments tab created")
            except Exception as e:
                print(f"Error creating segments tab: {e}")
            
            try:
                self.create_list_hygiene_tab()
                print("[OK] List Hygiene tab created")
            except Exception as e:
                print(f"Error creating list hygiene tab: {e}")
            
            try:
                self.create_compliance_tab()
                print("[OK] Compliance tab created")
            except Exception as e:
                print(f"Error creating compliance tab: {e}")
            
            try:
                self.create_tools_tab()
                print("[OK] Tools tab created")
            except Exception as e:
                print(f"Error creating tools tab: {e}")
                import traceback
                traceback.print_exc()
            
            try:
                self.create_developer_tab()
                print("[OK] Developer tab created")
            except Exception as e:
                print(f"Error creating developer tab: {e}")
            
            try:
                self.create_settings_tab()
                print("[OK] Settings tab created")
            except Exception as e:
                print(f"Error creating settings tab: {e}")
            
            print("[OK] All tabs created")
            
        except Exception as e:
            print(f"Error creating notebook: {e}")
            import traceback
            traceback.print_exc()
            error_label = tk.Label(self.root, text=f"Notebook Error: {str(e)}", fg='red', bg='yellow', font=('Arial', 16))
            error_label.pack(pady=5)
        
        # Start tracking server
        try:
            self.start_tracking_server()
        except Exception as e:
            print(f"Error starting tracking server: {e}")
        
        # Refresh dashboard after a short delay
        try:
            self.root.after(100, self.refresh_dashboard)
        except Exception as e:
            print(f"Error scheduling refresh: {e}")
        
        print("[OK] __init__ completed successfully")
    
    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Import Contacts...", command=self.import_contacts_dialog)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Test SMTP Connection", command=self.test_smtp)
        tools_menu.add_command(label="Initialize Database", command=self.init_database)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def setup_styles(self):
        """Setup ultra-modern professional styling"""
        style = ttk.Style()
        
        # Use modern theme
        try:
            style.theme_use('clam')
        except:
            pass
        
        # Configure root
        self.root.configure(bg=self.colors['background'])
        
        # Notebook (Tabs) - Ultra Modern
        style.configure('TNotebook', 
                       background=self.colors['background'],
                       borderwidth=0)
        style.configure('TNotebook.Tab', 
                       padding=[25, 15],
                       background=self.colors['surface'],
                       foreground=self.colors['text'],
                       font=('Segoe UI', 11, 'bold'),
                       borderwidth=0)
        
        style.map('TNotebook.Tab',
                 background=[('selected', self.colors['accent'])],
                 foreground=[('selected', 'white')],
                 expand=[('selected', [1, 1, 1, 0])])
        
        # Frame styles
        style.configure('TFrame', background=self.colors['background'])
        style.configure('TLabelFrame', 
                       background=self.colors['card'],
                       foreground=self.colors['text'],
                       borderwidth=2,
                       relief='flat',
                       bordercolor=self.colors['border'])
        style.configure('TLabelFrame.Label',
                       background=self.colors['card'],
                       foreground=self.colors['accent'],
                       font=('Segoe UI', 12, 'bold'))
        
        # Label styles
        style.configure('TLabel',
                       background=self.colors['background'],
                       foreground=self.colors['text'],
                       font=('Segoe UI', 10))
        
        # Entry styles - Visible dark theme
        style.configure('TEntry',
                       fieldbackground=self.colors['card'],
                       foreground=self.colors['text'],
                       borderwidth=2,
                       relief='flat',
                       insertcolor=self.colors['accent'])
        
        # Button styles - Beautiful modern buttons
        style.configure('TButton',
                       background=self.colors['accent'],
                       foreground='white',
                       borderwidth=0,
                       relief='flat',
                       padding=[20, 12],
                       font=('Segoe UI', 10, 'bold'))
        
        style.map('TButton',
                 background=[('active', self.colors['highlight']),
                           ('pressed', self.colors['primary'])])
        
        style.configure('Primary.TButton',
                       background=self.colors['accent'],
                       foreground='white',
                       padding=[20, 12],
                       font=('Segoe UI', 10, 'bold'))
        
        style.configure('Success.TButton',
                       background=self.colors['success'],
                       foreground='white',
                       padding=[20, 12],
                       font=('Segoe UI', 10, 'bold'))
        
        style.configure('Danger.TButton',
                       background=self.colors['danger'],
                       foreground='white',
                       padding=[20, 12],
                       font=('Segoe UI', 10, 'bold'))
        
        # Treeview - Visible dark theme
        style.configure('Treeview',
                       background=self.colors['card'],
                       foreground=self.colors['text'],
                       fieldbackground=self.colors['card'],
                       borderwidth=0,
                       rowheight=32,
                       font=('Segoe UI', 10))
        style.configure('Treeview.Heading',
                       background=self.colors['accent'],
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'),
                       borderwidth=0)
        style.map('Treeview',
                 background=[('selected', self.colors['highlight'])],
                 foreground=[('selected', 'white')])
        
        # Combobox - Visible
        style.configure('TCombobox',
                       fieldbackground=self.colors['card'],
                       foreground=self.colors['text'],
                       borderwidth=2,
                       relief='flat')
    
    def init_database_silent(self):
        """Initialize database silently on startup"""
        try:
            from database import Base, engine
            # Create all tables - this will create them if they don't exist
            Base.metadata.create_all(engine)
            print("Database initialized successfully")
        except Exception as e:
            print("Database initialization error: " + str(e))
            import traceback
            traceback.print_exc()
            # Show warning to user
            try:
                import tkinter.messagebox as mb
                mb.showwarning("Database", 
                    "Database initialization failed. The app may not work correctly.\n\n"
                    "Please go to Tools > Initialize Database to fix this.\n\n"
                    "Error: " + str(e))
            except:
                pass
    
    def start_tracking_server(self):
        """Start the tracking server"""
        try:
            server = get_tracking_server('localhost', 8080)
            # Check if already running
            if server.is_running():
                print("[OK] Tracking server is already running on http://localhost:8080")
                return
            
            if start_tracking_server('localhost', 8080):
                print("[OK] Tracking server started on http://localhost:8080")
            else:
                # Check again - might have detected existing server
                if server.is_running():
                    print("[OK] Tracking server is available on http://localhost:8080")
                else:
                    print("⚠ Failed to start tracking server")
        except Exception as e:
            print(f"⚠ Tracking server error: {str(e)}")
    
    def stop_tracking_server_on_exit(self):
        """Stop tracking server when app closes"""
        try:
            stop_tracking_server()
        except:
            pass
    
    def init_database(self):
        """Initialize database"""
        try:
            init_db()
            self.template_mgr.create_default_templates()
            messagebox.showinfo("Success", "Database initialized successfully!")
            self.refresh_all_tabs()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize database: {str(e)}")
    
    def test_smtp(self):
        """Test SMTP connection with detailed error messages"""
        # Get settings from UI if available, otherwise from config
        try:
            host = self.smtp_host.get().strip() if hasattr(self, 'smtp_host') else self.email_sender.smtp_host
            port = self.smtp_port.get().strip() if hasattr(self, 'smtp_port') else str(self.email_sender.smtp_port)
            user = self.smtp_user.get().strip() if hasattr(self, 'smtp_user') else self.email_sender.smtp_user
            password = self.smtp_password.get().strip() if hasattr(self, 'smtp_password') else self.email_sender.smtp_password
            use_ssl = self.smtp_ssl.get() if hasattr(self, 'smtp_ssl') else False
            use_tls = self.smtp_tls.get() if hasattr(self, 'smtp_tls') else True
        except:
            # Fallback to config
            from config import Config
            host = Config.SMTP_HOST
            port = str(Config.SMTP_PORT)
            user = Config.SMTP_USER
            password = Config.SMTP_PASSWORD
            use_ssl = False
            use_tls = Config.SMTP_USE_TLS
        
        if not all([host, port, user, password]):
            messagebox.showerror("Error", 
                               "Please fill in all SMTP settings!\n\n"
                               "Required: Host, Port, Username, Password")
            return
        
        # Show progress window
        progress_window = tk.Toplevel(self.root)
        progress_window.title("Testing SMTP Connection")
        progress_window.geometry("500x300")
        progress_window.transient(self.root)
        progress_window.grab_set()
        
        progress_text = scrolledtext.ScrolledText(progress_window, height=12, wrap=tk.WORD, font=('Consolas', 9))
        progress_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        def test_connection():
            try:
                import smtplib
                import socket
                
                progress_text.insert(tk.END, f"🔍 Testing SMTP Connection\n")
                progress_text.insert(tk.END, f"{'='*50}\n\n")
                progress_text.insert(tk.END, f"Host: {host}\n")
                progress_text.insert(tk.END, f"Port: {port}\n")
                progress_text.insert(tk.END, f"User: {user}\n")
                progress_text.insert(tk.END, f"SSL: {use_ssl}, TLS: {use_tls}\n\n")
                progress_window.update()
                
                # Validate port
                try:
                    port_int = int(port)
                    if port_int < 1 or port_int > 65535:
                        raise ValueError("Port must be between 1 and 65535")
                except ValueError as e:
                    progress_text.insert(tk.END, f"❌ Invalid port: {str(e)}\n")
                    progress_window.update()
                    progress_window.after(3000, progress_window.destroy)
                    return
                
                # Test DNS resolution
                try:
                    progress_text.insert(tk.END, f"1. Resolving hostname... ")
                    progress_window.update()
                    socket.gethostbyname(host)
                    progress_text.insert(tk.END, "✓ OK\n")
                    progress_window.update()
                except socket.gaierror:
                    progress_text.insert(tk.END, "❌ FAILED\n")
                    progress_text.insert(tk.END, f"   Cannot resolve hostname: {host}\n")
                    progress_text.insert(tk.END, "   Check your internet connection\n")
                    progress_window.update()
                    progress_window.after(5000, progress_window.destroy)
                    return
                
                # Test connection
                server = None
                try:
                    progress_text.insert(tk.END, f"2. Connecting to server... ")
                    progress_window.update()
                    
                    if use_ssl:
                        server = smtplib.SMTP_SSL(host, port_int, timeout=15)
                        progress_text.insert(tk.END, "✓ Connected (SSL)\n")
                    else:
                        server = smtplib.SMTP(host, port_int, timeout=15)
                        progress_text.insert(tk.END, "✓ Connected\n")
                    progress_window.update()
                    
                    if use_tls and not use_ssl:
                        progress_text.insert(tk.END, f"3. Starting TLS... ")
                        progress_window.update()
                        server.starttls()
                        progress_text.insert(tk.END, "✓ TLS Started\n")
                        progress_window.update()
                    
                    # Test authentication
                    progress_text.insert(tk.END, f"4. Authenticating... ")
                    progress_window.update()
                    server.login(user, password)
                    progress_text.insert(tk.END, "✓ Authenticated\n")
                    progress_window.update()
                    
                    # Success
                    progress_text.insert(tk.END, f"\n{'='*50}\n")
                    progress_text.insert(tk.END, "✅ SUCCESS! SMTP connection is working.\n")
                    progress_text.insert(tk.END, "All settings are correct.\n")
                    progress_window.update()
                    
                    progress_window.after(3000, lambda: self._close_progress_and_show_success(progress_window))
                    
                except smtplib.SMTPAuthenticationError as e:
                    error_msg = str(e)
                    progress_text.insert(tk.END, "❌ AUTHENTICATION FAILED\n\n")
                    progress_text.insert(tk.END, f"Error: {error_msg}\n\n")
                    progress_text.insert(tk.END, "💡 Solutions:\n")
                    
                    # Provider-specific help
                    host_lower = host.lower()
                    if 'gmail' in host_lower:
                        progress_text.insert(tk.END, "• Use App Password (not regular password)\n")
                        progress_text.insert(tk.END, "• Enable 2-Factor Authentication first\n")
                        progress_text.insert(tk.END, "• Generate App Password from Google Account\n")
                    elif 'yahoo' in host_lower:
                        progress_text.insert(tk.END, "• Use App Password (not regular password)\n")
                        progress_text.insert(tk.END, "• Generate from Yahoo Account Security\n")
                    elif 'outlook' in host_lower or 'office365' in host_lower:
                        progress_text.insert(tk.END, "• Use your email and password\n")
                        progress_text.insert(tk.END, "• If 2FA enabled, use App Password\n")
                    else:
                        progress_text.insert(tk.END, "• Check username/email is correct\n")
                        progress_text.insert(tk.END, "• Check password is correct\n")
                        progress_text.insert(tk.END, "• Verify with your email provider\n")
                    
                    progress_window.update()
                    progress_window.after(8000, progress_window.destroy)
                    
                except (smtplib.SMTPConnectError, ConnectionRefusedError) as e:
                    error_msg = str(e)
                    progress_text.insert(tk.END, "❌ CONNECTION REFUSED\n\n")
                    progress_text.insert(tk.END, f"Error: {error_msg}\n\n")
                    progress_text.insert(tk.END, "💡 Possible issues:\n")
                    progress_text.insert(tk.END, "• Wrong host or port\n")
                    progress_text.insert(tk.END, "• Firewall blocking connection\n")
                    progress_text.insert(tk.END, "• Server is down\n")
                    progress_text.insert(tk.END, "• Try different port (587, 465, 25)\n")
                    progress_window.update()
                    progress_window.after(8000, progress_window.destroy)
                    
                except socket.timeout:
                    progress_text.insert(tk.END, "❌ CONNECTION TIMEOUT\n\n")
                    progress_text.insert(tk.END, "Server did not respond in time.\n\n")
                    progress_text.insert(tk.END, "💡 Possible issues:\n")
                    progress_text.insert(tk.END, "• Slow internet connection\n")
                    progress_text.insert(tk.END, "• Firewall blocking\n")
                    progress_text.insert(tk.END, "• Wrong port\n")
                    progress_window.update()
                    progress_window.after(5000, progress_window.destroy)
                    
                except Exception as e:
                    error_type = type(e).__name__
                    error_msg = str(e)
                    progress_text.insert(tk.END, f"❌ ERROR: {error_type}\n\n")
                    progress_text.insert(tk.END, f"Error: {error_msg}\n\n")
                    progress_text.insert(tk.END, "Please check all settings and try again.\n")
                    progress_window.update()
                    progress_window.after(5000, progress_window.destroy)
                finally:
                    if server:
                        try:
                            server.quit()
                        except:
                            pass
            
            except Exception as e:
                progress_text.insert(tk.END, f"❌ UNEXPECTED ERROR\n\n")
                progress_text.insert(tk.END, f"{str(e)}\n")
                progress_window.update()
                progress_window.after(3000, progress_window.destroy)
        
        # Run test in thread
        thread = threading.Thread(target=test_connection, daemon=True)
        thread.start()
    
    def _close_progress_and_show_success(self, progress_window):
        """Close progress window and show success message"""
        progress_window.destroy()
        messagebox.showinfo("Success", 
                          "✅ SMTP Connection Successful!\n\n"
                          "Your SMTP settings are correct and ready to use.")
    
    def show_about(self):
        """Show about dialog"""
        about_text = """Email Marketing Pro
Professional Email Marketing Platform

Version 2.0.0

Features:
• Professional Contact Management
• Advanced Campaign Management
• Email Template System
• Real-time Analytics & Tracking
• Email Open Tracking
• Contact Segmentation
• Performance Metrics

© 2024 Email Marketing Pro
All rights reserved."""
        messagebox.showinfo("About Email Marketing Pro", about_text)
    
    # ==================== DASHBOARD TAB ====================
    
    def create_dashboard_tab(self):
        """Create enterprise-level dashboard tab"""
        # CRITICAL FIX: Use NO background colors - let system default
        dashboard_frame = tk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="📊 Dashboard")
        
        # Create main container - NO background
        main_container = tk.Frame(dashboard_frame)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # BIG TITLE - MUST SEE THIS
        title = tk.Label(main_container, 
                        text="📊 DASHBOARD",
                        font=('Arial', 60, 'bold'),
                        fg='blue')
        title.pack(pady=50)
        
        # Subtitle
        subtitle = tk.Label(main_container,
                            text="Email Marketing Pro - Dashboard",
                            font=('Arial', 30, 'bold'),
                            fg='green')
        subtitle.pack(pady=20)
        
        # Test button
        test_btn = tk.Button(main_container,
                            text="TEST BUTTON - Click Me",
                            font=('Arial', 24, 'bold'),
                            bg='green',
                            fg='white',
                            padx=50,
                            pady=20,
                            command=lambda: messagebox.showinfo("Test", "Dashboard works!"))
        test_btn.pack(pady=40)
        
        # Info label
        info = tk.Label(main_container,
                       text="If you see this, Dashboard tab is working!",
                       font=('Arial', 20),
                       fg='purple')
        info.pack(pady=30)
        
        # Modern Enterprise Header
        header_container = tk.Frame(main_container, bg=self.colors['background'])
        header_container.pack(fill=tk.X, padx=25, pady=(25, 30))
        
        header_card = tk.Frame(header_container, bg=self.colors['surface'], relief='flat')
        header_card.pack(fill=tk.X)
        
        # Gradient accent bar
        accent_bar = tk.Frame(header_card, bg=self.colors['accent'], height=5)
        accent_bar.pack(fill=tk.X)
        
        # Header content
        header_inner = tk.Frame(header_card, bg=self.colors['surface'], height=130)
        header_inner.pack(fill=tk.X, padx=35, pady=30)
        header_inner.pack_propagate(False)
        
        # Title section with icon
        title_section = tk.Frame(header_inner, bg=self.colors['surface'])
        title_section.pack(side=tk.LEFT, fill=tk.Y)
        
        icon_label = tk.Label(title_section,
                             text="📊",
                             font=('Segoe UI', 45),
                             bg=self.colors['surface'],
                             fg=self.colors['accent'])
        icon_label.pack(side=tk.LEFT, padx=(0, 25))
        
        title_frame = tk.Frame(title_section, bg=self.colors['surface'])
        title_frame.pack(side=tk.LEFT)
        
        title_label = tk.Label(title_frame,
                              text="Dashboard",
                              font=('Segoe UI', 34, 'bold'),
                              bg=self.colors['surface'],
                              fg=self.colors['text'])
        title_label.pack(anchor=tk.W)
        
        subtitle_label = tk.Label(title_frame,
                                 text="Real-time Analytics & Performance Insights",
                                 font=('Segoe UI', 13),
                                 bg=self.colors['surface'],
                                 fg=self.colors['text_secondary'])
        subtitle_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Enterprise Stats Cards - Beautiful Design
        stats_container = tk.Frame(main_container, bg=self.colors['background'])
        stats_container.pack(fill=tk.X, padx=25, pady=(0, 25))
        
        self.stats_labels = {}
        stats_grid = tk.Frame(stats_container, bg=self.colors['background'])
        stats_grid.pack()
        
        # Beautiful stat cards with icons
        stats = [
            ("👥", "Total Contacts", "contacts", self.colors['accent']),
            ("📧", "Active Campaigns", "campaigns", self.colors['success']),
            ("📝", "Templates", "templates", self.colors['highlight']),
            ("📊", "Open Rate", "open_rate", self.colors['warning']),
            ("🎯", "Click Rate", "click_rate", self.colors['info']),
            ("✅", "Success Rate", "success_rate", self.colors['success'])
        ]
        
        for i, (icon, label, key, color) in enumerate(stats):
            # Modern enterprise card
            card = tk.Frame(stats_grid, 
                          bg=self.colors['card'],
                          relief='flat',
                          borderwidth=1,
                          highlightbackground=self.colors['border'],
                          highlightthickness=1)
            card.grid(row=i//3, column=i%3, padx=15, pady=15, sticky='nsew')
            card.configure(width=300, height=160)
            
            # Card content with padding
            content = tk.Frame(card, bg=self.colors['card'])
            content.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)
            
            # Top: Icon + Label
            top_frame = tk.Frame(content, bg=self.colors['card'])
            top_frame.pack(fill=tk.X, pady=(0, 20))
            
            icon_widget = tk.Label(top_frame,
                                  text=icon,
                                  font=('Segoe UI', 32),
                                  bg=self.colors['card'],
                                  fg=color)
            icon_widget.pack(side=tk.LEFT, padx=(0, 15))
            
            label_widget = tk.Label(top_frame,
                                   text=label,
                                   font=('Segoe UI', 12),
                                   bg=self.colors['card'],
                                   fg=self.colors['text_secondary'],
                                   anchor='w')
            label_widget.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            # Bottom: Large value
            value_label = tk.Label(content,
                                  text="0",
                                  font=('Segoe UI', 42, 'bold'),
                                  bg=self.colors['card'],
                                  fg=color)
            value_label.pack(anchor=tk.W)
            self.stats_labels[key] = value_label
        
        # Configure grid
        for i in range(3):
            stats_grid.columnconfigure(i, weight=1, uniform="stats")
        
        # Action Buttons - Enterprise Style
        actions_container = tk.Frame(main_container, bg=self.colors['background'])
        actions_container.pack(fill=tk.X, padx=25, pady=(0, 25))
        
        actions_card = tk.Frame(actions_container, bg=self.colors['surface'], relief='flat')
        actions_card.pack(fill=tk.X)
        
        accent_line2 = tk.Frame(actions_card, bg=self.colors['accent'], height=3)
        accent_line2.pack(fill=tk.X)
        
        buttons_frame = tk.Frame(actions_card, bg=self.colors['surface'])
        buttons_frame.pack(fill=tk.X, padx=30, pady=25)
        
        refresh_btn = tk.Button(buttons_frame,
                               text="🔄 Refresh Dashboard",
                               command=self.refresh_dashboard,
                               bg=self.colors['accent'],
                               fg='white',
                               font=('Segoe UI', 12, 'bold'),
                               padx=30, pady=15,
                               cursor='hand2',
                               relief='flat',
                               borderwidth=0,
                               activebackground=self.colors['highlight'],
                               activeforeground='white')
        refresh_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        export_btn = tk.Button(buttons_frame,
                              text="📥 Export Report",
                              command=lambda: messagebox.showinfo("Info", "Export feature coming soon!"),
                              bg=self.colors['surface'],
                              fg=self.colors['text'],
                              font=('Segoe UI', 12, 'bold'),
                              padx=30, pady=15,
                              cursor='hand2',
                              relief='flat',
                              borderwidth=1,
                              highlightbackground=self.colors['border'],
                              highlightthickness=1,
                              activebackground=self.colors['card'],
                              activeforeground=self.colors['text'])
        export_btn.pack(side=tk.LEFT, padx=5)
        
        # Recent Campaigns - Enterprise Card Style
        recent_container = tk.Frame(main_container, bg=self.colors['background'])
        recent_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=(0, 25))
        
        recent_card = tk.Frame(recent_container, bg=self.colors['surface'], relief='flat')
        recent_card.pack(fill=tk.BOTH, expand=True)
        
        # Card header with accent
        card_header = tk.Frame(recent_card, bg=self.colors['accent'], height=60)
        card_header.pack(fill=tk.X)
        card_header.pack_propagate(False)
        
        header_text = tk.Label(card_header,
                              text="📋 Recent Campaigns",
                              font=('Segoe UI', 16, 'bold'),
                              bg=self.colors['accent'],
                              fg='white')
        header_text.pack(side=tk.LEFT, padx=30, pady=20)
        
        # Card content
        recent_content = tk.Frame(recent_card, bg=self.colors['surface'])
        recent_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Treeview for campaigns - Enterprise style
        columns = ("ID", "Name", "Status", "Sent", "Opens", "Clicks")
        self.recent_tree = ttk.Treeview(recent_content, columns=columns, show="headings", height=12)
        
        for col in columns:
            self.recent_tree.heading(col, text=col)
            self.recent_tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(recent_content, orient=tk.VERTICAL, command=self.recent_tree.yview)
        self.recent_tree.configure(yscrollcommand=scrollbar.set)
        
        self.recent_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Refresh dashboard after a short delay to ensure database is ready
        self.root.after(100, self.refresh_dashboard)
    
    def refresh_dashboard(self):
        """Refresh dashboard data"""
        try:
            # Update stats
            contacts = self.contact_mgr.list_contacts(limit=1000)
            campaigns = self.campaign_mgr.list_campaigns()
            templates = self.template_mgr.list_templates()
        except Exception as e:
            # Database might not be initialized yet
            print(f"Dashboard refresh error: {str(e)}")
            contacts = []
            campaigns = []
            templates = []
        
        try:
            self.stats_labels["contacts"].config(text=str(len(contacts)))
            self.stats_labels["campaigns"].config(text=str(len(campaigns)))
            self.stats_labels["templates"].config(text=str(len(templates)))
            
            # Calculate overall open rate
            try:
                overall_stats = self.analytics_mgr.get_overall_stats(30)
                if overall_stats['status'] == 'success':
                    open_rate = overall_stats['metrics']['overall_open_rate']
                    self.stats_labels["open_rate"].config(text=f"{open_rate}%")
                else:
                    self.stats_labels["open_rate"].config(text="0%")
            except:
                self.stats_labels["open_rate"].config(text="0%")
            
            # Update recent campaigns
            for item in self.recent_tree.get_children():
                self.recent_tree.delete(item)
            
            for campaign in campaigns[:10]:  # Show last 10
                try:
                    stats = self.campaign_mgr.get_campaign_stats(campaign.id)
                    if stats['status'] == 'success':
                        s = stats['stats']
                        self.recent_tree.insert("", tk.END, values=(
                            campaign.id,
                            campaign.name,
                            campaign.status,
                            s['sent'],
                            s['opened'],
                            s['clicked']
                        ))
                except:
                    # If stats fail, just show basic info
                    self.recent_tree.insert("", tk.END, values=(
                        campaign.id,
                        campaign.name,
                        campaign.status,
                        "N/A",
                        "N/A",
                        "N/A"
                    ))
        except Exception as e:
            print(f"Error refreshing dashboard: {str(e)}")
    
    # ==================== CONTACTS TAB ====================
    
    def create_contacts_tab(self):
        """Create contacts management tab"""
        contacts_frame = tk.Frame(self.notebook, bg='#1e293b')
        self.notebook.add(contacts_frame, text="👥 Contacts")
        
        # Top frame for add contacts
        add_frame = ttk.LabelFrame(contacts_frame, text="➕ Add Contacts - إضافة جهات الاتصال", padding=15)
        add_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Tabs for single vs bulk add
        add_notebook = ttk.Notebook(add_frame)
        add_notebook.pack(fill=tk.X, pady=5)
        
        # Single contact tab
        single_frame = ttk.Frame(add_notebook)
        add_notebook.add(single_frame, text="Single Contact - جهة اتصال واحدة")
        
        form_grid = ttk.Frame(single_frame)
        form_grid.pack(pady=10)
        
        ttk.Label(form_grid, text="Email:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.contact_email = ttk.Entry(form_grid, width=30)
        self.contact_email.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_grid, text="First Name:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.contact_first = ttk.Entry(form_grid, width=20)
        self.contact_first.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(form_grid, text="Last Name:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.contact_last = ttk.Entry(form_grid, width=20)
        self.contact_last.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_grid, text="Phone:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        self.contact_phone = ttk.Entry(form_grid, width=20)
        self.contact_phone.grid(row=1, column=3, padx=5, pady=5)
        
        add_single_btn = tk.Button(single_frame, text="➕ Add Single Contact", 
                                   command=self.add_contact,
                                   bg=self.colors['success'],
                                   fg='white',
                                   font=('Segoe UI', 10, 'bold'),
                                   padx=20, pady=8,
                                   cursor='hand2',
                                   relief=tk.FLAT)
        add_single_btn.pack(pady=10)
        
        # Bulk contacts tab
        bulk_frame = ttk.Frame(add_notebook)
        add_notebook.add(bulk_frame, text="Bulk Add - إضافة قائمة كاملة")
        
        bulk_info = tk.Label(bulk_frame, 
                            text="Enter contacts (one per line). Format: email,first_name,last_name,phone\n"
                                 "أدخل جهات الاتصال (واحدة في كل سطر). الصيغة: email,first_name,last_name,phone",
                            font=('Segoe UI', 9),
                            justify=tk.LEFT,
                            fg='gray')
        bulk_info.pack(pady=10, padx=10, anchor=tk.W)
        
        # Example
        example_label = tk.Label(bulk_frame,
                               text="Example - مثال:\n"
                                    "user1@example.com,John,Doe,+1234567890\n"
                                    "user2@example.com,Jane,Smith,+1234567891\n"
                                    "user3@example.com,Bob,Johnson",
                               font=('Segoe UI', 8),
                               justify=tk.LEFT,
                               fg='#3498DB',
                               bg='#EBF5FB',
                               relief=tk.SOLID,
                               borderwidth=1,
                               padx=10,
                               pady=5)
        example_label.pack(pady=5, padx=10, fill=tk.X, anchor=tk.W)
        
        # Text area for bulk input
        self.bulk_contacts_text = scrolledtext.ScrolledText(bulk_frame, height=12, wrap=tk.WORD, font=('Consolas', 10))
        self.bulk_contacts_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Bulk add button
        bulk_buttons_frame = tk.Frame(bulk_frame)
        bulk_buttons_frame.pack(fill=tk.X, padx=10, pady=5)
        
        add_bulk_btn = tk.Button(bulk_buttons_frame, text="➕ Add All Contacts - إضافة جميع جهات الاتصال", 
                                command=self.add_bulk_contacts,
                                bg=self.colors['secondary'],
                                fg='white',
                                font=('Segoe UI', 11, 'bold'),
                                padx=30, pady=10,
                                cursor='hand2',
                                relief=tk.FLAT)
        add_bulk_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(bulk_buttons_frame, text="🗑️ Clear - مسح", 
                             command=lambda: self.bulk_contacts_text.delete("1.0", tk.END),
                             bg=self.colors['warning'],
                             fg='white',
                             font=('Segoe UI', 10),
                             padx=15, pady=10,
                             cursor='hand2',
                             relief=tk.FLAT)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        import_btn = tk.Button(bulk_buttons_frame, text="📁 Import from File - استيراد من ملف", 
                              command=self.import_contacts_dialog,
                              bg=self.colors['accent'],
                              fg='white',
                              font=('Segoe UI', 10),
                              padx=15, pady=10,
                              cursor='hand2',
                              relief=tk.FLAT)
        import_btn.pack(side=tk.LEFT, padx=5)
        
        # Contacts list
        list_frame = ttk.LabelFrame(contacts_frame, text="Contacts List", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Search frame
        search_frame = ttk.Frame(list_frame)
        search_frame.pack(fill=tk.X, pady=5)
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.contact_search = ttk.Entry(search_frame, width=30)
        self.contact_search.pack(side=tk.LEFT, padx=5)
        self.contact_search.bind('<KeyRelease>', lambda e: self.refresh_contacts())
        ttk.Button(search_frame, text="Refresh", command=self.refresh_contacts).pack(side=tk.LEFT, padx=5)
        
        # Treeview
        columns = ("ID", "Email", "Name", "Phone", "Status", "Created")
        self.contacts_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.contacts_tree.heading(col, text=col)
            self.contacts_tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.contacts_tree.yview)
        self.contacts_tree.configure(yscrollcommand=scrollbar.set)
        
        self.contacts_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Action buttons
        action_frame = ttk.Frame(list_frame)
        action_frame.pack(fill=tk.X, pady=5)
        ttk.Button(action_frame, text="Unsubscribe Selected", command=self.unsubscribe_contact).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Delete Selected", command=self.delete_contact).pack(side=tk.LEFT, padx=5)
        
        self.refresh_contacts()
    
    def add_contact(self):
        """Add a new contact"""
        email = self.contact_email.get().strip()
        if not email:
            messagebox.showerror("Error", "Email is required!")
            return
        
        result = self.contact_mgr.add_contact(
            email=email,
            first_name=self.contact_first.get().strip() or None,
            last_name=self.contact_last.get().strip() or None,
            phone=self.contact_phone.get().strip() or None
        )
        
        if result['status'] == 'success':
            messagebox.showinfo("Success", "Contact added successfully!")
            self.contact_email.delete(0, tk.END)
            self.contact_first.delete(0, tk.END)
            self.contact_last.delete(0, tk.END)
            self.contact_phone.delete(0, tk.END)
            self.refresh_contacts()
        elif result['status'] == 'exists':
            messagebox.showwarning("Warning", "Contact already exists!")
        else:
            messagebox.showerror("Error", result.get('message', 'Unknown error'))
    
    def add_bulk_contacts(self):
        """Add multiple contacts from text area"""
        text_content = self.bulk_contacts_text.get("1.0", tk.END).strip()
        
        if not text_content:
            messagebox.showwarning("Warning", "Please enter contacts to add!")
            return
        
        # Parse contacts
        lines = [line.strip() for line in text_content.split('\n') if line.strip()]
        
        if not lines:
            messagebox.showwarning("Warning", "No valid contacts found!")
            return
        
        # Confirm before adding
        if not messagebox.askyesno("Confirm", f"Add {len(lines)} contacts?"):
            return
        
        contacts_data = []
        for line in lines:
            parts = [p.strip() for p in line.split(',')]
            if len(parts) >= 1 and parts[0]:  # At least email required
                contact = {
                    'email': parts[0],
                    'first_name': parts[1] if len(parts) > 1 and parts[1] else None,
                    'last_name': parts[2] if len(parts) > 2 and parts[2] else None,
                    'phone': parts[3] if len(parts) > 3 and parts[3] else None
                }
                contacts_data.append(contact)
        
        if not contacts_data:
            messagebox.showerror("Error", "No valid contacts to add!")
            return
        
        # Import contacts
        result = self.contact_mgr.import_contacts(contacts_data)
        
        # Show results
        message = (
            f"Import Complete!\n\n"
            f"✅ Successfully added: {result['success']}\n"
            f"⚠️ Already exists: {result['exists']}\n"
            f"❌ Failed: {result['failed']}\n\n"
            f"Total processed: {len(contacts_data)}"
        )
        
        if result['success'] > 0:
            messagebox.showinfo("Success", message)
            self.bulk_contacts_text.delete("1.0", tk.END)
            self.refresh_contacts()
        else:
            messagebox.showwarning("Warning", message)
    
    def refresh_contacts(self):
        """Refresh contacts list"""
        for item in self.contacts_tree.get_children():
            self.contacts_tree.delete(item)
        
        search_term = self.contact_search.get().lower()
        contacts = self.contact_mgr.list_contacts(limit=1000)
        
        for contact in contacts:
            if search_term and search_term not in contact.email.lower():
                continue
            
            name = f"{contact.first_name or ''} {contact.last_name or ''}".strip() or "N/A"
            self.contacts_tree.insert("", tk.END, values=(
                contact.id,
                contact.email,
                name,
                contact.phone or "N/A",
                contact.status,
                contact.created_at.strftime('%Y-%m-%d') if contact.created_at else "N/A"
            ))
    
    def unsubscribe_contact(self):
        """Unsubscribe selected contact"""
        selection = self.contacts_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a contact!")
            return
        
        item = self.contacts_tree.item(selection[0])
        email = item['values'][1]
        
        result = self.contact_mgr.unsubscribe(email)
        if result['status'] == 'success':
            messagebox.showinfo("Success", "Contact unsubscribed!")
            self.refresh_contacts()
        else:
            messagebox.showerror("Error", result.get('message', 'Unknown error'))
    
    def delete_contact(self):
        """Delete selected contact"""
        selection = self.contacts_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a contact!")
            return
        
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this contact?"):
            return
        
        item = self.contacts_tree.item(selection[0])
        email = item['values'][1]
        
        result = self.contact_mgr.delete_contact(email)
        if result['status'] == 'success':
            messagebox.showinfo("Success", "Contact deleted!")
            self.refresh_contacts()
        else:
            messagebox.showerror("Error", result.get('message', 'Unknown error'))
    
    def import_contacts_dialog(self):
        """Import contacts from file"""
        filename = filedialog.askopenfilename(
            title="Import Contacts - استيراد جهات الاتصال",
            filetypes=[
                ("JSON files", "*.json"),
                ("CSV files", "*.csv"),
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            try:
                # Check file extension
                if filename.lower().endswith('.json'):
                    with open(filename, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                elif filename.lower().endswith(('.csv', '.txt')):
                    # Parse CSV/TXT file
                    data = []
                    with open(filename, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            if not line:
                                continue
                            parts = [p.strip() for p in line.split(',')]
                            if len(parts) >= 1 and parts[0]:
                                contact = {
                                    'email': parts[0],
                                    'first_name': parts[1] if len(parts) > 1 and parts[1] else None,
                                    'last_name': parts[2] if len(parts) > 2 and parts[2] else None,
                                    'phone': parts[3] if len(parts) > 3 and parts[3] else None
                                }
                                data.append(contact)
                else:
                    messagebox.showerror("Error", "Unsupported file format!")
                    return
                
                if not data:
                    messagebox.showwarning("Warning", "No contacts found in file!")
                    return
                
                # Confirm import
                if not messagebox.askyesno("Confirm", f"Import {len(data)} contacts from file?"):
                    return
                
                result = self.contact_mgr.import_contacts(data)
                
                message = (
                    f"Import Complete!\n\n"
                    f"✅ Successfully added: {result['success']}\n"
                    f"⚠️ Already exists: {result['exists']}\n"
                    f"❌ Failed: {result['failed']}\n\n"
                    f"Total processed: {len(data)}"
                )
                
                messagebox.showinfo("Import Complete - اكتمل الاستيراد", message)
                self.refresh_contacts()
                
                # Also populate bulk text area with imported data
                if result['success'] > 0:
                    self.bulk_contacts_text.delete("1.0", tk.END)
                    
            except json.JSONDecodeError as e:
                messagebox.showerror("Error", f"Invalid JSON file: {str(e)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import: {str(e)}")
    
    # ==================== CAMPAIGNS TAB ====================
    
    def create_campaigns_tab(self):
        """Create campaigns management tab"""
        campaigns_frame = tk.Frame(self.notebook, bg='#1e293b')
        self.notebook.add(campaigns_frame, text="📧 Campaigns")
        
        # Create campaign frame
        create_frame = ttk.LabelFrame(campaigns_frame, text="Create Campaign", padding=10)
        create_frame.pack(fill=tk.X, padx=10, pady=10)
        
        form_frame = ttk.Frame(create_frame)
        form_frame.pack(fill=tk.X)
        
        ttk.Label(form_frame, text="Campaign Name:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.campaign_name = ttk.Entry(form_frame, width=40)
        self.campaign_name.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        ttk.Label(form_frame, text="Subject:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.campaign_subject = ttk.Entry(form_frame, width=40)
        self.campaign_subject.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        form_frame.columnconfigure(1, weight=1)
        
        # HTML editor
        html_frame = ttk.Frame(create_frame)
        html_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        ttk.Label(html_frame, text="HTML Body:").pack(anchor=tk.W)
        self.campaign_html = scrolledtext.ScrolledText(html_frame, height=10, wrap=tk.WORD)
        self.campaign_html.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(create_frame, text="Create Campaign", command=self.create_campaign).pack(pady=5)
        
        # Campaigns list
        list_frame = ttk.LabelFrame(campaigns_frame, text="Campaigns", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview
        columns = ("ID", "Name", "Subject", "Status", "Sent At", "Created")
        self.campaigns_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.campaigns_tree.heading(col, text=col)
            self.campaigns_tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.campaigns_tree.yview)
        self.campaigns_tree.configure(yscrollcommand=scrollbar.set)
        
        self.campaigns_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Action buttons
        action_frame = ttk.Frame(list_frame)
        action_frame.pack(fill=tk.X, pady=5)
        ttk.Button(action_frame, text="Add Recipients", command=self.add_recipients_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Send Campaign", command=self.send_campaign).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="View Stats", command=self.view_campaign_stats).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Refresh", command=self.refresh_campaigns).pack(side=tk.LEFT, padx=5)
        
        self.refresh_campaigns()
    
    def create_campaign(self):
        """Create a new campaign"""
        name = self.campaign_name.get().strip()
        subject = self.campaign_subject.get().strip()
        html = self.campaign_html.get("1.0", tk.END).strip()
        
        if not name or not subject or not html:
            messagebox.showerror("Error", "Please fill in all fields!")
            return
        
        result = self.campaign_mgr.create_campaign(name, subject, html)
        
        if result['status'] == 'success':
            messagebox.showinfo("Success", f"Campaign created! ID: {result['campaign'].id}")
            self.campaign_name.delete(0, tk.END)
            self.campaign_subject.delete(0, tk.END)
            self.campaign_html.delete("1.0", tk.END)
            self.refresh_campaigns()
        else:
            messagebox.showerror("Error", result.get('message', 'Unknown error'))
    
    def refresh_campaigns(self):
        """Refresh campaigns list"""
        for item in self.campaigns_tree.get_children():
            self.campaigns_tree.delete(item)
        
        try:
            campaigns = self.campaign_mgr.list_campaigns()
        except Exception as e:
            print(f"Error loading campaigns: {str(e)}")
            campaigns = []
        for campaign in campaigns:
            self.campaigns_tree.insert("", tk.END, values=(
                campaign.id,
                campaign.name,
                campaign.subject[:50] + "..." if len(campaign.subject) > 50 else campaign.subject,
                campaign.status,
                campaign.sent_at.strftime('%Y-%m-%d %H:%M') if campaign.sent_at else "N/A",
                campaign.created_at.strftime('%Y-%m-%d') if campaign.created_at else "N/A"
            ))
    
    def add_recipients_dialog(self):
        """Dialog to add recipients to campaign"""
        selection = self.campaigns_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a campaign!")
            return
        
        item = self.campaigns_tree.item(selection[0])
        campaign_id = item['values'][0]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Recipients")
        dialog.geometry("500x300")
        
        ttk.Label(dialog, text="Enter email addresses (one per line):").pack(pady=10)
        emails_text = scrolledtext.ScrolledText(dialog, height=10)
        emails_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        def add_recipients():
            emails = [e.strip() for e in emails_text.get("1.0", tk.END).strip().split('\n') if e.strip()]
            if not emails:
                messagebox.showerror("Error", "Please enter at least one email!")
                return
            
            result = self.campaign_mgr.add_recipients(campaign_id, emails=emails)
            if result['status'] == 'success':
                messagebox.showinfo("Success", f"Added {result['recipients_added']} recipients!")
                dialog.destroy()
            else:
                messagebox.showerror("Error", result.get('message', 'Unknown error'))
        
        ttk.Button(dialog, text="Add Recipients", command=add_recipients).pack(pady=10)
    
    def send_campaign(self):
        """Send selected campaign"""
        selection = self.campaigns_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a campaign!")
            return
        
        if not messagebox.askyesno("Confirm", "Are you sure you want to send this campaign?"):
            return
        
        item = self.campaigns_tree.item(selection[0])
        campaign_id = item['values'][0]
        
        def send():
            result = self.campaign_mgr.send_campaign(campaign_id)
            if result['status'] == 'success':
                results = result['results']
                messagebox.showinfo("Success",
                    f"Campaign sent!\n"
                    f"Sent: {results['sent']}\n"
                    f"Failed: {results['failed']}\n"
                    f"Skipped: {results['skipped']}")
                self.refresh_campaigns()
            else:
                messagebox.showerror("Error", result.get('message', 'Unknown error'))
        
        threading.Thread(target=send, daemon=True).start()
        messagebox.showinfo("Sending", "Sending campaign in background...")
    
    def view_campaign_stats(self):
        """View campaign statistics"""
        selection = self.campaigns_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a campaign!")
            return
        
        item = self.campaigns_tree.item(selection[0])
        campaign_id = item['values'][0]
        
        stats = self.campaign_mgr.get_campaign_stats(campaign_id)
        if stats['status'] == 'success':
            s = stats['stats']
            messagebox.showinfo("Campaign Statistics",
                f"Total Recipients: {s['total']}\n"
                f"Sent: {s['sent']}\n"
                f"Opened: {s['opened']}\n"
                f"Clicked: {s['clicked']}\n"
                f"Open Rate: {s['open_rate']:.2f}%\n"
                f"Click Rate: {s['click_rate']:.2f}%")
        else:
            messagebox.showerror("Error", stats.get('message', 'Unknown error'))
    
    # ==================== TEMPLATES TAB ====================
    
    def create_templates_tab(self):
        """Create templates management tab"""
        templates_frame = tk.Frame(self.notebook, bg='#1e293b')
        self.notebook.add(templates_frame, text="📝 Templates")
        
        # Create template frame
        create_frame = ttk.LabelFrame(templates_frame, text="Create Template", padding=10)
        create_frame.pack(fill=tk.X, padx=10, pady=10)
        
        form_frame = ttk.Frame(create_frame)
        form_frame.pack(fill=tk.X)
        
        ttk.Label(form_frame, text="Template Name:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.template_name = ttk.Entry(form_frame, width=30)
        self.template_name.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Subject:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.template_subject = ttk.Entry(form_frame, width=50)
        self.template_subject.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        form_frame.columnconfigure(1, weight=1)
        
        ttk.Label(create_frame, text="HTML Body:").pack(anchor=tk.W, pady=(10, 5))
        self.template_html = scrolledtext.ScrolledText(create_frame, height=8, wrap=tk.WORD)
        self.template_html.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(create_frame, text="Create Template", command=self.create_template).pack(pady=5)
        ttk.Button(create_frame, text="Create Default Templates", command=self.create_default_templates).pack(pady=2)
        
        # Templates list
        list_frame = ttk.LabelFrame(templates_frame, text="Templates", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ("ID", "Name", "Subject", "Created")
        self.templates_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.templates_tree.heading(col, text=col)
            self.templates_tree.column(col, width=200)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.templates_tree.yview)
        self.templates_tree.configure(yscrollcommand=scrollbar.set)
        
        self.templates_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        ttk.Button(list_frame, text="Refresh", command=self.refresh_templates).pack(pady=5)
        
        self.refresh_templates()
    
    def create_template(self):
        """Create a new template"""
        name = self.template_name.get().strip()
        subject = self.template_subject.get().strip()
        html = self.template_html.get("1.0", tk.END).strip()
        
        if not name or not subject or not html:
            messagebox.showerror("Error", "Please fill in all fields!")
            return
        
        result = self.template_mgr.create_template(name, subject, html)
        
        if result['status'] == 'success':
            messagebox.showinfo("Success", "Template created successfully!")
            self.template_name.delete(0, tk.END)
            self.template_subject.delete(0, tk.END)
            self.template_html.delete("1.0", tk.END)
            self.refresh_templates()
        else:
            messagebox.showerror("Error", result.get('message', 'Unknown error'))
    
    def create_default_templates(self):
        """Create default templates"""
        results = self.template_mgr.create_default_templates()
        success_count = sum(1 for r in results if r['status'] == 'success')
        messagebox.showinfo("Success", f"Created {success_count} default templates!")
        self.refresh_templates()
    
    def refresh_templates(self):
        """Refresh templates list"""
        for item in self.templates_tree.get_children():
            self.templates_tree.delete(item)
        
        try:
            templates = self.template_mgr.list_templates()
        except Exception as e:
            print(f"Error loading templates: {str(e)}")
            templates = []
        for template in templates:
            self.templates_tree.insert("", tk.END, values=(
                template.id,
                template.name,
                template.subject[:50] + "..." if len(template.subject) > 50 else template.subject,
                template.created_at.strftime('%Y-%m-%d') if template.created_at else "N/A"
            ))
    
    # ==================== ANALYTICS TAB ====================
    
    def create_analytics_tab(self):
        """Create analytics tab"""
        analytics_frame = tk.Frame(self.notebook, bg='#1e293b')
        self.notebook.add(analytics_frame, text="📊 Analytics")
        
        # Overall stats
        overall_frame = ttk.LabelFrame(analytics_frame, text="Overall Statistics", padding=10)
        overall_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.overall_text = scrolledtext.ScrolledText(overall_frame, height=8, wrap=tk.WORD)
        self.overall_text.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(overall_frame, text="Refresh Overall Stats", command=self.refresh_overall_stats).pack(pady=5)
        
        # Top campaigns
        top_frame = ttk.LabelFrame(analytics_frame, text="Top Performing Campaigns", padding=10)
        top_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ("ID", "Name", "Sent", "Opened", "Clicked", "Open Rate", "Click Rate")
        self.top_tree = ttk.Treeview(top_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.top_tree.heading(col, text=col)
            self.top_tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(top_frame, orient=tk.VERTICAL, command=self.top_tree.yview)
        self.top_tree.configure(yscrollcommand=scrollbar.set)
        
        self.top_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        ttk.Button(top_frame, text="Refresh Top Campaigns", command=self.refresh_top_campaigns).pack(pady=5)
        
        self.refresh_overall_stats()
        self.refresh_top_campaigns()
    
    def refresh_overall_stats(self):
        """Refresh overall statistics"""
        result = self.analytics_mgr.get_overall_stats(30)
        
        self.overall_text.delete("1.0", tk.END)
        
        if result['status'] == 'success':
            m = result['metrics']
            text = f"""Overall Statistics (Last 30 Days):

Total Campaigns: {m['total_campaigns']}
Total Emails Sent: {m['total_emails_sent']}
Total Opens: {m['total_opens']}
Total Clicks: {m['total_clicks']}
Overall Open Rate: {m['overall_open_rate']}%
Overall Click Rate: {m['overall_click_rate']}%
"""
            self.overall_text.insert("1.0", text)
        else:
            self.overall_text.insert("1.0", "No data available")
    
    def refresh_top_campaigns(self):
        """Refresh top campaigns"""
        for item in self.top_tree.get_children():
            self.top_tree.delete(item)
        
        try:
            campaigns = self.analytics_mgr.get_top_performing_campaigns(10)
            for camp in campaigns:
                self.top_tree.insert("", tk.END, values=(
                    camp['campaign_id'],
                    camp['campaign_name'],
                    camp['sent'],
                    camp['opened'],
                    camp['clicked'],
                    f"{camp['open_rate']}%",
                    f"{camp['click_rate']}%"
                ))
        except Exception as e:
            print(f"Error loading top campaigns: {str(e)}")
    
    # ==================== TRACKING TAB ====================
    
    def create_tracking_tab(self):
        """Create email open tracking tab"""
        tracking_frame = tk.Frame(self.notebook, bg='#1e293b')
        self.notebook.add(tracking_frame, text="🔍 Email Tracking")
        
        # Server status
        status_frame = ttk.LabelFrame(tracking_frame, text="Tracking Server Status", padding=10)
        status_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.tracking_status_label = ttk.Label(status_frame, text="Checking...", font=("Arial", 10))
        self.tracking_status_label.pack(pady=5)
        
        server_info = ttk.Label(status_frame, 
            text="Tracking server runs on: http://localhost:8080/track.php?mb=HASH\n"
                 "Each email gets a unique hash for tracking opens.",
            foreground="gray", justify=tk.LEFT)
        server_info.pack(pady=5)
        
        ttk.Button(status_frame, text="Refresh Status", command=self.refresh_tracking_status).pack(pady=5)
        
        # Filter frame
        filter_frame = ttk.Frame(tracking_frame)
        filter_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(filter_frame, text="Campaign:").pack(side=tk.LEFT, padx=5)
        self.tracking_campaign_var = tk.StringVar()
        self.tracking_campaign_combo = ttk.Combobox(filter_frame, textvariable=self.tracking_campaign_var, width=30)
        self.tracking_campaign_combo.pack(side=tk.LEFT, padx=5)
        self.tracking_campaign_combo.bind('<<ComboboxSelected>>', lambda e: self.refresh_tracking_list())
        
        ttk.Button(filter_frame, text="Show All", command=self.refresh_tracking_list).pack(side=tk.LEFT, padx=5)
        ttk.Button(filter_frame, text="Refresh", command=self.refresh_tracking_list).pack(side=tk.LEFT, padx=5)
        
        # Tracking list
        list_frame = ttk.LabelFrame(tracking_frame, text="Email Open Tracking", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview
        columns = ("Email", "Campaign", "Status", "Opens", "First Open", "Last Open", "IP", "Hash")
        self.tracking_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tracking_tree.heading(col, text=col)
            if col == "Hash":
                self.tracking_tree.column(col, width=100)
            elif col == "Email":
                self.tracking_tree.column(col, width=200)
            else:
                self.tracking_tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tracking_tree.yview)
        self.tracking_tree.configure(yscrollcommand=scrollbar.set)
        
        self.tracking_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Stats frame
        stats_frame = ttk.LabelFrame(tracking_frame, text="Tracking Statistics", padding=10)
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.tracking_stats_text = scrolledtext.ScrolledText(stats_frame, height=4, wrap=tk.WORD)
        self.tracking_stats_text.pack(fill=tk.BOTH, expand=True)
        
        self.refresh_tracking_status()
        self.refresh_tracking_campaigns()
        self.refresh_tracking_list()
    
    def refresh_tracking_status(self):
        """Refresh tracking server status"""
        server = get_tracking_server()
        if server.is_running():
            self.tracking_status_label.config(text="✓ Tracking Server: RUNNING on http://localhost:8080", foreground="green")
        else:
            self.tracking_status_label.config(text="✗ Tracking Server: NOT RUNNING", foreground="red")
            # Try to start it
            self.start_tracking_server()
            if server.is_running():
                self.tracking_status_label.config(text="✓ Tracking Server: STARTED on http://localhost:8080", foreground="green")
    
    def refresh_tracking_campaigns(self):
        """Refresh campaign list for filter"""
        campaigns = self.campaign_mgr.list_campaigns()
        campaign_names = ["All Campaigns"] + [f"{c.id}: {c.name}" for c in campaigns]
        self.tracking_campaign_combo['values'] = campaign_names
        if campaign_names:
            self.tracking_campaign_combo.current(0)
    
    def refresh_tracking_list(self):
        """Refresh email open tracking list"""
        from database import get_db, Campaign
        
        # Clear existing items
        for item in self.tracking_tree.get_children():
            self.tracking_tree.delete(item)
        
        db = get_db()
        try:
            # Get filter
            campaign_filter = self.tracking_campaign_var.get()
            campaign_id = None
            if campaign_filter and campaign_filter != "All Campaigns":
                try:
                    campaign_id = int(campaign_filter.split(':')[0])
                except:
                    pass
            
            # Query email opens
            query = db.query(EmailOpen)
            if campaign_id:
                query = query.filter(EmailOpen.campaign_id == campaign_id)
            
            email_opens = query.order_by(EmailOpen.opened_at.desc()).limit(1000).all()
            
            # Get campaign names
            campaigns = {c.id: c.name for c in db.query(Campaign).all()}
            
            active_count = 0
            inactive_count = 0
            
            for email_open in email_opens:
                # Determine status: ACTIVE if opened, INACTIVE if not
                status = "ACTIVE" if email_open.open_count > 0 else "INACTIVE"
                if status == "ACTIVE":
                    active_count += 1
                else:
                    inactive_count += 1
                
                campaign_name = campaigns.get(email_open.campaign_id, f"Campaign {email_open.campaign_id}")
                
                first_open = email_open.opened_at.strftime('%Y-%m-%d %H:%M') if email_open.opened_at else "Never"
                last_open = first_open  # Same for now
                
                # Color code: green for ACTIVE, red for INACTIVE
                item_id = self.tracking_tree.insert("", tk.END, values=(
                    email_open.email,
                    campaign_name,
                    status,
                    email_open.open_count,
                    first_open,
                    last_open,
                    email_open.ip_address or "N/A",
                    email_open.hash_value[:16] + "..." if len(email_open.hash_value) > 16 else email_open.hash_value
                ))
                
                # Color code rows
                if status == "ACTIVE":
                    self.tracking_tree.set(item_id, "Status", "✓ ACTIVE")
                else:
                    self.tracking_tree.set(item_id, "Status", "✗ INACTIVE")
            
            # Update stats
            total = len(email_opens)
            self.tracking_stats_text.delete("1.0", tk.END)
            stats_text = f"""Tracking Statistics:
Total Emails Tracked: {total}
ACTIVE (Opened): {active_count} ({active_count/total*100 if total > 0 else 0:.1f}%)
INACTIVE (Not Opened): {inactive_count} ({inactive_count/total*100 if total > 0 else 0:.1f}%)

Note: ACTIVE = Email was opened (tracking pixel loaded)
      INACTIVE = Email was not opened (pixel never loaded)
      Some email clients block images, which may show as INACTIVE
"""
            self.tracking_stats_text.insert("1.0", stats_text)
            
        finally:
            db.close()
    
    # ==================== REPORTS TAB ====================
    
    def create_reports_tab(self):
        """Create reports tab"""
        reports_frame = tk.Frame(self.notebook, bg='#1e293b')
        self.notebook.add(reports_frame, text="📊 Reports")
        
        # Comprehensive report
        report_frame = ttk.LabelFrame(reports_frame, text="Comprehensive Report", padding=15)
        report_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.comprehensive_report_text = scrolledtext.ScrolledText(report_frame, height=15, wrap=tk.WORD)
        self.comprehensive_report_text.pack(fill=tk.BOTH, expand=True)
        
        # Export buttons
        export_frame = ttk.Frame(report_frame)
        export_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(export_frame, text="📥 Export Contacts CSV", 
                 command=self.export_contacts_csv,
                 bg=self.colors['success'],
                 fg='white',
                 font=('Segoe UI', 10, 'bold'),
                 padx=15, pady=8,
                 cursor='hand2',
                 relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        
        tk.Button(export_frame, text="📥 Export Opens CSV", 
                 command=self.export_opens_csv,
                 bg=self.colors['secondary'],
                 fg='white',
                 font=('Segoe UI', 10, 'bold'),
                 padx=15, pady=8,
                 cursor='hand2',
                 relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        
        tk.Button(export_frame, text="📥 Export Clicks CSV", 
                 command=self.export_clicks_csv,
                 bg=self.colors['accent'],
                 fg='white',
                 font=('Segoe UI', 10, 'bold'),
                 padx=15, pady=8,
                 cursor='hand2',
                 relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        
        tk.Button(export_frame, text="🔄 Refresh Report", 
                 command=self.refresh_comprehensive_report,
                 bg=self.colors['warning'],
                 fg='white',
                 font=('Segoe UI', 10, 'bold'),
                 padx=15, pady=8,
                 cursor='hand2',
                 relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        
        # Daily stats
        daily_frame = ttk.LabelFrame(reports_frame, text="Daily Statistics (Last 7 Days)", padding=15)
        daily_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ("Date", "Opens", "Bounces", "Unsubscribes")
        self.daily_stats_tree = ttk.Treeview(daily_frame, columns=columns, show="headings", height=8)
        
        for col in columns:
            self.daily_stats_tree.heading(col, text=col)
            self.daily_stats_tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(daily_frame, orient=tk.VERTICAL, command=self.daily_stats_tree.yview)
        self.daily_stats_tree.configure(yscrollcommand=scrollbar.set)
        
        self.daily_stats_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.refresh_comprehensive_report()
        self.refresh_daily_stats()
    
    def refresh_comprehensive_report(self):
        """Refresh comprehensive report"""
        self.comprehensive_report_text.delete("1.0", tk.END)
        
        try:
            report = self.reports_mgr.get_comprehensive_report()
            
            if report['status'] == 'success':
                text = f"""COMPREHENSIVE EMAIL MARKETING REPORT
==========================================

CONTACTS:
  Total Contacts: {report['contacts']['total']}
  Active: {report['contacts']['active']}
  Unsubscribed: {report['contacts']['unsubscribed']}
  Bounced: {report['contacts']['bounced']}

CAMPAIGNS:
  Total Campaigns: {report['campaigns']['total']}
  Sent Campaigns: {report['campaigns']['sent']}

EMAIL STATISTICS:
  Total Emails Sent: {report['emails']['total_sent']}
  Total Opens: {report['emails']['total_opens']}
  Total Clicks: {report['emails']['total_clicks']}
  Total Bounces: {report['emails']['total_bounces']}
  Total Unsubscribes: {report['emails']['total_unsubscribes']}

PERFORMANCE RATES:
  Open Rate: {report['rates']['open_rate']}%
  Click Rate: {report['rates']['click_rate']}%
  Bounce Rate: {report['rates']['bounce_rate']}%
  Unsubscribe Rate: {report['rates']['unsubscribe_rate']}%

==========================================
Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
                self.comprehensive_report_text.insert("1.0", text)
        except Exception as e:
            self.comprehensive_report_text.insert("1.0", f"Error loading report: {str(e)}")
    
    def refresh_daily_stats(self):
        """Refresh daily statistics"""
        for item in self.daily_stats_tree.get_children():
            self.daily_stats_tree.delete(item)
        
        try:
            stats = self.reports_mgr.get_daily_stats(7)
            if stats['status'] == 'success':
                for day in stats['daily_stats']:
                    self.daily_stats_tree.insert("", tk.END, values=(
                        day['date'],
                        day['opens'],
                        day['bounces'],
                        day['unsubscribes']
                    ))
        except Exception as e:
            print(f"Error loading daily stats: {str(e)}")
    
    def export_contacts_csv(self):
        """Export contacts to CSV"""
        try:
            csv_data = self.reports_mgr.export_contacts_csv()
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Save Contacts CSV"
            )
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(csv_data)
                messagebox.showinfo("Success", f"Contacts exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def export_opens_csv(self):
        """Export opens to CSV"""
        try:
            csv_data = self.reports_mgr.export_opens_csv()
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Save Opens CSV"
            )
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(csv_data)
                messagebox.showinfo("Success", f"Opens exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def export_clicks_csv(self):
        """Export clicks to CSV"""
        try:
            csv_data = self.reports_mgr.export_clicks_csv()
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Save Clicks CSV"
            )
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(csv_data)
                messagebox.showinfo("Success", f"Clicks exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    # ==================== SEGMENTS TAB ====================
    
    def create_segments_tab(self):
        """Create segments tab"""
        segments_frame = tk.Frame(self.notebook, bg='#1e293b')
        self.notebook.add(segments_frame, text="🎯 Segments")
        
        # Create segment frame
        create_frame = ttk.LabelFrame(segments_frame, text="Create Segment", padding=15)
        create_frame.pack(fill=tk.X, padx=10, pady=10)
        
        form_frame = ttk.Frame(create_frame)
        form_frame.pack(fill=tk.X)
        
        ttk.Label(form_frame, text="Segment Name:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.segment_name = ttk.Entry(form_frame, width=40)
        self.segment_name.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        ttk.Label(form_frame, text="Description:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.segment_description = ttk.Entry(form_frame, width=40)
        self.segment_description.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        form_frame.columnconfigure(1, weight=1)
        
        tk.Button(create_frame, text="➕ Create Segment", 
                 command=self.create_segment,
                 bg=self.colors['success'],
                 fg='white',
                 font=('Segoe UI', 10, 'bold'),
                 padx=20, pady=8,
                 cursor='hand2',
                 relief=tk.FLAT).pack(pady=10)
        
        # Segments list
        list_frame = ttk.LabelFrame(segments_frame, text="Segments", padding=15)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ("ID", "Name", "Description", "Members", "Created")
        self.segments_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.segments_tree.heading(col, text=col)
            self.segments_tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.segments_tree.yview)
        self.segments_tree.configure(yscrollcommand=scrollbar.set)
        
        self.segments_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Action buttons
        action_frame = tk.Frame(list_frame)
        action_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(action_frame, text="👥 View Members", 
                 command=self.view_segment_members,
                 bg=self.colors['secondary'],
                 fg='white',
                 font=('Segoe UI', 9, 'bold'),
                 padx=15, pady=6,
                 cursor='hand2',
                 relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        
        tk.Button(action_frame, text="🗑️ Delete", 
                 command=self.delete_segment,
                 bg=self.colors['danger'],
                 fg='white',
                 font=('Segoe UI', 9, 'bold'),
                 padx=15, pady=6,
                 cursor='hand2',
                 relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        
        tk.Button(action_frame, text="🔄 Refresh", 
                 command=self.refresh_segments,
                 bg=self.colors['warning'],
                 fg='white',
                 font=('Segoe UI', 9),
                 padx=15, pady=6,
                 cursor='hand2',
                 relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        
        # Advanced Segmentation
        advanced_frame = ttk.LabelFrame(segments_frame, text="Advanced Segmentation", padding=15)
        advanced_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(advanced_frame, text="Create Dynamic Segment:").pack(anchor=tk.W, pady=5)
        
        segment_type_frame = ttk.Frame(advanced_frame)
        segment_type_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(segment_type_frame, text="Type:").pack(side=tk.LEFT, padx=5)
        self.advanced_segment_type = ttk.Combobox(segment_type_frame, 
                                                   values=['Behavior', 'Lifecycle', 'Demographics'],
                                                   width=20, state='readonly')
        self.advanced_segment_type.current(0)
        self.advanced_segment_type.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(segment_type_frame, text="Value:").pack(side=tk.LEFT, padx=5)
        self.advanced_segment_value = ttk.Combobox(segment_type_frame, width=25)
        self.advanced_segment_value.pack(side=tk.LEFT, padx=5)
        
        # Update values based on type
        def update_segment_values(event=None):
            seg_type = self.advanced_segment_type.get()
            if seg_type == 'Behavior':
                self.advanced_segment_value['values'] = ['high_engagement', 'low_engagement', 'clickers', 'recent_subscribers']
            elif seg_type == 'Lifecycle':
                self.advanced_segment_value['values'] = ['new', 'active', 'at_risk', 'churned']
            elif seg_type == 'Demographics':
                self.advanced_segment_value['values'] = ['active', 'inactive', 'bounced', 'unsubscribed']
            if self.advanced_segment_value['values']:
                self.advanced_segment_value.current(0)
        
        self.advanced_segment_type.bind('<<ComboboxSelected>>', update_segment_values)
        update_segment_values()  # Initialize
        
        ttk.Label(segment_type_frame, text="Name:").pack(side=tk.LEFT, padx=5)
        self.advanced_segment_name = ttk.Entry(segment_type_frame, width=25)
        self.advanced_segment_name.pack(side=tk.LEFT, padx=5)
        
        tk.Button(advanced_frame, text="➕ Create Dynamic Segment", 
                 command=self.create_advanced_segment,
                 bg=self.colors['accent'],
                 fg='white',
                 font=('Segoe UI', 9, 'bold'),
                 padx=15, pady=6,
                 cursor='hand2',
                 relief=tk.FLAT).pack(pady=10)
        
        self.refresh_segments()
    
    def create_segment(self):
        """Create a new segment"""
        name = self.segment_name.get().strip()
        if not name:
            messagebox.showerror("Error", "Segment name is required!")
            return
        
        result = self.segment_mgr.create_segment(
            name=name,
            description=self.segment_description.get().strip() or None
        )
        
        if result['status'] == 'success':
            messagebox.showinfo("Success", "Segment created successfully!")
            self.segment_name.delete(0, tk.END)
            self.segment_description.delete(0, tk.END)
            self.refresh_segments()
        else:
            messagebox.showerror("Error", result.get('message', 'Unknown error'))
    
    def refresh_segments(self):
        """Refresh segments list"""
        for item in self.segments_tree.get_children():
            self.segments_tree.delete(item)
        
        try:
            segments = self.segment_mgr.list_segments()
            for segment in segments:
                members = self.segment_mgr.get_segment_contacts(segment.id)
                self.segments_tree.insert("", tk.END, values=(
                    segment.id,
                    segment.name,
                    segment.description or "N/A",
                    len(members),
                    segment.created_at.strftime('%Y-%m-%d') if segment.created_at else "N/A"
                ))
        except Exception as e:
            print(f"Error loading segments: {str(e)}")
    
    def view_segment_members(self):
        """View segment members"""
        selection = self.segments_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a segment!")
            return
        
        item = self.segments_tree.item(selection[0])
        segment_id = item['values'][0]
        
        try:
            contacts = self.segment_mgr.get_segment_contacts(segment_id)
            message = f"Segment: {item['values'][1]}\n\nMembers: {len(contacts)}\n\n"
            for contact in contacts[:20]:  # Show first 20
                message += f"- {contact.email}\n"
            if len(contacts) > 20:
                message += f"\n... and {len(contacts) - 20} more"
            
            messagebox.showinfo("Segment Members", message)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def delete_segment(self):
        """Delete selected segment"""
        selection = self.segments_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a segment!")
            return
        
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this segment?"):
            return
        
        item = self.segments_tree.item(selection[0])
        segment_id = item['values'][0]
        
        result = self.segment_mgr.delete_segment(segment_id)
        if result['status'] == 'success':
            messagebox.showinfo("Success", "Segment deleted!")
            self.refresh_segments()
        else:
            messagebox.showerror("Error", result.get('message', 'Unknown error'))
    
    def create_advanced_segment(self):
        """Create advanced dynamic segment"""
        segment_type = self.advanced_segment_type.get()
        segment_value = self.advanced_segment_value.get()
        segment_name = self.advanced_segment_name.get().strip()
        
        if not segment_name:
            messagebox.showwarning("Warning", "Please enter a segment name!")
            return
        
        try:
            conditions = {}
            
            if segment_type == 'Behavior':
                conditions['behavior'] = {
                    'type': segment_value,
                    'days': 30,
                    'threshold': 1
                }
            elif segment_type == 'Lifecycle':
                conditions['lifecycle'] = segment_value
            elif segment_type == 'Demographics':
                conditions['demographics'] = {
                    'field': 'status',
                    'value': segment_value
                }
            
            result = self.advanced_segmentation.create_dynamic_segment(segment_name, conditions)
            
            if result['status'] == 'success':
                messagebox.showinfo("Success", f"Dynamic segment '{segment_name}' created!")
                self.advanced_segment_name.delete(0, tk.END)
                self.refresh_segments()
            else:
                messagebox.showerror("Error", result.get('message', 'Unknown error'))
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    # ==================== LIST HYGIENE TAB ====================
    
    def create_list_hygiene_tab(self):
        """Create list hygiene tab"""
        hygiene_frame = tk.Frame(self.notebook, bg='#1e293b')
        self.notebook.add(hygiene_frame, text="🧹 List Hygiene")
        
        # Health Score
        health_frame = ttk.LabelFrame(hygiene_frame, text="List Health Score", padding=15)
        health_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.health_score_text = scrolledtext.ScrolledText(health_frame, height=10, wrap=tk.WORD)
        self.health_score_text.pack(fill=tk.BOTH, expand=True)
        
        tk.Button(health_frame, text="🔄 Refresh Health Score", 
                 command=self.refresh_health_score,
                 bg=self.colors['success'],
                 fg='white',
                 font=('Segoe UI', 10, 'bold'),
                 padx=15, pady=8,
                 cursor='hand2',
                 relief=tk.FLAT).pack(pady=10)
        
        # Suppression List
        suppression_frame = ttk.LabelFrame(hygiene_frame, text="Suppression List", padding=15)
        suppression_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ("Email", "Reason", "Date", "Details")
        self.suppression_tree = ttk.Treeview(suppression_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.suppression_tree.heading(col, text=col)
            self.suppression_tree.column(col, width=200)
        
        scrollbar = ttk.Scrollbar(suppression_frame, orient=tk.VERTICAL, command=self.suppression_tree.yview)
        self.suppression_tree.configure(yscrollcommand=scrollbar.set)
        
        self.suppression_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Actions
        action_frame = tk.Frame(suppression_frame)
        action_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(action_frame, text="🔍 Find Inactive Contacts", 
                 command=self.find_inactive_contacts,
                 bg=self.colors['warning'],
                 fg='white',
                 font=('Segoe UI', 9, 'bold'),
                 padx=15, pady=6,
                 cursor='hand2',
                 relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        
        tk.Button(action_frame, text="🧹 Cleanup Inactive", 
                 command=self.cleanup_inactive,
                 bg=self.colors['danger'],
                 fg='white',
                 font=('Segoe UI', 9, 'bold'),
                 padx=15, pady=6,
                 cursor='hand2',
                 relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        
        tk.Button(action_frame, text="🔄 Refresh", 
                 command=self.refresh_suppression_list,
                 bg=self.colors['secondary'],
                 fg='white',
                 font=('Segoe UI', 9),
                 padx=15, pady=6,
                 cursor='hand2',
                 relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        
        self.refresh_health_score()
        self.refresh_suppression_list()
    
    def refresh_health_score(self):
        """Refresh list health score"""
        self.health_score_text.delete("1.0", tk.END)
        
        try:
            health = self.list_hygiene.get_list_health_score()
            
            status_emoji = "🟢" if health['status'] == 'excellent' else "🟡" if health['status'] == 'good' else "🟠" if health['status'] == 'fair' else "🔴"
            
            text = f"""LIST HEALTH REPORT
==========================================

{status_emoji} Overall Health Score: {health['health_score']}/100 ({health['status'].upper()})

CONTACTS BREAKDOWN:
  Total Contacts: {health['total_contacts']}
  Active: {health['active_contacts']} ({health['active_rate']}%)
  Bounced: {health['bounced']} ({health['bounce_rate']}%)
  Unsubscribed: {health['unsubscribed']} ({health['unsubscribe_rate']}%)
  Suppressed: {health['suppressed']}

ENGAGEMENT:
  Engagement Rate: {health['engagement_rate']}%

RECOMMENDATIONS:
"""
            if health['bounce_rate'] > 5:
                text += "  ⚠️ High bounce rate! Review email validation.\n"
            if health['unsubscribe_rate'] > 2:
                text += "  ⚠️ High unsubscribe rate! Review email content.\n"
            if health['engagement_rate'] < 20:
                text += "  ⚠️ Low engagement! Consider re-engagement campaigns.\n"
            if health['health_score'] >= 80:
                text += "  ✓ List is healthy! Keep up the good work.\n"
            
            text += f"\n==========================================\nReport Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            self.health_score_text.insert("1.0", text)
        except Exception as e:
            self.health_score_text.insert("1.0", f"Error loading health score: {str(e)}")
    
    def refresh_suppression_list(self):
        """Refresh suppression list"""
        for item in self.suppression_tree.get_children():
            self.suppression_tree.delete(item)
        
        try:
            suppressions = self.list_hygiene.get_suppression_list()
            for sup in suppressions:
                self.suppression_tree.insert("", tk.END, values=(
                    sup['email'],
                    sup['reason'],
                    sup['date'].strftime('%Y-%m-%d') if sup['date'] else "N/A",
                    sup['details'] or "N/A"
                ))
        except Exception as e:
            print(f"Error loading suppression list: {str(e)}")
    
    def find_inactive_contacts(self):
        """Find inactive contacts"""
        try:
            candidates = self.list_hygiene.identify_suppression_candidates(days_inactive=90)
            message = f"Found {len(candidates)} inactive contacts (no opens in 90 days)\n\n"
            message += "First 20 contacts:\n"
            for contact in candidates[:20]:
                message += f"- {contact.email}\n"
            if len(candidates) > 20:
                message += f"\n... and {len(candidates) - 20} more"
            
            messagebox.showinfo("Inactive Contacts", message)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def cleanup_inactive(self):
        """Cleanup inactive contacts"""
        if not messagebox.askyesno("Confirm", 
                                   "This will suppress inactive contacts (no opens in 180 days).\n\nContinue?"):
            return
        
        try:
            result = self.list_hygiene.cleanup_inactive_contacts(days_inactive=180, action='suppress')
            messagebox.showinfo("Cleanup Complete", 
                              f"Processed: {result['processed']}\n"
                              f"Suppressed: {result['suppressed']}\n"
                              f"Errors: {result['errors']}")
            self.refresh_health_score()
            self.refresh_suppression_list()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    # ==================== COMPLIANCE TAB ====================
    
    def create_compliance_tab(self):
        """Create compliance tab"""
        compliance_frame = tk.Frame(self.notebook, bg='#1e293b')
        self.notebook.add(compliance_frame, text="⚖️ Compliance")
        
        # Compliance Info
        info_frame = ttk.LabelFrame(compliance_frame, text="Legal Compliance", padding=15)
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        info_text = """
GDPR (EU): Requires explicit consent, double opt-in, right to access/delete data
CCPA (California): Requires consent, right to delete/export data
CAN-SPAM (USA): Requires unsubscribe link, accurate sender info

This tool helps you:
✓ Record consent for contacts
✓ Manage double opt-in confirmations
✓ Export contact data (GDPR/CCPA right to access)
✓ Delete contact data (GDPR/CCPA right to be forgotten)
✓ Add compliant unsubscribe links
"""
        ttk.Label(info_frame, text=info_text, justify=tk.LEFT).pack(anchor=tk.W)
        
        # Compliance Actions
        actions_frame = ttk.LabelFrame(compliance_frame, text="Compliance Actions", padding=15)
        actions_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Export Data
        export_frame = ttk.Frame(actions_frame)
        export_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(export_frame, text="Export Contact Data (GDPR/CCPA):").pack(side=tk.LEFT, padx=5)
        self.export_email = ttk.Entry(export_frame, width=30)
        self.export_email.pack(side=tk.LEFT, padx=5)
        
        tk.Button(export_frame, text="📥 Export", 
                 command=self.export_contact_data,
                 bg=self.colors['success'],
                 fg='white',
                 font=('Segoe UI', 9, 'bold'),
                 padx=15, pady=5,
                 cursor='hand2',
                 relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        
        # Delete Data
        delete_frame = ttk.Frame(actions_frame)
        delete_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(delete_frame, text="Delete Contact Data (Right to be Forgotten):").pack(side=tk.LEFT, padx=5)
        self.delete_email = ttk.Entry(delete_frame, width=30)
        self.delete_email.pack(side=tk.LEFT, padx=5)
        
        tk.Button(delete_frame, text="🗑️ Delete", 
                 command=self.delete_contact_data,
                 bg=self.colors['danger'],
                 fg='white',
                 font=('Segoe UI', 9, 'bold'),
                 padx=15, pady=5,
                 cursor='hand2',
                 relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        
        # Consent Management
        consent_frame = ttk.LabelFrame(actions_frame, text="Consent Management", padding=10)
        consent_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(consent_frame, text="Email:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.consent_email = ttk.Entry(consent_frame, width=30)
        self.consent_email.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(consent_frame, text="Consent Type:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.consent_type = ttk.Combobox(consent_frame, values=['gdpr', 'ccpa', 'general'], width=27)
        self.consent_type.current(0)
        self.consent_type.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Button(consent_frame, text="✓ Record Consent", 
                 command=self.record_consent,
                 bg=self.colors['success'],
                 fg='white',
                 font=('Segoe UI', 9, 'bold'),
                 padx=15, pady=6,
                 cursor='hand2',
                 relief=tk.FLAT).grid(row=2, column=0, columnspan=2, pady=10)
        
        # Double Opt-in
        optin_frame = ttk.LabelFrame(actions_frame, text="Double Opt-in", padding=10)
        optin_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(optin_frame, text="Email:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.optin_email = ttk.Entry(optin_frame, width=30)
        self.optin_email.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Button(optin_frame, text="📧 Send Confirmation", 
                 command=self.setup_double_optin,
                 bg=self.colors['secondary'],
                 fg='white',
                 font=('Segoe UI', 9, 'bold'),
                 padx=15, pady=6,
                 cursor='hand2',
                 relief=tk.FLAT).grid(row=1, column=0, columnspan=2, pady=10)
    
    def export_contact_data(self):
        """Export contact data for GDPR/CCPA"""
        email = self.export_email.get().strip()
        if not email:
            messagebox.showwarning("Warning", "Please enter an email address!")
            return
        
        try:
            result = self.compliance_mgr.export_contact_data(email)
            if result['status'] == 'success':
                # Save to file
                filename = filedialog.asksaveasfilename(
                    defaultextension=".json",
                    filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                    title="Save Contact Data"
                )
                if filename:
                    import json
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(result['data'], f, indent=2, ensure_ascii=False)
                    messagebox.showinfo("Success", f"Contact data exported to {filename}")
            else:
                messagebox.showerror("Error", result.get('message', 'Unknown error'))
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def delete_contact_data(self):
        """Delete contact data for GDPR/CCPA"""
        email = self.delete_email.get().strip()
        if not email:
            messagebox.showwarning("Warning", "Please enter an email address!")
            return
        
        if not messagebox.askyesno("Confirm", 
                                   f"Are you sure you want to DELETE ALL DATA for {email}?\n\n"
                                   "This action cannot be undone!"):
            return
        
        try:
            result = self.compliance_mgr.delete_contact_data(email)
            if result['status'] == 'success':
                messagebox.showinfo("Success", "All contact data deleted successfully!")
                self.delete_email.delete(0, tk.END)
            else:
                messagebox.showerror("Error", result.get('message', 'Unknown error'))
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def record_consent(self):
        """Record consent for a contact"""
        email = self.consent_email.get().strip()
        consent_type = self.consent_type.get()
        
        if not email:
            messagebox.showwarning("Warning", "Please enter an email address!")
            return
        
        try:
            result = self.compliance_mgr.add_consent(email, consent_type)
            if result['status'] == 'success':
                messagebox.showinfo("Success", "Consent recorded successfully!")
                self.consent_email.delete(0, tk.END)
            else:
                messagebox.showerror("Error", result.get('message', 'Unknown error'))
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def setup_double_optin(self):
        """Set up double opt-in"""
        email = self.optin_email.get().strip()
        if not email:
            messagebox.showwarning("Warning", "Please enter an email address!")
            return
        
        try:
            result = self.compliance_mgr.setup_double_optin(email)
            if result['status'] == 'success':
                messagebox.showinfo("Success", "Confirmation email sent!")
                self.optin_email.delete(0, tk.END)
            else:
                messagebox.showerror("Error", result.get('message', 'Unknown error'))
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    # ==================== TOOLS TAB ====================
    
    def create_tools_tab(self):
        """Create professional tools tab"""
        tools_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(tools_frame, text="🛠️ Tools")
        
        # BIG VISIBLE TITLE - MUST SEE THIS
        title_label = tk.Label(tools_frame,
                             text="🛠️ TOOLS - 66 TOOLS AVAILABLE",
                             font=('Arial', 60, 'bold'),
                             fg='red',
                             bg='white')
        title_label.pack(pady=40)
        
        subtitle_label = tk.Label(tools_frame,
                                text="Professional Email Marketing Tools Library",
                                font=('Arial', 28, 'bold'),
                                fg='blue',
                                bg='white')
        subtitle_label.pack(pady=15)
        
        # Tools Categories
        categories_frame = ttk.LabelFrame(tools_frame, text="Tool Categories", padding=15)
        categories_frame.pack(fill=tk.X, padx=10, pady=10)
        
        categories = [
            "Email Validation", "List Management", "Segmentation", 
            "Analytics", "A/B Testing", "Automation", "Personalization",
            "Deliverability", "Compliance", "Content", "Integration",
            "AI & ML", "Performance", "Security"
        ]
        
        self.tool_category = ttk.Combobox(categories_frame, values=categories, width=30, state='readonly')
        self.tool_category.current(0)
        self.tool_category.pack(side=tk.LEFT, padx=5)
        
        tk.Button(categories_frame, text="🔍 Search Tools", 
                 command=self.search_tools,
                 bg=self.colors['secondary'],
                 fg='white',
                 font=('Segoe UI', 9, 'bold'),
                 padx=15, pady=6,
                 cursor='hand2',
                 relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        
        # Tools List
        tools_list_frame = ttk.LabelFrame(tools_frame, text="Available Tools (100+)", padding=15)
        tools_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ("Tool Name", "Category", "Status")
        self.tools_tree = ttk.Treeview(tools_list_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tools_tree.heading(col, text=col)
            self.tools_tree.column(col, width=250)
        
        scrollbar = ttk.Scrollbar(tools_list_frame, orient=tk.VERTICAL, command=self.tools_tree.yview)
        self.tools_tree.configure(yscrollcommand=scrollbar.set)
        
        self.tools_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Tool Execution
        execution_frame = ttk.LabelFrame(tools_frame, text="Execute Tool", padding=15)
        execution_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(execution_frame, text="Tool Name:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.tool_name_entry = ttk.Entry(execution_frame, width=40)
        self.tool_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        ttk.Label(execution_frame, text="Input (JSON):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.tool_input_text = scrolledtext.ScrolledText(execution_frame, height=5, width=50)
        self.tool_input_text.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        execution_frame.columnconfigure(1, weight=1)
        
        tk.Button(execution_frame, text="▶ Execute Tool", 
                 command=self.execute_tool,
                 bg=self.colors['success'],
                 fg='white',
                 font=('Segoe UI', 10, 'bold'),
                 padx=20, pady=8,
                 cursor='hand2',
                 relief=tk.FLAT).grid(row=2, column=0, columnspan=2, pady=10)
        
        # Results
        results_frame = ttk.LabelFrame(tools_frame, text="Results", padding=15)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.tool_results_text = scrolledtext.ScrolledText(results_frame, height=8, wrap=tk.WORD)
        self.tool_results_text.pack(fill=tk.BOTH, expand=True)
        
        self.refresh_tools_list()
    
    def refresh_tools_list(self):
        """Refresh tools list - Show ALL tools"""
        print("refresh_tools_list called")
        for item in self.tools_tree.get_children():
            self.tools_tree.delete(item)
        
        try:
            # Check if tools_library exists
            if not hasattr(self, 'tools_library') or self.tools_library is None:
                print("tools_library not found, using default tools")
                default_tools = [
                    ('email_validator', 'Email Validation', 'Available'),
                    ('email_quality_checker', 'Email Validation', 'Available'),
                    ('domain_validator', 'Email Validation', 'Available'),
                    ('list_cleaner', 'List Management', 'Available'),
                    ('duplicate_finder', 'List Management', 'Available'),
                    ('behavioral_segmenter', 'Segmentation', 'Available'),
                    ('engagement_calculator', 'Analytics', 'Available'),
                    ('ab_test_creator', 'A/B Testing', 'Available'),
                    ('workflow_builder', 'Automation', 'Available'),
                    ('gdpr_compliance_checker', 'Compliance', 'Available'),
                    ('ai_content_generator', 'AI & ML', 'Available'),
                ]
                for tool, category, status in default_tools:
                    self.tools_tree.insert("", tk.END, values=(tool, category, status))
                print(f"Loaded {len(default_tools)} default tools")
                return
            
            print("Getting all tools from library...")
            all_tools = self.tools_library.get_all_tools()
            print(f"Found {len(all_tools)} tools")
            
            for tool in all_tools:
                # Categorize tool
                category = "Other"
                tool_lower = tool.lower()
                
                if 'email' in tool_lower or 'validation' in tool_lower or 'domain' in tool_lower or 'mx' in tool_lower or 'spf' in tool_lower or 'dkim' in tool_lower or 'dmarc' in tool_lower:
                    category = "Email Validation"
                elif 'list' in tool_lower or 'duplicate' in tool_lower or 'clean' in tool_lower or 'suppression' in tool_lower:
                    category = "List Management"
                elif 'segment' in tool_lower or 'behavior' in tool_lower or 'demographic' in tool_lower or 'engagement' in tool_lower or 'lifecycle' in tool_lower or 'rfm' in tool_lower:
                    category = "Segmentation"
                elif 'analytics' in tool_lower or 'report' in tool_lower or 'engagement' in tool_lower or 'conversion' in tool_lower or 'revenue' in tool_lower or 'cohort' in tool_lower or 'funnel' in tool_lower:
                    category = "Analytics"
                elif 'ab' in tool_lower or 'test' in tool_lower or 'multivariate' in tool_lower or 'significance' in tool_lower:
                    category = "A/B Testing"
                elif 'automation' in tool_lower or 'workflow' in tool_lower or 'trigger' in tool_lower or 'drip' in tool_lower or 'autoresponder' in tool_lower or 're_engagement' in tool_lower:
                    category = "Automation"
                elif 'personalization' in tool_lower or 'dynamic' in tool_lower or 'recommendation' in tool_lower or 'smart_send' in tool_lower:
                    category = "Personalization"
                elif 'deliverability' in tool_lower or 'reputation' in tool_lower or 'blacklist' in tool_lower or 'inbox' in tool_lower:
                    category = "Deliverability"
                elif 'compliance' in tool_lower or 'gdpr' in tool_lower or 'ccpa' in tool_lower or 'can_spam' in tool_lower or 'consent' in tool_lower:
                    category = "Compliance"
                elif 'content' in tool_lower or 'subject' in tool_lower or 'spam' in tool_lower or 'readability' in tool_lower or 'link' in tool_lower:
                    category = "Content"
                elif 'integration' in tool_lower or 'crm' in tool_lower or 'ecommerce' in tool_lower or 'api' in tool_lower or 'webhook' in tool_lower:
                    category = "Integration"
                elif 'ai' in tool_lower or 'predict' in tool_lower or 'sentiment' in tool_lower or 'churn' in tool_lower or 'ml' in tool_lower:
                    category = "AI & ML"
                elif 'performance' in tool_lower or 'load' in tool_lower or 'cache' in tool_lower or 'cdn' in tool_lower:
                    category = "Performance"
                elif 'security' in tool_lower or 'encryption' in tool_lower or 'authentication' in tool_lower or 'rate' in tool_lower or 'scanner' in tool_lower:
                    category = "Security"
                
                self.tools_tree.insert("", tk.END, values=(
                    tool,
                    category,
                    "Available"
                ))
            
            print(f"[OK] Loaded {len(all_tools)} tools successfully")
        except Exception as e:
            print(f"Error loading tools: {e}")
            import traceback
            traceback.print_exc()
            # Show error in tree
            self.tools_tree.insert("", tk.END, values=(
                f"Error: {str(e)}",
                "Error",
                "Failed"
            ))
    
    def search_tools(self):
        """Search tools by category"""
        category = self.tool_category.get()
        # Filter tools by category
        self.refresh_tools_list()
    
    def execute_tool(self):
        """Execute selected tool"""
        tool_name = self.tool_name_entry.get().strip()
        if not tool_name:
            messagebox.showwarning("Warning", "Please enter a tool name!")
            return
        
        try:
            input_text = self.tool_input_text.get("1.0", tk.END).strip()
            input_data = json.loads(input_text) if input_text else {}
            
            result = self.tools_library.execute_tool(tool_name, **input_data)
            
            self.tool_results_text.delete("1.0", tk.END)
            if result['status'] == 'success':
                self.tool_results_text.insert("1.0", json.dumps(result['result'], indent=2))
            else:
                self.tool_results_text.insert("1.0", f"Error: {result.get('message', 'Unknown error')}")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON input!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    # ==================== DEVELOPER TAB ====================
    
    def create_developer_tab(self):
        """Create developer tab for multi-language support"""
        dev_frame = tk.Frame(self.notebook, bg='#1e293b')
        self.notebook.add(dev_frame, text="💻 Developer")
        
        # Language Selection
        lang_frame = ttk.LabelFrame(dev_frame, text="Programming Language", padding=15)
        lang_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(lang_frame, text="Select Language:").pack(side=tk.LEFT, padx=5)
        self.dev_language = ttk.Combobox(lang_frame, 
                                        values=self.multi_lang_bridge.get_supported_languages(),
                                        width=25, state='readonly')
        self.dev_language.current(0)
        self.dev_language.pack(side=tk.LEFT, padx=5)
        
        tk.Button(lang_frame, text="✓ Check Availability", 
                 command=self.check_language_availability,
                 bg=self.colors['secondary'],
                 fg='white',
                 font=('Segoe UI', 9, 'bold'),
                 padx=15, pady=6,
                 cursor='hand2',
                 relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        
        # Code Editor
        code_frame = ttk.LabelFrame(dev_frame, text="Code Editor", padding=15)
        code_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(code_frame, text="Write your code:").pack(anchor=tk.W, pady=5)
        self.code_editor = scrolledtext.ScrolledText(code_frame, height=15, wrap=tk.NONE, font=('Consolas', 10))
        self.code_editor.pack(fill=tk.BOTH, expand=True)
        
        # Input Data
        input_frame = ttk.LabelFrame(code_frame, text="Input Data (JSON)", padding=10)
        input_frame.pack(fill=tk.X, pady=10)
        
        self.code_input = scrolledtext.ScrolledText(input_frame, height=3, wrap=tk.WORD)
        self.code_input.pack(fill=tk.X)
        
        # Execute Button
        tk.Button(code_frame, text="▶ Execute Code", 
                 command=self.execute_code,
                 bg=self.colors['success'],
                 fg='white',
                 font=('Segoe UI', 10, 'bold'),
                 padx=20, pady=8,
                 cursor='hand2',
                 relief=tk.FLAT).pack(pady=10)
        
        # Results
        results_frame = ttk.LabelFrame(dev_frame, text="Execution Results", padding=15)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.code_results_text = scrolledtext.ScrolledText(results_frame, height=8, wrap=tk.WORD)
        self.code_results_text.pack(fill=tk.BOTH, expand=True)
        
        # Language Info
        info_text = """
Supported Languages:
Python, JavaScript, Java, Go, Rust, PHP, Ruby, C, C++, Swift, Kotlin, R, Perl, Lua, Scala, Dart, TypeScript, Shell, PowerShell

Note: Some languages require runtime installation (Java JDK, Go, Rust compiler, etc.)
"""
        ttk.Label(dev_frame, text=info_text, foreground="gray", justify=tk.LEFT).pack(anchor=tk.W, padx=10, pady=5)
    
    def check_language_availability(self):
        """Check if selected language is available"""
        language = self.dev_language.get()
        if not language:
            return
        
        available = self.multi_lang_bridge.check_language_available(language)
        status = "✓ Available" if available else "✗ Not Installed"
        messagebox.showinfo("Language Status", f"{language}: {status}")
    
    def execute_code(self):
        """Execute code in selected language"""
        language = self.dev_language.get()
        code = self.code_editor.get("1.0", tk.END).strip()
        
        if not language:
            messagebox.showwarning("Warning", "Please select a language!")
            return
        
        if not code:
            messagebox.showwarning("Warning", "Please write some code!")
            return
        
        try:
            input_text = self.code_input.get("1.0", tk.END).strip()
            input_data = json.loads(input_text) if input_text else {}
            
            result = self.multi_lang_bridge.execute_code(language, code, input_data)
            
            self.code_results_text.delete("1.0", tk.END)
            if result['status'] == 'success':
                output = f"Status: {result['status']}\n"
                output += f"Output:\n{result.get('output', '')}\n"
                if result.get('error'):
                    output += f"\nErrors:\n{result['error']}"
                self.code_results_text.insert("1.0", output)
            else:
                self.code_results_text.insert("1.0", f"Error: {result.get('message', 'Unknown error')}")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON input!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    # ==================== SETTINGS TAB ====================
    
    def create_settings_tab(self):
        """Create settings tab"""
        settings_frame = tk.Frame(self.notebook, bg='#1e293b')
        self.notebook.add(settings_frame, text="⚙️ Settings")
        
        smtp_frame = ttk.LabelFrame(settings_frame, text="SMTP Configuration", padding=10)
        smtp_frame.pack(fill=tk.X, padx=10, pady=10)
        
        from config import Config
        
        form_grid = ttk.Frame(smtp_frame)
        form_grid.pack(fill=tk.X)
        
        ttk.Label(form_grid, text="SMTP Host:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.smtp_host = ttk.Entry(form_grid, width=40)
        self.smtp_host.insert(0, Config.SMTP_HOST)
        self.smtp_host.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        ttk.Label(form_grid, text="SMTP Port:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.smtp_port = ttk.Entry(form_grid, width=40)
        self.smtp_port.insert(0, str(Config.SMTP_PORT))
        self.smtp_port.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        ttk.Label(form_grid, text="SMTP User:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.smtp_user = ttk.Entry(form_grid, width=40)
        self.smtp_user.insert(0, Config.SMTP_USER)
        self.smtp_user.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        ttk.Label(form_grid, text="SMTP Password:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.smtp_password = ttk.Entry(form_grid, width=40, show="*")
        self.smtp_password.insert(0, Config.SMTP_PASSWORD)
        self.smtp_password.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        form_grid.columnconfigure(1, weight=1)
        
        info_text = """
Note: SMTP settings are loaded from .env file.
To change settings, edit the .env file and restart the application.

For Gmail:
- Use App Password (not regular password)
- Enable 2-factor authentication first
- Generate App Password from Google Account settings
"""
        ttk.Label(smtp_frame, text=info_text, foreground="gray", justify=tk.LEFT).pack(anchor=tk.W, pady=10)
        
        ttk.Button(smtp_frame, text="Test SMTP Connection", command=self.test_smtp).pack(pady=5)
    
    def refresh_all_tabs(self):
        """Refresh all tabs"""
        self.refresh_dashboard()
        self.refresh_contacts()
        self.refresh_campaigns()
        self.refresh_templates()
        self.refresh_overall_stats()
        self.refresh_top_campaigns()
        self.refresh_tracking_list()
        try:
            self.refresh_comprehensive_report()
            self.refresh_daily_stats()
            self.refresh_segments()
            self.refresh_health_score()
            self.refresh_suppression_list()
        except:
            pass  # Tabs might not be created yet

def main():
    """Main entry point"""
    print("="*50)
    print("Starting application...")
    print("="*50)
    
    try:
        root = tk.Tk()
        print("[OK] Window created")
        root.title("Email Marketing Pro")
        root.geometry("1400x800")
        root.configure(bg='white')
        
        print("Creating EmailMarketingApp...")
        app = EmailMarketingApp(root)
        print("[OK] App created successfully")
        
        # Force update
        root.update()
        print("[OK] Window updated")
        
        print("="*50)
        print("Starting mainloop...")
        print("="*50)
        root.mainloop()
        print("Mainloop ended")
        
    except Exception as e:
        print("="*50)
        print(f"ERROR: {e}")
        print("="*50)
        import traceback
        traceback.print_exc()
        
        # Try to show error in window
        try:
            error_root = tk.Tk()
            error_root.title("ERROR")
            error_root.geometry("800x600")
            error_root.configure(bg='red')
            
            error_label = tk.Label(error_root, 
                                  text=f"ERROR: {str(e)}", 
                                  fg='white', 
                                  bg='red', 
                                  font=('Arial', 20, 'bold'))
            error_label.pack(pady=50)
            
            traceback_text = tk.Text(error_root, height=20, width=90, bg='white', fg='red', font=('Consolas', 10))
            traceback_text.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
            traceback_text.insert('1.0', traceback.format_exc())
            
            error_root.mainloop()
        except:
            pass
    
    # Stop tracking server on exit
    def on_closing():
        try:
            stop_tracking_server()
        except:
            pass
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    print("Starting mainloop...")
    root.mainloop()
    print("Mainloop ended")

if __name__ == "__main__":
    main()

