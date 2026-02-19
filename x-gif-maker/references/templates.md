# GIF Templates

Pre-configured templates for common social media use cases.

## Quick Templates

### Product Announcement
```python
maker.create_text_gif(
    text="Introducing Feature X\nNow with AI-powered automation",
    output_path="announcement.gif",
    style="slide_down",
    bg_colors=["#667eea", "#764ba2"],
    signature="🚀 YourProduct"
)
```

### Quote Post
```python
maker.create_text_gif(
    text='"The only way to do great work\nis to love what you do."\n— Steve Jobs',
    output_path="quote.gif",
    style="fade",
    bg_colors=["#0f0c29", "#302b63"],
    text_color="#00d2ff"
)
```

### Call to Action
```python
maker.create_text_gif(
    text="🔥 Limited Time Offer!\n50% off everything",
    output_path="cta.gif",
    style="pulse",
    bg_colors=["#ff6b6b", "#feca57"],
    duration=3
)
```

### Success Story
```python
maker.create_text_gif(
    text="10,000 Users Reached! 🎉\nThank you for your support",
    output_path="success.gif",
    style="slide_up",
    bg_colors=["#11998e", "#38ef7d"],
    signature="YourCompany"
)
```

### Breaking News
```python
maker.create_text_gif(
    text="BREAKING:\nWe just launched v2.0",
    output_path="news.gif",
    style="shake",
    bg_colors=["#f12711", "#f5af19"],
    duration=2
)
```

### Coming Soon
```python
maker.create_text_gif(
    text="Coming Soon\nSomething amazing is brewing...",
    output_path="teaser.gif",
    style="fade",
    bg_colors=["#0f0f0f", "#1a1a1a"],
    text_color="#ff00ff",
    signature="🔮 Stay tuned"
)
```

### Fun/Casual
```python
maker.create_text_gif(
    text="Oops! We broke something.\nFixing it right now 🛠️",
    output_path="status.gif",
    style="bounce",
    bg_colors=["#ffeaa7", "#fdcb6e"],
    text_color="#2d3436"
)
```

### Developer/Tech
```python
maker.create_text_gif(
    text="New API Released!\n/beta endpoint now live",
    output_path="tech.gif",
    style="typewriter",
    bg_colors=["#0f0f0f", "#2d3436"],
    text_color="#00ff88",
    signature="🤖 nanobot"
)
```

## Business Templates

### Company Announcement
```python
maker.create_text_gif(
    text="We're Hiring! 🎯\nJoin our amazing team",
    output_path="hiring.gif",
    style="slide_down",
    bg_colors=["#667eea", "#764ba2"],
    signature="💼 YourCompany"
)
```

### Feature Release
```python
maker.create_text_gif(
    text="✨ Dark Mode is Here!\nToggle in settings now",
    output_path="feature.gif",
    style="glow",
    bg_colors=["#0f0c29", "#302b63"],
    text_color="#00d2ff"
)
```

### Milestone Achievement
```python
maker.create_text_gif(
    text="1 Million Downloads! 🏆\nThank you for believing in us",
    output_path="milestone.gif",
    style="zoom",
    bg_colors=["#f12711", "#f5af19"],
    signature="🎉 App Name"
)
```

### Partnership Announcement
```python
maker.create_text_gif(
    text="Exciting Partnership!\nWe're teaming up with Partner",
    output_path="partner.gif",
    style="slide_up",
    bg_colors=["#11998e", "#38ef7d"],
    duration=2
)
```

### Event Invitation
```python
maker.create_text_gif(
    text="🎪 Join Our Webinar!\nMarch 15th at 3PM EST",
    output_path="event.gif",
    style="pulse",
    bg_colors=["#c471ed", "#f64f59"],
    signature="📅 Save the date"
)
```

## Social Media Templates

### Twitter/X Post
```python
maker.create_text_gif(
    text="Hot Take:\nAI is a tool, not a replacement.\n\nWhat do you think? 👇",
    output_path="twitter.gif",
    style="fade",
    bg_colors=["#0f0f0f", "#1a1a1a"],
    text_color="#ffffff",
    signature="💭 Thread 🧵"
)
```

