"""
MarketSage AI for Small and Medium Businesses
A comprehensive AI Marketing tool powered by Streamlit and OpenAI
"""

import streamlit as st
from openai import OpenAI
import json
import requests
from datetime import datetime

# ============================================================
# 🎨 YOUR BRANDING - CUSTOMIZE THIS SECTION
# ============================================================
BRAND_CONFIG = {
    # Your Information
    "consultant_name": "ADD YOUR NAME",
    "business_name": "MarketSage AI",
    "tagline": "Your AI App For Marketing Wisdom",
    # Contact & Links
    "email": "ADD YOUR GMAIL EMAIL ADDRESS",
    "website": "https://yourwebsite.com",  # Update when ready
    # "calendar_link": "https://calendly.com/your-link",  Update when ready#
    "calendar_link": " Sign UP  For a Free Account and add your link",    
    "course_name": "Complete AI for Business Course",
    # Social Media (update when ready)
    "linkedin": "https://linkedin.com/in/yourprofile",
    "twitter": "",
    "youtube": "",
    # Lead Capture Settings - GOOGLE SHEETS METHOD
    "enable_lead_capture": True,
    "google_sheet_url": "https://script.google.com/macros/s/AKfycbxmnFf6HkC9Pgasek69ivlKsHGRHM3AgHATN0rUhrIsp9xpL9CCrzG7iHUwhrDZzPxK/exec",
    # Customization
    "show_powered_by": True,
}
# ============================================================

