import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, date
import random

# Page configuration
st.set_page_config(
    page_title="IELTS Progress Tracker",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Data persistence functions
DATA_FILE = "ielts_data.json"

def load_data():
    """Load data from JSON file"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
                # Convert date strings back to date objects where needed
                if 'target_date' in data:
                    data['target_date'] = datetime.strptime(data['target_date'], '%Y-%m-%d').date()
                return data
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return get_default_data()
    return get_default_data()

def save_data():
    """Save data to JSON file"""
    try:
        data_to_save = {
            'scores': st.session_state.scores,
            'target_date': st.session_state.target_date.strftime('%Y-%m-%d')
        }
        with open(DATA_FILE, 'w') as f:
            json.dump(data_to_save, f, indent=2)
    except Exception as e:
        st.error(f"Error saving data: {e}")

def get_default_data():
    """Get default data structure"""
    return {
        'scores': {
            'listening': [],
            'reading': [],
            'writing': [],
            'speaking': []
        },
        'target_date': date(2025, 11, 1)
    }

# Initialize session state with persistent data
if 'initialized' not in st.session_state:
    saved_data = load_data()
    st.session_state.scores = saved_data['scores']
    st.session_state.target_date = saved_data['target_date']
    st.session_state.initialized = True

# Professional Dark Theme CSS (keeping your existing styles)
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main App Styling */
    .stApp {
        background-color: #0E1117;
        font-family: 'Inter', sans-serif;
    }
    
    .main > div {
        background-color: #0E1117;
    }
    
    /* Custom metric cards */
    .metric-card {
        background: linear-gradient(135deg, #1E2329 0%, #2B2F36 100%);
        border: 1px solid #3A3F47;
        border-radius: 12px;
        padding: 24px;
        margin: 8px 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
        border-color: #4F46E5;
    }
    
    .metric-title {
        color: #9CA3AF;
        font-size: 14px;
        font-weight: 500;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .metric-value {
        color: #F9FAFB;
        font-size: 32px;
        font-weight: 700;
        line-height: 1;
        margin-bottom: 8px;
    }
    
    .metric-subtitle {
        color: #6B7280;
        font-size: 13px;
        font-weight: 400;
    }
    
    /* Countdown Timer */
    .countdown-container {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
        border-radius: 16px;
        padding: 32px;
        text-align: center;
        margin: 24px 0;
        box-shadow: 0 10px 30px rgba(79, 70, 229, 0.3);
    }
    
    .countdown-days {
        color: #FFFFFF;
        font-size: 48px;
        font-weight: 800;
        line-height: 1;
        margin-bottom: 8px;
    }
    
    .countdown-label {
        color: #E0E7FF;
        font-size: 16px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    
    .countdown-date {
        color: #C7D2FE;
        font-size: 14px;
        margin-top: 8px;
    }
    
    /* Quote box */
    .quote-container {
        background: linear-gradient(135deg, #059669 0%, #0D9488 100%);
        border-radius: 12px;
        padding: 24px;
        margin: 16px 0;
        position: relative;
        overflow: hidden;
    }
    
    .quote-container::before {
        content: '"';
        position: absolute;
        top: -10px;
        left: 16px;
        font-size: 120px;
        color: rgba(255, 255, 255, 0.1);
        font-family: Georgia, serif;
    }
    
    .quote-text {
        color: #FFFFFF;
        font-size: 18px;
        font-weight: 500;
        line-height: 1.6;
        position: relative;
        z-index: 1;
    }
    
    /* Page title */
    .main-title {
        color: #F9FAFB;
        font-size: 40px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 32px;
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 50%, #06B6D4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Test entries */
    .test-entry {
        background-color: #1F2937;
        border: 1px solid #374151;
        border-radius: 8px;
        padding: 16px;
        margin: 8px 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: all 0.2s ease;
    }
    
    .test-entry:hover {
        background-color: #252C3A;
        border-color: #4B5563;
    }
    
    .test-info {
        color: #F9FAFB;
        font-weight: 500;
    }
    
    .test-meta {
        color: #9CA3AF;
        font-size: 14px;
        margin-top: 4px;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #111827;
    }
    
    /* Section headers */
    .section-header {
        color: #F9FAFB;
        font-size: 24px;
        font-weight: 600;
        margin: 32px 0 16px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid #374151;
    }
    
    /* Status indicators */
    .status-excellent { color: #10B981; }
    .status-good { color: #3B82F6; }
    .status-average { color: #F59E0B; }
    .status-needs-work { color: #EF4444; }
    
    /* Save status indicator */
    .save-status {
        position: fixed;
        top: 10px;
        right: 10px;
        background: #059669;
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 12px;
        z-index: 1000;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main-title { font-size: 32px; }
        .countdown-days { font-size: 36px; }
        .metric-value { font-size: 28px; }
    }
</style>
""", unsafe_allow_html=True)