### Instagram Story Poll
```python
maker = GifMaker(width=640, height=1136, duration=2)
maker.create_text_gif(
    text="Quick Poll:\n👍 for Yes\n👎 for No",
    output_path="story.gif",
    style="bounce",
    bg_colors=["#ff6b6b", "#feca57"]
)
```

### LinkedIn Thought Leadership
```python
maker.create_text_gif(
    text="Leadership Insight:\nGreat leaders listen more\nthan they speak.",
    output_path="linkedin.gif",
    style="fade",
    bg_colors=["#2193b0", "#6dd5ed"],
    signature="💡 #Leadership"
)
```

### Discord Server Update
```python
maker = GifMaker(width=480, height=270, duration=2)
maker.create_text_gif(
    text="📢 Server Update!\nNew channels added",
    output_path="discord.gif",
    style="shake",
    bg_colors=["#7289da", "#5865F2"],
    signature="🎮 Game On"
)
```

### TikTok Hook
```python
maker = GifMaker(width=720, height=1280, duration=2)
maker.create_text_gif(
    text="Wait for it... 👀\n\n#fyp #viral",
    output_path="tiktok.gif",
    style="zoom",
    bg_colors=["#00c6ff", "#0072ff"]
)
```

## Tech/Developer Templates

### Version Release
```python
maker.create_text_gif(
    text="v3.0 Released! 🚀\n\nBreaking changes ahead",
    output_path="release.gif",
    style="glitch",
    bg_colors=["#0f0f0f", "#1a1a1a"],
    text_color="#00ff88"
)
```

### Bug Fix Announcement
```python
maker.create_text_gif(
    text="🐛 Bug Squashed!\n\nFixed the login issue.\nUpdate now!",
    output_path="bugfix.gif",
    style="bounce",
    bg_colors=["#ff6b6b", "#feca57"]
)
```

### Security Update
```python
maker.create_text_gif(
    text="🔒 Security Update!\n\nUpdate to v2.1.5\nto patch vulnerabilities.",
    output_path="security.gif",
    style="shake",
    bg_colors=["#f12711", "#f5af19"],
    duration=3
)
```

### API Documentation
```python
maker.create_text_gif(
    text="API Docs Updated!\n\nNew endpoints added.\nCheck the docs. 📚",
    output_path="api.gif",
    style="typewriter",
    bg_colors=["#0f0f0f", "#2d3436"],
    text_color="#00ff88"
)
```

### Open Source Contribution
```python
maker.create_text_gif(
    text="⭐ Thanks Contributors!\n\n100+ PRs merged this month.",
    output_path="oss.gif",
    style="slide_up",
    bg_colors=["#11998e", "#38ef7d"],
    signature="🙏 Open Source"
)
```

## Marketing Templates

### Flash Sale
```python
maker.create_text_gif(
    text="⚡ FLASH SALE!\n\n50% OFF - 24 HOURS ONLY!",
    output_path="sale.gif",
    style="pulse",
    bg_colors=["#ff6b6b", "#feca57"],
    duration=3,
    signature="🛒 Shop Now"
)
```

### Product Showcase
```python
maker.create_text_gif(
    text="Meet Product X\n\nThe future of productivity.",
    output_path="product.gif",
    style="glow",
    bg_colors=["#667eea", "#764ba2"],
    text_color="#ffffff"
)
```

### Testimonial Highlight
```python
maker.create_text_gif(
    text='"Best tool ever!"\n- Happy Customer ⭐⭐⭐⭐⭐',
    output_path="testimonial.gif",
    style="fade",
    bg_colors=["#2c3e50", "#4ca1af"],
    signature="💬 5000+ Reviews"
)
```

### Newsletter Signup
```python
maker.create_text_gif(
    text="Subscribe! 📧\n\nGet weekly insights\ndelivered to your inbox.",
    output_path="newsletter.gif",
    style="slide_down",
    bg_colors=["#9d50bb", "#6e48aa"],
    signature="📬 No spam, ever"
)
```

### Brand Awareness
```python
maker.create_text_gif(
    text="YourBrand\n\nEmpowering creators worldwide.",
    output_path="brand.gif",
    style="wave",
    bg_colors=["#c471ed", "#f64f59"],
    duration=3
)
```

## Personal Templates