# Page Configuration
st.set_page_config(
    page_title=f"{BRAND_CONFIG['business_name']} - AI for SMB Marketing",
    page_icon="icon.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
st.markdown(
    """
<style>
    /* Main theme */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #6d28d9 100%);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #e2e8f0 !important;
    }
    
    /* Cards */
    .metric-card {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 0.5rem 0;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #6366f1;
    }
    
    .metric-label {
        color: #94a3b8;
        font-size: 0.9rem;
    }
    
    /* Use case cards */
    .use-case-card {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(99, 102, 241, 0.15);
        border-radius: 12px;
        padding: 1.25rem;
        margin: 0.75rem 0;
        transition: all 0.2s ease;
    }
    
    .use-case-card:hover {
        border-color: rgba(99, 102, 241, 0.4);
    }
    
    /* Badges */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    .badge-easy {
        background: rgba(16, 185, 129, 0.2);
        color: #34d399;
    }
    
    .badge-medium {
        background: rgba(245, 158, 11, 0.2);
        color: #fbbf24;
    }
    
    .badge-info {
        background: rgba(99, 102, 241, 0.2);
        color: #a5b4fc;
    }
    
    /* Chat messages */
    .chat-message {
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
    }
    
    .chat-assistant {
        background: rgba(99, 102, 241, 0.15);
        border-left: 3px solid #6366f1;
    }
    
    .chat-user {
        background: rgba(30, 41, 59, 0.6);
        border-left: 3px solid #94a3b8;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    }
    
    /* Progress bars */
    .stProgress > div > div {
        background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%);
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: rgba(30, 41, 59, 0.6);
        border-radius: 8px;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(18, 12, 32, 0.95);
    }
    
    /* Info boxes */
    .info-box {
        background: rgba(99, 102, 241, 0.1);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .success-box {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Lead capture form */
    .lead-form {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
        border: 2px solid rgba(99, 102, 241, 0.4);
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
        text-align: center;
    }
    
    .lead-form h3 {
        margin-bottom: 0.5rem;
    }
    
    /* Footer */
    .custom-footer {
        background: rgba(15, 23, 42, 0.8);
        border-top: 1px solid rgba(99, 102, 241, 0.2);
        padding: 1.5rem;
        margin-top: 3rem;
        border-radius: 12px;
        text-align: center;
    }
    
    .footer-links a {
        color: #a5b4fc;
        text-decoration: none;
        margin: 0 0.5rem;
    }
    
    .footer-links a:hover {
        color: #c7d2fe;
    }
    
    /* CTA Button */
    .cta-button {
        background: linear-gradient(135deg, #10b981 0%, #5b21b6 100%);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 600;
        display: inline-block;
        margin: 0.5rem;
    }
    
    .cta-button:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        color: white;
    }
</style>
""",
    unsafe_allow_html=True,
)
# ============================================================

# Initialize session state
if "assessment_answers" not in st.session_state:
    st.session_state.assessment_answers = {}
if "assessment_complete" not in st.session_state:
    st.session_state.assessment_complete = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "generated_content" not in st.session_state:
    st.session_state.generated_content = ""
if "generated_prompt" not in st.session_state:
    st.session_state.generated_prompt = ""
if "checklist_state" not in st.session_state:
    st.session_state.checklist_state = {}
if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠 Home"
if "pending_message" not in st.session_state:
    st.session_state.pending_message = None
if "selected_use_case" not in st.session_state:
    st.session_state.selected_use_case = None


# Navigation helper function
def navigate_to(page_name):
    st.session_state.current_page = page_name


# Initialize OpenAI client
@st.cache_resource
def get_openai_client():
    api_key = st.secrets.get("OPENAI_API_KEY", None)
    if api_key:
        return OpenAI(api_key=api_key)
    return None


# Data: Assessment Questions
ASSESSMENT_QUESTIONS = [
    {
        "id": "business_type",
        "category": "Brand Profile",
        "question": "What type of business do you run?",
        "options": {
            "retail": "Retail and E-commerce",
            "services": "Professional Services",
            "restaurant": "Tourism and Hospitality",
            "healthcare": "Healthcare and Wellness Clinics",
            "tech": "Technology Start-Ups",
            "other": "Others",
        },
    },
    {
        "id": "tech_comfort",
        "category": "AI Awareness",
        "question": "What is your team’s current familiarity with AI tools?",
        "options": {
            1: "No exposure",
            2: "Basic usage (ChatGPT, Canva AI used)",
            3: "Gen AI used by all Marketing Teams",
            4: "Advanced experimentation (automation, agentic workflows)",
        },
    },
    {
        "id": "data_quality",
        "category": "Data Infrastructure",
        "question": "What marketing data do you currently collect and centralize?",
        "options": {
            1: "Scattered customer, email, campaigns data in spreadsheets",
            2: "CRM Data",
            3: "Website Analytics and Digital Data in isolated systems",
            4: "Integrated Marketing Datawarehouse",
        },
    },
    {
        "id": "budget",
        "category": "Spending Capability",
        "question": "What's your monthly budget for AI tools?",
        "options": {
            1: "Under $1000/month",
            2: "$1000-5000/month",
            3: "$5000-10000/month",
            4: "$10000+/month",
        },
    },
    {
        "id": "pain_points",
        "category": "Marketing Needs",
        "question": "What's your biggest marketing challenge?",
        "options": {
            "customer_service": "Customer Support",
            "content": "Content Creation",
            "admin": "Digital Marketing",
            "sales": "Sales & Lead Generation",
        },
    },
    {
        "id": "team_size",
        "category": "Organization",
        "question": "How many employees do you have?",
        "options": {
            1: "Solo or 1-2 people",
            2: "3-10 employees",
            3: "11-50 employees",
            4: "50+ employees",
        },
    },
    {
        "id": "ai_adoption",
        "category": "AI Ambition",
        "question": "What level of AI adoption are you aiming for in the next 6–12 months?",
        "options": {
            1: "Assistive AI (content, copy, research)",
            2: "Marketing Analytics",
            3: "Workflow automation",
            4: "AI-driven personalization at scale",
        },
    },
    {
        "id": "ai_privacy",
        "category": "AI Governance",
        "question": "Are there concerns about data privacy, compliance, or brand control when using AI?",
        "options": {
            1: "None",
            2: "Low",
            3: "Moderate",
            4: "High",
        },
    },
]

# Content Templates
CONTENT_TEMPLATES = [
    {"id": "social", "name": "Social Media Post", "icon": "📱"},
    {"id": "email", "name": "Marketing Email", "icon": "📧"},
    {"id": "product", "name": "Product Description", "icon": "🛍️"},
    {"id": "blog", "name": "Blog Post Outline", "icon": "📝"},
    {"id": "ad", "name": "Ad Copy", "icon": "📢"},
]

def calculate_roi(
    hours_on_task, hourly_rate, ai_efficiency, tool_cost, implementation_hours
):
    """Calculate ROI metrics for AI implementation"""
    hours_saved = hours_on_task * (ai_efficiency / 100)
    labor_savings = hours_saved * hourly_rate * 4  # Monthly
    monthly_roi = labor_savings - tool_cost
    implementation_cost = implementation_hours * hourly_rate
    payback_period = implementation_cost / monthly_roi if monthly_roi > 0 else 999
    yearly_roi = (monthly_roi * 12) - implementation_cost
    roi_percentage = (
        ((yearly_roi / (implementation_cost + tool_cost * 12)) * 100)
        if (implementation_cost + tool_cost * 12) > 0
        else 0
    )

    return {
        "hours_saved": round(hours_saved * 4),
        "monthly_roi": round(monthly_roi),
        "yearly_roi": round(yearly_roi),
        "payback_period": round(payback_period, 1),
        "roi_percentage": round(roi_percentage),
    }


def get_assessment_results():
    """Calculate assessment results based on answers"""
    answers = st.session_state.assessment_answers

    numeric_scores = []
    for key in ["tech_comfort", "data_quality", "budget", "team_size", "ai_adoption","ai_privacy"]:
        if key in answers and isinstance(answers[key], int):
            numeric_scores.append(answers[key])

    avg_score = sum(numeric_scores) / len(numeric_scores) if numeric_scores else 1
    pain_point = answers.get("pain_points", "customer_service")

    if avg_score < 2:
        level = {
            "name": "AI Beginner",
            "color": "🟠",
            "desc": "Start with simple, low-cost AI use cases",
        }
        recommendations = ["Chatbot", "Content Generation", "Grpahics Generation"]
    elif avg_score < 3:
        level = {
            "name": "AI Experimenter",
            "color": "🟡",
            "desc": "Build and integrate AI use cases in your Marketing Ecosystem",
        }
        recommendations = ["Content Generation", "Email Campaigns", "Chatbot", "Predictive Analytics"]
    else:
        level = {
            "name": "AI Accelerator",
            "color": "🟢",
            "desc": "Go for comprehensive AI transformation building AI use cases across Marketing needs",
        }
        recommendations = ["Sales and Lead Generation", "Predictive Analytics", "Campaign Management", "Content Generation", "Chatbot"]

    pain_point_map = {
        "customer_service": "chatbot",
        "content": "content",
        "admin": "analytics",
        "sales": "sales",
    }

    priority = pain_point_map.get(pain_point, "chatbot")
    if priority in recommendations:
        recommendations.remove(priority)
    recommendations.insert(0, priority)

    return {
        "avg_score": avg_score,
        "level": level,
        "recommendations": recommendations[:4],
        "pain_point": pain_point,
    }


def call_openai(messages, system_prompt=None):
    """Call OpenAI API with messages"""
    client = get_openai_client()
    if not client:
        return "⚠️ OpenAI API key not configured. Please add OPENAI_API_KEY to your Streamlit secrets."

    try:
        full_messages = []
        if system_prompt:
            full_messages.append({"role": "system", "content": system_prompt})
        full_messages.extend(messages)

        response = client.chat.completions.create(
            model="gpt-4o", messages=full_messages, max_tokens=1500, temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error calling OpenAI: {str(e)}"

        # Sidebar Navigation
st.sidebar.markdown(f"## 💯 {BRAND_CONFIG['business_name']}")
st.sidebar.markdown("*For Small and Medium Business*")
st.sidebar.markdown("---")

# Page options
page_options = [
    "🏠 Home",
    "🛰️ AI Tour",
    "✅ Assessment",
    "💲  AI Returns",
]

# Get current index
current_index = (
    page_options.index(st.session_state.current_page)
    if st.session_state.current_page in page_options
    else 0
)

# Sidebar radio for navigation (without key)
selected_page = st.sidebar.radio(
    "Navigate", page_options, index=current_index, label_visibility="collapsed"
)

# If user clicked a different radio option, update and rerun
if selected_page != st.session_state.current_page:
    st.session_state.current_page = selected_page
    st.rerun()

# Current page for routing
current_page = st.session_state.current_page

st.sidebar.markdown("---")
st.sidebar.markdown("### Quick Stats")
if st.session_state.assessment_complete:
    results = get_assessment_results()
    st.sidebar.markdown(
        f"**Readiness:** {results['level']['color']} {results['level']['name']}"
    )
    st.sidebar.markdown(f"**Top Priority:** {results['recommendations'][0].title()}")
else:
    st.sidebar.markdown("*Complete assessment for personalized marketing reccomendations*")

# Sidebar CTA
#render_sidebar_cta()


# HOME PAGE
if current_page == "🏠 Home":
    st.markdown(f"# 💯{BRAND_CONFIG['business_name']}")
    st.markdown(f"### {BRAND_CONFIG['tagline']}")

    st.markdown(
        """
    <div class="info-box">
        <strong>🚀 AI-Driven Decision Making</strong> • Get Personalized recommendations, rapid content generation, 
        and transform your Marketing Initiatives  — all powered by OpenAI.
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("### How It Works")

    col1, col2,col3 = st.columns(3)

    with col1:
        st.markdown(
            """
        **1️⃣ Take the Assessment**
        - Answer 8 quick questions
        - Get your AI readiness score
        - Receive personalized marketing recommendations
        """
        )

    with col2:
        st.markdown(
            """
        **2️⃣Generate Content**
        - Create social media posts
        - Build marketing emails, ads
        - Get Product Descriptions, Blogs
        """
        )
    with col3:
        st.markdown(
            """
        **3️⃣Calculate AI Returns**
        - Follow step-by-step instructions
        - Provide Expected AI Efficiency
        - Calculate your savings
        """
        )

    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col2:
        if st.button("🚀 Get Started - Take Assessment", use_container_width=True):
            st.session_state.assessment_complete = False
            navigate_to("✅ Assessment")
            st.rerun()

# AI TOOLS PAGE
elif current_page == "🛰️ AI Tour":
    st.markdown("# 🛰️ AI Tour")

    tool_tab = st.tabs(
        ["✨ Content Generator"]
    )
 # CONTENT GENERATOR TAB
    with tool_tab[0]:
        st.markdown("### AI Content Generator")
        st.markdown("*Generate marketing content instantly*")

        template = st.selectbox(
            "Select Content Type",
            options=[t["id"] for t in CONTENT_TEMPLATES],
            format_func=lambda x: next(
                t["icon"] + " " + t["name"] for t in CONTENT_TEMPLATES if t["id"] == x
            ),
        )

        col1, col2 = st.columns(2)
        with col1:
            business_name = st.text_input(
                "Business Name", placeholder="e.g., Sunrise Bakery"
            )
            product = st.text_input(
                "Product/Service/Topic", placeholder="e.g., artisan sourdough bread"
            )
        with col2:
            audience = st.text_input(
                "Target Audience", placeholder="e.g., health-conscious foodies"
            )
            tone = st.selectbox(
                "Tone",
                [
                    "Professional",
                    "Friendly & Casual",
                    "Luxurious & Premium",
                    "Playful & Fun",
                    "Authoritative & Expert",
                    "Empathetic & Caring",
                ],
            )

        additional_info = st.text_area(
            "Additional Details (optional)",
            placeholder="Any specific promotions, key messages, or requirements...",
        )

        if st.button("✨ Generate Content", use_container_width=True):
            if not get_openai_client():
                st.error("OpenAI API key not configured")
            else:
                template_prompts = {
                    "social": f"Create 3 engaging social media posts for {business_name or 'a business'} about {product or 'their product'}. Target: {audience or 'general audience'}. Tone: {tone}. {additional_info}\n\nInclude hashtags and best platform for each.",
                    "email": f"Write a marketing email for {business_name or 'a business'} promoting {product or 'their product'}. Target: {audience or 'subscribers'}. Tone: {tone}. {additional_info}\n\nInclude: 3 subject lines, preview text, body (150-200 words), CTA, P.S. line.",
                    "product": f"Write a product description for {product or 'a product'} by {business_name or 'a business'}. Target: {audience or 'customers'}. Tone: {tone}. {additional_info}\n\nInclude: headline, short description, features, benefits, CTA.",
                    "blog": f"Create a blog post outline for {business_name or 'a business'} about {product or 'their expertise'}. Target: {audience or 'readers'}. Tone: {tone}. {additional_info}\n\nInclude: SEO title, meta description, intro hook, 5-7 sections, conclusion, keywords.",
                    "ad": f"Write ad copy for {business_name or 'a business'} promoting {product or 'their product'}. Target: {audience or 'customers'}. Tone: {tone}. {additional_info}\n\nCreate versions for: Facebook/Instagram, Google Search, LinkedIn.",
                    "chatbot": f"Create a chatbot script for {business_name or 'a business'} handling {product or 'customer inquiries'}. Target: {audience or 'website visitors'}. Tone: {tone}. {additional_info}\n\nInclude: welcome message, 5 FAQ Q&As, booking flow, handoff message.",
                }

                with st.spinner("Generating content..."):
                    response = call_openai(
                        [{"role": "user", "content": template_prompts[template]}]
                    )
                    st.session_state.generated_content = response

        if st.session_state.generated_content:
            st.markdown("### Generated Content")
            st.markdown(st.session_state.generated_content)

            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    "📥 Download Content",
                    st.session_state.generated_content,
                    file_name=f"{template}_content.txt",
                    mime="text/plain",
                )
            with col2:
                if st.button("🔄 Generate Again"):
                    st.session_state.generated_content = ""
                    st.rerun()

# ASSESSMENT PAGE
elif current_page == "✅ Assessment":
    st.markdown("# ✅ AI Readiness Assessment")

    if not st.session_state.assessment_complete:
        st.markdown("### Answer 8 quick questions to get personalized recommendations")

        answered_count = len(st.session_state.assessment_answers)
        total_questions = len(ASSESSMENT_QUESTIONS)
        progress = answered_count / total_questions

        # Progress bar and status
        st.progress(progress)

        if answered_count == total_questions:
            st.success(
                f"✅ All {total_questions} questions answered! Click the button below to see your results."
            )
        else:
            st.info(
                f"📝 {answered_count} of {total_questions} questions answered. Please answer all questions to see your results."
            )

        st.markdown("---")

        # Questions - using callbacks for immediate visual update
        def update_answer(question_id, key):
            """Callback to update answer when radio changes"""
            value = st.session_state.get(key)
            if value is not None:
                st.session_state.assessment_answers[question_id] = value

        for q in ASSESSMENT_QUESTIONS:
            # Show checkmark if answered
            is_answered = q["id"] in st.session_state.assessment_answers
            status = "✅" if is_answered else "⬜"

            st.markdown(f"### {status} {q['category']}")

            # Get current value if exists
            current_value = st.session_state.assessment_answers.get(q["id"])
            current_index = (
                list(q["options"].keys()).index(current_value)
                if current_value in q["options"]
                else None
            )

            st.radio(
                q["question"],
                options=list(q["options"].keys()),
                format_func=lambda x, opts=q["options"]: opts[x],
                key=f"q_{q['id']}",
                index=current_index,
                on_change=update_answer,
                args=(q["id"], f"q_{q['id']}"),
            )
            st.markdown("---")

        # Always show button area, but disable if not all answered
        st.markdown("### 📊 Get Your Results")
        if answered_count == total_questions:
            if st.button("✨ See My Results", use_container_width=True, type="primary"):
                st.session_state.assessment_complete = True
                st.rerun()
        else:
            remaining = total_questions - answered_count
            st.warning(
                f"⚠️ Please answer {remaining} more question{'s' if remaining > 1 else ''} to see your results."
            )

            # Show which questions are unanswered
            unanswered = [
                q["category"]
                for q in ASSESSMENT_QUESTIONS
                if q["id"] not in st.session_state.assessment_answers
            ]
            st.markdown("**Still need to answer:**")
            for category in unanswered:
                st.markdown(f"- {category}")

    else:
        # Show results
        results = get_assessment_results()

        st.markdown(
            f"## {results['level']['color']} Your Readiness Level: **{results['level']['name']}**"
        )
        st.markdown(f"*{results['level']['desc']}*")

        st.progress(results["avg_score"] / 4)
        st.markdown(f"**Score: {results['avg_score']:.1f} / 4.0**")

        st.markdown("---")
        st.markdown("### 🎯 Your Top Recommended AI Use Cases for Marketing Needs")

        # Loop through recommendations
        for i, rec_id in enumerate(results["recommendations"], 1):

            st.markdown(f"#### {i}. {rec_id}")

            prompt = f"""
            You are an AI marketing consultant.
            Provide a practical, SMB-friendly description for the following AI use case:

            {rec_id}

            Include:
            - What it is
            - Why it matters for a small/medium marketing team
            - Example implementation
            Keep it concise (150-200 words).
            """

            with st.spinner("Generating recommendation..."):
                response = call_openai(
                    [{"role": "user", "content": prompt}]
                )

            st.markdown(response)
            st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Retake Assessment"):
                st.session_state.assessment_answers = {}
                st.session_state.assessment_complete = False
                st.rerun()
        with col2:
            if st.button("💬 Take AI Tour"):
                navigate_to("🛰️ AI Tour")
                st.rerun()

# ROI CALCULATOR PAGE
elif current_page == "💲  AI Returns":
    st.markdown("# 💲  AI Returns Calculator")
    st.markdown("*Calculate the potential return on your AI use cases*")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Describe your Use Case")

        hours_on_task = st.slider("Hours spent on task per week", 1, 40, 20)
        hourly_rate = st.number_input(
            "Hourly labor cost ($)", min_value=10, max_value=200, value=35
        )
        ai_efficiency = st.slider("Expected AI Efficiency Gains (%)", 30, 90, 70)
        tool_cost = st.number_input(
            "Monthly AI Tech cost ($)", min_value=0, max_value=1000, value=50
        )
        implementation_hours = st.number_input(
            "AI Implementation Effort (one-time hours)", min_value=1, max_value=100, value=10
        )

    with col2:
        st.markdown("### Projected Returns")

        roi = calculate_roi(
            hours_on_task, hourly_rate, ai_efficiency, tool_cost, implementation_hours
        )

        st.markdown(
            f"""
        <div class="metric-card" style="text-align: center;">
            <div class="metric-value" style="font-size: 3rem;">{roi['roi_percentage']}%</div>
            <div class="metric-label">First Year ROI</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Hours Saved/Month", f"{roi['hours_saved']} hrs")
            st.metric("Monthly Savings", f"${roi['monthly_roi']:,}")
        with col_b:
            st.metric("Yearly ROI", f"${roi['yearly_roi']:,}")
            st.metric("Payback Period", f"{roi['payback_period']} months")

        # Recommendation
        if roi["roi_percentage"] > 200:
            st.success(
                "✅ **Great Opportunity.** Proceed with implementation."
            )
        elif roi["roi_percentage"] > 100:
            st.info("📊 **Good ROI potential.** Consider starting with a pilot.")
        else:
            st.warning(
                "⚠️ **Marginal returns.** Look for higher-impact use cases first."
            )

    st.markdown("---")
    st.markdown("### ROI Breakdown")

    st.markdown(
        f"""
| Metric | Value |
|--------|-------|
| Weekly hours on task | {hours_on_task} hrs |
| Hours saved with AI ({ai_efficiency}% efficiency) | {hours_on_task * ai_efficiency / 100:.1f} hrs/week |
| Monthly hours saved | {roi['hours_saved']} hrs |
| Labor savings (@ ${hourly_rate}/hr) | ${roi['hours_saved'] * hourly_rate:,}/month |
| Tool cost | ${tool_cost}/month |
| **Net monthly benefit** | **${roi['monthly_roi']:,}** |
| Implementation cost | ${implementation_hours * hourly_rate:,} |
| **First year net ROI** | **${roi['yearly_roi']:,}** |
    """
    )


# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("*Built to help small and medium businesses take the AI Leap*")
st.sidebar.markdown("Powered by OpenAI & Streamlit")