# Motivational quotes (keeping your existing quotes)
quotes = [
    "Success is the sum of small efforts, repeated day in and day out.",
    "Every expert was once a beginner. Keep practicing!",
    "Your limitation—it's only your imagination. Break through!",
    "Push yourself, because no one else is going to do it for you.",
    "Great things never come from comfort zones. Step up!",
    "Dream it. Wish it. Do it. Achieve your IELTS goals!",
    "The harder you work for something, the greater you'll feel when you achieve it.",
    "Success doesn't just find you. You have to go out and get it.",
    "Don't stop when you're tired. Stop when you're done!",
    "Wake up with determination. Go to bed with satisfaction."
]

# Helper Functions (keeping your existing functions)
def calculate_days_left():
    today = date.today()
    days_left = (st.session_state.target_date - today).days
    return max(0, days_left)

def get_daily_quote():
    random.seed(date.today().toordinal())
    return random.choice(quotes)

def add_score(test_type, score, test_date, test_time):
    test_id = f"{test_date.strftime('%Y-%m-%d')}_{test_time}_{len(st.session_state.scores[test_type])}"
    
    st.session_state.scores[test_type].append({
        'id': test_id,
        'date': test_date.strftime('%Y-%m-%d'),
        'time': test_time,
        'score': score,
        'datetime': f"{test_date.strftime('%Y-%m-%d')} {test_time}"
    })
    
    st.session_state.scores[test_type].sort(key=lambda x: x['datetime'])
    save_data()  # Auto-save after adding

def remove_score(test_type, test_id):
    st.session_state.scores[test_type] = [
        item for item in st.session_state.scores[test_type] 
        if item['id'] != test_id
    ]
    save_data()  # Auto-save after removing

def create_progress_chart_data(test_type):
    if not st.session_state.scores[test_type]:
        return None
    
    data = st.session_state.scores[test_type]
    df = pd.DataFrame({
        'Test': [f"Test {i+1}" for i in range(len(data))],
        'Date': [item['date'] for item in data],
        'Score': [item['score'] for item in data],
    })
    return df

def get_latest_score(test_type):
    if st.session_state.scores[test_type]:
        return st.session_state.scores[test_type][-1]['score']
    return 0

def get_average_score(test_type):
    if st.session_state.scores[test_type]:
        scores = [item['score'] for item in st.session_state.scores[test_type]]
        return round(sum(scores) / len(scores), 1)
    return 0

def get_best_score(test_type):
    if st.session_state.scores[test_type]:
        scores = [item['score'] for item in st.session_state.scores[test_type]]
        return max(scores)
    return 0

def get_score_status(score):
    if score >= 7.5:
        return "status-excellent", "🔥 Excellent"
    elif score >= 7.0:
        return "status-good", "🎯 Target Reached"
    elif score >= 6.0:
        return "status-average", "📈 Good Progress"
    elif score > 0:
        return "status-needs-work", "💪 Keep Practicing"
    else:
        return "status-needs-work", "📚 Start Testing"