### Birthday Wish
```python
maker.create_text_gif(
    text="Happy Birthday! 🎂\n\nHave an amazing day!",
    output_path="birthday.gif",
    style="bounce",
    bg_colors=["#ff6b6b", "#feca57"]
)
```

### Thank You Message
```python
maker.create_text_gif(
    text="Thank You! 🙏\n\nFor all your support.",
    output_path="thanks.gif",
    style="fade",
    bg_colors=["#11998e", "#38ef7d"],
    signature="💝 Grateful"
)
```

### Motivation Quote
```python
maker.create_text_gif(
    text='"Dream big, work hard,\nstay humble."\n\n— Unknown',
    output_path="motivation.gif",
    style="slide_up",
    bg_colors=["#2193b0", "#6dd5ed"]
)
```

### Monday Motivation
```python
maker.create_text_gif(
    text="Monday Mindset:\n\nNew week, new goals.\nLet's crush it! 💪",
    output_path="monday.gif",
    style="zoom",
    bg_colors=["#f12711", "#f5af19"]
)
```

### Weekend Vibes
```python
maker.create_text_gif(
    text="Weekend Mode: ON 😎\n\nRecharge & reflect.",
    output_path="weekend.gif",
    style="wave",
    bg_colors=["#ff6b6b", "#feca57"],
    duration=3
)
```

## Seasonal Templates

### Holiday Special
```python
maker.create_text_gif(
    text="🎄 Holiday Special!\n\nAll products 40% off",
    output_path="holiday.gif",
    style="pulse",
    bg_colors=["#c0392b", "#e74c3c"],
    signature="🎁 Happy Holidays"
)
```

### New Year
```python
maker.create_text_gif(
    text="Happy New Year! 🎊\n\n2026 is going to be amazing!",
    output_path="newyear.gif",
    style="zoom",
    bg_colors=["#0f0c29", "#302b63"],
    signature="✨ Cheers!"
)
```

### Spring Promotion
```python
maker.create_text_gif(
    text="🌸 Spring Sale!\n\nFresh deals blooming now",
    output_path="spring.gif",
    style="slide_up",
    bg_colors=["#11998e", "#38ef7d"]
)
```

### Summer Vibes
```python
maker.create_text_gif(
    text="☀️ Summer Savings!\n\nHot deals, cool prices",
    output_path="summer.gif",
    style="bounce",
    bg_colors=["#ff6b6b", "#feca57"]
)
```

### Halloween Special
```python
maker.create_text_gif(
    text="🎃 Halloween Special!\n\nSpooky deals inside",
    output_path="halloween.gif",
    style="glitch",
    bg_colors=["#0f0f0f", "#1a1a1a"],
    text_color="#ff6600"
)
```

## Customization Tips

### Adding Emojis
Use Unicode emojis directly in text:
- `"🚀 Launching now!"`
- `"🎉 10K users!"`
- `"⚡ Speed update"`
- `"🐛 Bug fixed!"`

### Multi-line Text
Use `\n` for line breaks:
- `"Line 1\nLine 2\nLine 3"`

### Signature Branding
Add your brand at the bottom:
- `signature="🤖 @yourhandle"`
- `signature="🚀 YourProduct"`
- `signature="💼 YourCompany"`
- `signature="📚 Read more"`

### Duration Tuning
- **1 second**: Quick updates, status messages
- **2 seconds**: Standard announcements (recommended)
- **3 seconds**: Call-to-actions, important messages

### Font Sizing
Adjust font size for impact:
```python
# Large text for impact
maker = GifMaker(font_size=48)

# Medium text (default)
maker = GifMaker(font_size=36)

# Small text for more content
maker = GifMaker(font_size=28)
```

### Platform-Specific
```python
# X/Twitter
maker = GifMaker(width=640, height=360)

# Instagram Story
maker = GifMaker(width=640, height=1136)

# Instagram Square
maker = GifMaker(width=640, height=640)

# Discord
maker = GifMaker(width=480, height=270)

# TikTok
maker = GifMaker(width=720, height=1280)
```

### Logo Branding
Add your logo to any template:
```python
maker.create_text_gif(
    text="Your text",
    output_path="branded.gif",
    logo_path="logo.png",
    logo_position="bottom-right"
)
```

Available logo positions:
- `top-left`
- `top-right`
- `bottom-left`
- `bottom-right`
- `center`
