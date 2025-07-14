# Reddit Persona Generator

An intelligent system that analyzes Reddit user profiles to generate detailed, professional user personas based on their posts and comments. The system uses Reddit API for data collection and Google's Gemini LLM to generate comprehensive persona reports with evidence-based insights and citations.

## Features

- **Automated Reddit Scraping**: Extracts posts and comments from any public Reddit user profile
- **LLM-Powered Analysis**: Uses Google Gemini to generate complete, professional persona reports
- **Evidence-Based Insights**: Every insight is backed by specific Reddit posts/comments with citations
- **Comprehensive Analysis**: Covers demographics, traits, motivations, personality, behaviors, frustrations, and goals
- **Professional Output**: Generates well-formatted TXT reports with clear sections and bullet points
- **Confidence Assessment**: Each report includes confidence level and data quality evaluation

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Reddit API credentials (free)
- Google Gemini API key (free/premium)

### 1. Clone the Repository
```bash
git clone https://github.com/SamuelAlex013/reddit-persona-generator.git
cd reddit-persona-generator
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Get API Credentials

#### Reddit API Setup:
1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Choose "script" as the app type
4. Fill in the form:
   - **Name**: Your app name (e.g., "PersonaGenerator")
   - **App type**: Script
   - **Description**: Optional
   - **About URL**: Leave blank
   - **Redirect URI**: http://localhost:8080 (required but not used)
5. Click "Create app"
6. Note down:
   - **Client ID**: Found under the app name (short string)
   - **Client Secret**: The longer "secret" string

#### Google Gemini API Setup:
1. Go to https://aistudio.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key

### 4. Configure Environment Variables
Create a `.env` file in the project directory with your credentials:

```env
# Reddit API Configuration
REDDIT_CLIENT_ID=your_reddit_client_id_here
REDDIT_CLIENT_SECRET=your_reddit_client_secret_here
REDDIT_USER_AGENT=PersonaGenerator/1.0 by YourUsername

# Google Gemini API Configuration
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

**Important**: 
- Replace `YourUsername` with your actual Reddit username
- Never commit the `.env` file to version control (already in .gitignore)

## Usage

### Basic Usage
Generate a persona for any Reddit user:

```bash
python reddit_persona_generator.py https://www.reddit.com/user/USERNAME
```

### With Custom Output File
```bash
python reddit_persona_generator.py https://www.reddit.com/user/USERNAME -o custom_persona.txt
```

### Examples
```bash
# Generate persona for a specific user
python reddit_persona_generator.py https://www.reddit.com/user/spez

# Generate with custom filename
python reddit_persona_generator.py https://www.reddit.com/user/spez -o spez_analysis.txt
```

## Output

The tool generates professional persona reports saved in the `persona/` folder as `.txt` files. Each report includes:

- **Demographics**: Age, gender, location, occupation (when inferrable)
- **Traits**: Key personality characteristics
- **Motivations**: What drives the user
- **Personality**: Behavioral patterns and tendencies
- **Behaviors & Habits**: Observable actions and preferences
- **Frustrations**: Common pain points and concerns
- **Goals & Needs**: Objectives and requirements
- **Key Quote**: Representative statement from the user
- **Analysis Summary**: Overall assessment
- **Citations**: Source Reddit posts/comments for each insight
- **Confidence Level**: Assessment of analysis reliability
- **Data Quality**: Evaluation of source data completeness

## Sample Outputs

See the `persona/` folder for example persona reports demonstrating the tool's capabilities.

## Project Structure

```
reddit-persona-generator/
├── reddit_persona_generator.py    # Main executable script
├── persona_generator.py           # Core persona generation logic
├── persona_analyzer.py            # LLM analysis and JSON parsing
├── reddit_scraper.py              # Reddit API data collection
├── config_utils.py                # Configuration and credential management
├── models.py                      # Data models (RedditPost)
├── requirements.txt               # Python dependencies
├── .env                          # API credentials (create this file)
├── .gitignore                    # Git ignore rules
├── persona/                      # Output folder for generated personas
│   ├── sample_user1_persona.txt  # Example persona report
│   ├── sample_user2_persona.txt  # Example persona report
│   └── ...                       # Additional sample reports
└── README.md                     # This file
```

## Troubleshooting

### Common Issues

**Reddit API 401 Error:**
- Verify your Reddit app type is set to "script"
- Check that Client ID and Secret are correct
- Ensure your Reddit account email is verified
- Confirm the user profile exists and is public

**Reddit API 403 Error:**
- The user profile may be private or suspended
- Try with a different public user profile

**Reddit API 404 Error:**
- Username not found - check spelling
- User may have been deleted or banned

**Google API Error:**
- Verify your Gemini API key is correct
- Check your API quota/limits
- Ensure the API key has proper permissions

**Empty Output:**
- User may have no public posts/comments
- Try with a more active Reddit user
- Check if user posts are in non-English languages

### Getting Help

If you encounter issues:
1. Check the error messages carefully
2. Verify all API credentials are correct
3. Test with known public Reddit users
4. Ensure your internet connection is stable

## Technical Details

### Data Collection
- Uses PRAW (Python Reddit API Wrapper) for efficient Reddit data collection
- Scrapes up to 100 recent posts and 100 recent comments per user
- Handles rate limiting and API errors gracefully
- Respects Reddit's API terms of service

### LLM Analysis
- Leverages Google Gemini 2.0 Flash Lite for content analysis
- Uses structured prompts to ensure consistent persona formatting
- Implements evidence-based analysis with citation requirements
- Generates JSON output for reliable parsing
