# 📧 Email Marketing Suite ✉️

Professional Email Marketing Desktop Application with GUI 🚀

---

## 🌟 Overview

Welcome to **Email Marketing Suite** - a powerful, comprehensive desktop application for managing your email marketing campaigns. Built with Python and Tkinter, this application provides a user-friendly interface with all the tools you need to run successful email marketing campaigns.

Whether you're a small business owner, marketing professional, or enterprise team, our suite has everything you need to engage with your audience effectively.

---

## 🎯 Features

### 👥 Contact Management
- 📥 Import contacts from CSV, Excel, and text files
- 📤 Export contacts to various formats
- 🔍 Search and filter contacts
- 🏷️ Tag-based organization
- 📊 Contact segmentation
- ✅ Duplicate detection and removal
- 📈 Contact activity tracking

### 📨 Campaign Management
- ✨ Create rich HTML and plain-text emails
- ⏰ Schedule campaigns for future delivery
- 📋 Draft and save campaigns
- 🚀 Send immediately or schedule
- 📊 Track campaign performance
- 🔄 A/B testing support
- 📝 Multi-variant testing

### 📝 Template Management
- 🎨 Pre-designed email templates
- 🖌️ Custom template creation
- 📑 Template categorization
- 🔄 Template reuse
- 🖼️ Image and logo support
- 📱 Responsive design templates

### 📊 Tracking & Analytics
- 👁️ Email open tracking
- 🔗 Click tracking
- 📉 Bounce rate monitoring
- ⏱️ Delivery time analytics
- 📈 Conversion tracking
- 📊 Interactive dashboards
- 📑 Detailed reports

### 🔄 Bounce Handling
- ⚠️ Automatic bounce detection
- 🔧 Hard bounce management
- 💧 Soft bounce handling
- 📋 Bounce report generation
- 🗑️ Automatic list cleanup
- 📊 Bounce analytics

### 🚫 Unsubscribe Handling
- 🔗 One-click unsubscribe links
- ⚙️ Automatic unsubscribe processing
- 📋 Unsubscribe tracking
- ✅ Compliance with email regulations
- 📊 Unsubscribe analytics

### 🎯 Segmentation
- 🎨 Dynamic segment creation
- 🔍 Advanced filtering rules
- 🏷️ Tag-based segmentation
- 📊 Behavioral segmentation
- ⏰ Time-based segmentation
- 🔄 Real-time segment updates

### 📈 Reports & Analytics
- 📊 Campaign performance reports
- 📈 ROI calculations
- 📉 Trend analysis
- 📋 Export to PDF/CSV
- 📊 Visual charts and graphs
- 🕐 Custom date ranges

### 🧹 List Hygiene
- ✨ Email validation
- ❌ Remove invalid emails
- 🔍 Duplicate removal
- 🗑️ Spam trap detection
- 📋 List health score
- 🧼 List cleaning wizard
- 📊 Hygiene reports

### ✅ Compliance
- 🛡️ GDPR compliance tools
- 📜 CAN-SPAM compliance
- 📋 Consent management
- 🔏 Data export/erasure
- 📊 Compliance reports
- ✅ Double opt-in support

### 🌍 Multi-language Support
- 🌐 Multiple language interface
- 🗣️ Email content translation
- 📝 Template localization
- 🔄 Language switching

### 🔧 Professional Tools
- 🔌 SMTP provider integration
- 📡 API connections
- 🔒 Secure credentials storage
- ⚙️ Custom settings
- 📊 Bulk operations
- 🔄 Automation workflows

---

## 🛠️ Requirements

| Requirement | Version |
|-------------|---------|
| 🐍 Python | 3.8+ |
| 🗄️ SQLAlchemy | Latest |
| 📄 Jinja2 | Latest |
| 🔐 python-dotenv | Latest |
| 🖥️ Tkinter | (included with Python) |

---

## 💻 Installation

### Step 1: Clone or Download
```bash
git clone https://github.com/zougar99/Email-Marketing-Suite.git
cd Email-Marketing-Suite
```

### Step 2: Install Dependencies
```bash
pip install sqlalchemy jinja2 python-dotenv
```

### Step 3: Run the Application
```bash
python app.py
```

---

## ▶️ Usage

### Getting Started

1. **Launch the Application**
   ```bash
   python app.py
   ```

2. **Configure SMTP Settings**
   - Go to Settings
   - Enter your SMTP credentials
   - Test the connection

3. **Import Contacts**
   - Click "Contacts" tab
   - Click "Import"
   - Select your file format

4. **Create a Campaign**
   - Click "Campaigns" tab
   - Click "New Campaign"
   - Select template or create new
   - Choose recipients
   - Send or schedule

---

## 📁 Project Structure

```
Email-Marketing-Suite/
├── 📄 app.py              # Main application
├── 📄 database.py         # Database management
├── 📄 config.py           # Configuration
├── 📄 contact_manager.py  # Contact management
├── 📄 campaign_manager.py # Campaign management
├── 📄 template_manager.py # Template management
├── 📄 email_sender.py     # Email sending
├── 📄 tracking_server.py  # Tracking server
├── 📄 tracking_hash.py    # Tracking hashes
├── 📄 bounce_handler.py   # Bounce handling
├── 📄 unsubscribe_handler.py # Unsubscribe handling
├── 📄 segment_manager.py  # Segmentation
├── 📄 reports_manager.py # Reports
├── 📄 list_hygiene.py    # List hygiene
├── 📄 advanced_segmentation.py # Advanced segmentation
├── 📄 compliance_manager.py # Compliance
├── 📄 multi_language_support.py # Multi-language
├── 📄 professional_tools_library.py # Professional tools
├── 📄 smtp_providers.py  # SMTP providers
├── 📄 ab_testing.py      # A/B testing
├── 📄 analytics.py       # Analytics
├── 📄 README.md          # Documentation
└── 📄 email_marketing.db # SQLite database
```

---

## 💾 Database

The application uses **SQLite** database (`email_marketing.db`) for data storage:

- 📊 Contacts table
- 📬 Campaigns table
- 📨 Campaign recipients table
- 👁️ Email opens table
- 🔗 Email clicks table
- ⚠️ Bounces table
- 🚫 Unsubscribes table
- 📝 Templates table
- 🎯 Segments table

---

## 🔧 Configuration

Create a `.env` file in the project root:

```env
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USERNAME=your@email.com
SMTP_PASSWORD=your_password
SMTP_USE_TLS=True
```

---

## 🆘 Troubleshooting

### Common Issues

**Q: Application won't start**
- ✅ Check Python version (3.8+)
- ✅ Install all dependencies

**Q: Can't send emails**
- ✅ Check SMTP settings
- ✅ Verify network connection
- ✅ Check credentials

**Q: Database errors**
- ✅ Delete `email_marketing.db` and restart
- ✅ Check file permissions

---

## 📝 License

This project is for educational and personal use.

---

## 👨‍💻 Author

Created with ❤️

---

## 🙏 Acknowledgments

Thank you for using Email Marketing Suite!

🌟 Star the project if you found it useful!
