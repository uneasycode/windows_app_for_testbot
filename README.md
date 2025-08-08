# user_guide.md - Complete User Guide for Windows Desktop App

# Telegram Bot Manager - Windows Desktop Application User Guide

## 🚀 Quick Start Guide

### Step 1: Download & Setup
1. Download the `TelegramBotManager_Portable` folder
2. Extract to your desired location (e.g., `C:\TelegramBot\`)
3. Open the `.env` file in a text editor
4. Configure your Telegram API credentials:

```
API_ID=your_api_id_here
API_HASH=your_api_hash_here  
PHONE=+1234567890
```

### Step 2: Get Telegram API Credentials
1. Visit https://my.telegram.org
2. Log in with your phone number
3. Go to "API development tools"
4. Create a new application
5. Copy your **API_ID** and **API_HASH**

### Step 3: Run the Application
1. Double-click `TelegramBotManager.exe` 
2. OR run `start.bat` for easier launching
3. The desktop application will open with 5 main tabs

## 📱 Application Interface

### 🤖 Bot Control Tab
**Start/Stop Your Bot**
- **Green Status**: Bot is running and connected
- **Red Status**: Bot is stopped
- **Orange Status**: Bot is starting/connecting

**Statistics Dashboard**
- Total responses configured
- Messages processed today  
- Media files available
- Configuration validation status

**Quick Actions**
- Start Bot: Connect to Telegram and begin responding
- Stop Bot: Disconnect and stop all bot activities

### 💬 Response Management Tab
**Manage Bot Responses**
- **View All Responses**: See keywords, types, and content previews
- **Add New Response**: Create text, image, or audio responses
- **Edit Response**: Modify existing bot responses
- **Delete Response**: Remove unwanted responses

**Response Types Supported**
- **Text**: Multiple text responses (bot picks randomly)
- **Image**: Send image files with optional captions
- **Audio**: Send audio files as voice messages

**Creating Responses**
1. Click "➕ Add Response"
2. Enter trigger keyword (what users type)
3. Select response type
4. Configure content:
   - **Text**: Enter multiple lines for variety
   - **Image**: Select from uploaded images + add caption
   - **Audio**: Select from uploaded audio files

### 📁 Media Files Tab
**Upload & Manage Media**
- **Upload Images**: JPG, PNG, GIF, BMP files
- **Upload Audio**: MP3, WAV, OGG, M4A files
- **View File Details**: Filename, type, and size
- **Delete Files**: Remove unused media

**File Management Tips**
- Upload images first, then create image responses
- Keep file sizes reasonable (<5MB for images, <10MB for audio)
- Use descriptive filenames for easy identification

### 📨 Live Messages Tab
**Real-Time Message Monitoring**
- **Incoming Messages**: Blue text shows messages received
- **Outgoing Responses**: Green text shows bot replies
- **System Events**: Red text shows errors and status updates
- **Timestamps**: Gray text shows when messages occurred

**Message Log Features**
- **Auto-scroll**: Automatically scroll to newest messages
- **Clear Log**: Remove all messages from display
- **Save Log**: Export conversation history to text file
- **Search & Filter**: Find specific messages or events

### ⚙️ Settings Tab
**API Configuration**
- Edit your Telegram credentials
- Test connection status
- Update phone number if needed

**Application Settings**
- **Auto-start Bot**: Automatically start bot when app opens
- **Minimize to Tray**: Hide app in system tray instead of taskbar
- **Message Notifications**: Show popup notifications for new messages

**System Tray Integration**
- Right-click tray icon for quick actions
- Start/stop bot from tray menu
- Show/hide main window
- Exit application

## 🔧 Advanced Features

### Message Monitoring & Logging
The application automatically logs all bot activities:
- **Incoming user messages**: What people send to your bot
- **Outgoing bot responses**: How your bot replies
- **System events**: Start/stop, errors, configuration changes
- **Unknown messages**: Messages that didn't match any response

### NLP (Natural Language Processing)
Your bot includes intelligent message matching:
- **Exact matches**: Direct keyword matching
- **Wildcard matching**: Use `*` in keywords (e.g., `hello*` matches "hello", "hello there")
- **Fuzzy matching**: Handles typos and similar phrases
- **Hinglish support**: Understands mixed Hindi-English messages

### Response Patterns
**Text Responses**
```json
{
  "hello": {
    "type": "text",
    "content": ["Hi there!", "Hello! How can I help?", "Hey!"]
  }
}
```

**Image Responses**
```json
{
  "show photo": {
    "type": "image", 
    "content": "my_image.jpg",
    "caption": "Here's the photo you requested!"
  }
}
```

**Audio Responses**
```json
{
  "play music": {
    "type": "audio",
    "content": "song.mp3"
  }
}
```

## 🚨 Troubleshooting

### Bot Won't Start
**Check Configuration**
1. Verify API_ID and API_HASH in `.env` file
2. Ensure phone number includes country code (+1234567890)
3. Test internet connection
4. Check Windows firewall settings

**Common Solutions**
- Restart the application
- Re-enter API credentials
- Check Telegram app on your phone for verification codes

### Messages Not Working
**Response Issues**
1. Check that bot status shows "Running" (green)
2. Verify responses.json has valid entries
3. Test with simple text responses first
4. Check Live Messages tab for error details

**Media Not Sending**
1. Verify media files exist in `media/images/` or `media/audio/` folders
2. Check file formats are supported
3. Ensure file sizes are reasonable (<5MB images, <10MB audio)

### System Tray Problems
**If tray integration fails**
1. Disable "Minimize to tray" in Settings
2. Check Windows notification area settings
3. Some antivirus software blocks tray access

### Performance Issues
**If application is slow**
1. Clear message log regularly
2. Remove unused media files
3. Limit number of responses to reasonable amount
4. Close other resource-intensive applications

## 📋 File Structure

```
TelegramBotManager_Portable/
├── TelegramBotManager.exe    # Main application executable
├── .env                      # Your API configuration (KEEP PRIVATE!)
├── responses.json            # Bot responses database  
├── conversation.json         # Message history log
├── bot.log                   # Technical error log
├── start.bat                # Easy launcher script
├── README.txt               # Quick reference guide
└── media/
    ├── images/              # Image files for image responses
    └── audio/               # Audio files for audio responses
```

## 🔒 Security & Privacy

### Keep Your Credentials Safe
- **Never share** your `.env` file
- **Don't commit** credentials to version control
- **Use strong** unique API hash
- **Rotate credentials** if compromised

### Data Protection
- All messages are logged locally only
- No data is sent to external servers (except Telegram API)
- Media files stored locally on your computer
- Configuration files remain on your device

## 🆘 Support & Help

### Getting Help
1. **Check Live Messages tab** for real-time error details
2. **Review bot.log file** for technical error information  
3. **Verify configuration** in Settings tab
4. **Test with simple responses** before complex setups

### Common Error Messages
- **"API_ID not configured"**: Missing or invalid API credentials
- **"Phone number verification needed"**: Check Telegram app for code
- **"File not found"**: Media file missing or moved
- **"Invalid response format"**: Check responses.json syntax

### Best Practices
- **Start simple**: Begin with text responses before adding media
- **Test thoroughly**: Verify each response works before adding more
- **Regular backups**: Keep copies of your responses.json file
- **Monitor actively**: Use Live Messages tab to watch bot performance

## 🎯 Pro Tips

### Optimize Bot Performance
- Use specific keywords rather than generic ones
- Create response variations for more natural conversations
- Organize media files with descriptive names
- Monitor message patterns to improve responses

### Advanced Response Patterns
- Use wildcards for flexible matching: `help*` matches "help", "help me", "help please"
- Create contextual responses based on user sentiment
- Combine text and media responses for rich interactions
- Use conversation.json to analyze popular requests

### Automation Ideas
- Set up auto-start for always-on bot operation
- Use system tray for invisible background operation
- Create scheduled responses (requires custom scripting)
- Integration with other Windows applications

---

*This guide covers the complete functionality of Telegram Bot Manager v2.0. For additional support, refer to the in-app help sections and log files.*