def display_test_entries(test_type):
    if st.session_state.scores[test_type]:
        recent_tests = list(reversed(st.session_state.scores[test_type][-5:]))
        
        for entry in recent_tests:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"""
                <div class="test-entry">
                    <div>
                        <div class="test-info">Score: {entry['score']} • {entry['date']}</div>
                        <div class="test-meta">Time: {entry['time']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button("🗑️", key=f"remove_{entry['id']}", help="Delete this entry", type="secondary"):
                    remove_score(test_type, entry['id'])
                    st.rerun()

# Main Application
st.markdown('<h1 class="main-title">🎯 IELTS Progress Tracker</h1>', unsafe_allow_html=True)

# Show save status
if os.path.exists(DATA_FILE):
    st.markdown('<div class="save-status">💾 Data Auto-Saved</div>', unsafe_allow_html=True)

# Countdown Timer
days_left = calculate_days_left()
st.markdown(f'''
<div class="countdown-container">
    <div class="countdown-days">{days_left}</div>
    <div class="countdown-label">Days Until IELTS</div>
    <div class="countdown-date">{st.session_state.target_date.strftime("%B %d, %Y")}</div>
</div>
''', unsafe_allow_html=True)

# Daily Quote
daily_quote = get_daily_quote()
st.markdown(f'''
<div class="quote-container">
    <div class="quote-text">{daily_quote}</div>
</div>
''', unsafe_allow_html=True)

# Sidebar for adding scores
st.sidebar.markdown("### 📝 Add New Test Score")

test_type = st.sidebar.selectbox(
    "Test Type",
    ['listening', 'reading', 'writing', 'speaking'],
    format_func=lambda x: f"🎧 {x.title()}" if x == 'listening' 
    else f"📖 {x.title()}" if x == 'reading'
    else f"✍️ {x.title()}" if x == 'writing'
    else f"🗣️ {x.title()}"
)

# Score options from 5.0 to 9.0 in 0.5 increments
score_options = [i/2 for i in range(10, 19)]  # 5.0, 5.5, 6.0, ..., 9.0
score_labels = [str(float(score)) for score in score_options]

score = st.sidebar.selectbox(
    "Score",
    options=score_options,
    format_func=lambda x: f"{x} ⭐",
    index=2  # Default to 6.0
)

test_date = st.sidebar.date_input(
    "Test Date",
    value=date.today(),
    help="When did you take this test?"
)

test_time = st.sidebar.time_input(
    "Test Time",
    value=datetime.now().time(),
    help="What time did you take the test?"
).strftime("%H:%M")

if st.sidebar.button("➕ Add Score", type="primary", use_container_width=True):
    add_score(test_type, score, test_date, test_time)
    st.sidebar.success(f"Added {test_type} score: {score}")
    st.rerun()

st.sidebar.markdown("---")

# Target date settings
st.sidebar.markdown("### 🎯 Exam Settings")
new_target = st.sidebar.date_input(
    "IELTS Exam Date",
    value=st.session_state.target_date,
    help="When is your actual IELTS exam?"
)

if st.sidebar.button("Update Exam Date", use_container_width=True):
    st.session_state.target_date = new_target
    save_data()  # Save after updating target date
    st.sidebar.success("Exam date updated!")
    st.rerun()

# Data management section
st.sidebar.markdown("---")
st.sidebar.markdown("### 💾 Data Management")

# Export data
if st.sidebar.button("📤 Export Data", use_container_width=True):
    data_to_export = {
        'scores': st.session_state.scores,
        'target_date': st.session_state.target_date.strftime('%Y-%m-%d'),
        'exported_at': datetime.now().isoformat()
    }
    st.sidebar.download_button(
        label="💾 Download JSON File",
        data=json.dumps(data_to_export, indent=2),
        file_name=f"ielts_progress_{date.today().strftime('%Y%m%d')}.json",
        mime="application/json",
        use_container_width=True
    )

# Clear all data (with confirmation)
if st.sidebar.button("🗑️ Clear All Data", type="secondary", use_container_width=True):
    if 'confirm_clear' not in st.session_state:
        st.session_state.confirm_clear = False
    
    if not st.session_state.confirm_clear:
        st.session_state.confirm_clear = True
        st.sidebar.error("⚠️ Click again to confirm deletion!")
    else:
        # Clear data
        st.session_state.scores = get_default_data()['scores']
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
        st.session_state.confirm_clear = False
        st.sidebar.success("All data cleared!")
        st.rerun()

# Main Dashboard - Score Cards (keeping all your existing dashboard code)
st.markdown('<div class="section-header">📊 Current Performance</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
test_types = ['listening', 'reading', 'writing', 'speaking']
test_icons = ['🎧', '📖', '✍️', '🗣️']

for i, (test, icon) in enumerate(zip(test_types, test_icons)):
    with [col1, col2, col3, col4][i]:
        latest = get_latest_score(test)
        average = get_average_score(test)
        best = get_best_score(test)
        total_tests = len(st.session_state.scores[test])
        
        status_class, status_text = get_score_status(latest)
        
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-title">{icon} {test.title()}</div>
            <div class="metric-value">{latest if latest > 0 else "—"}</div>
            <div class="metric-subtitle">
                Best: {best if best > 0 else "—"} • Avg: {average if average > 0 else "—"}<br>
                <span class="{status_class}">{status_text}</span> • {total_tests} tests
            </div>
        </div>
        ''', unsafe_allow_html=True)

# Progress Charts Section
st.markdown('<div class="section-header">📈 Progress Analysis</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(['🎧 Listening', '📖 Reading', '✍️ Writing', '🗣️ Speaking'])
tabs = [tab1, tab2, tab3, tab4]

for i, (tab, test) in enumerate(zip(tabs, test_types)):
    with tab:
        chart_data = create_progress_chart_data(test)
        
        if chart_data is not None and not chart_data.empty:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Progress Chart**")
                
                # Create chart with better styling
                chart_df = chart_data.set_index('Test')
                st.line_chart(
                    chart_df['Score'], 
                    height=400,
                    use_container_width=True
                )
                
                # Progress insights
                if len(chart_data) > 1:
                    improvement = chart_data['Score'].iloc[-1] - chart_data['Score'].iloc[0]
                    if improvement > 0:
                        st.success(f"📈 **+{improvement}** points improvement!")
                    elif improvement < 0:
                        st.warning(f"📉 **{improvement}** points since first test")
                    else:
                        st.info("📊 **Stable** performance")
            
            with col2:
                st.markdown("**Target Reference**")
                st.markdown("🎯 **Band 7.0** - Target Score")
                st.markdown("🔥 **Band 7.5+** - Excellent")
                st.markdown("📈 **Band 6.5** - Good Progress")
                st.markdown("💪 **Band 6.0** - Keep Going")
                
                st.markdown("**Recent Tests**")
                display_test_entries(test)
        else:
            st.info(f"No {test} scores yet. Add your first test score using the sidebar! 👈")

# Overall Summary (keeping your existing summary code)
st.markdown('<div class="section-header">🏆 Overall Summary</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    all_scores = []
    for test in test_types:
        if st.session_state.scores[test]:
            scores = [item['score'] for item in st.session_state.scores[test]]
            all_scores.extend(scores)
    
    overall_avg = round(sum(all_scores) / len(all_scores), 1) if all_scores else 0
    total_tests = sum(len(st.session_state.scores[test]) for test in test_types)
    
    status_class, status_text = get_score_status(overall_avg)
    
    st.markdown(f'''
    <div class="metric-card">
        <div class="metric-title">🎯 Overall Average</div>
        <div class="metric-value">{overall_avg if overall_avg > 0 else "—"}</div>
        <div class="metric-subtitle">
            <span class="{status_class}">{status_text}</span><br>
            {total_tests} total tests completed
        </div>
    </div>
    ''', unsafe_allow_html=True)

with col2:
    # Calculate readiness
    ready_count = sum(1 for test in test_types if get_latest_score(test) >= 7.0)
    readiness_pct = (ready_count / 4) * 100 if ready_count > 0 else 0
    
    st.markdown(f'''
    <div class="metric-card">
        <div class="metric-title">🚀 Exam Readiness</div>
        <div class="metric-value">{ready_count}/4</div>
        <div class="metric-subtitle">
            Skills at target level<br>
            {int(readiness_pct)}% ready for IELTS
        </div>
    </div>
    ''', unsafe_allow_html=True)

with col3:
    # Next steps recommendation
    weakest_skill = min(test_types, key=lambda x: get_latest_score(x)) if any(get_latest_score(test) > 0 for test in test_types) else "listening"
    weakest_score = get_latest_score(weakest_skill)
    
    if weakest_score >= 7.0:
        recommendation = "🔥 All skills strong!"
    else:
        recommendation = f"💪 Focus on {weakest_skill}"
    
    st.markdown(f'''
    <div class="metric-card">
        <div class="metric-title">📚 Next Focus</div>
        <div class="metric-value" style="font-size: 20px;">{recommendation}</div>
        <div class="metric-subtitle">
            {"Maintain current level" if weakest_score >= 7.0 else f"Current: {weakest_score if weakest_score > 0 else 'Not tested'}"}<br>
            {"Keep practicing all skills" if weakest_score >= 7.0 else "Target: 7.0+"}
        </div>
    </div>
    ''', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6B7280; padding: 20px; font-size: 14px;">
    💪 Built for IELTS Success • Track your progress, achieve your goals • 💾 Data automatically saved
</div>
""", unsafe_allow_html=True)