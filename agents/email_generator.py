from config.groq_config import get_groq_client

client = get_groq_client()

def generate_email(user):
    if user.segment_label == "New / Onboarding":
        subject = "Welcome aboard! Let’s get you started 🚀"
        goal = "Help the user get started and achieve first success."

    elif user.segment_label == "High Churn Risk":
        subject = "We miss you — let’s get you back 💙"
        goal = "Re-engage the user and reduce churn."

    else:
        subject = "New features you’ll love ✨"
        goal = "Encourage deeper product usage."

    prompt = f"""
You are a SaaS email marketing expert.

Goal: {goal}
User plan: {user.plan}
Signup days: {user.signup_days}
Features used: {user.features_used}
Churn risk: {user.churn_risk:.2f}

Write a short, friendly, personalized email.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    body = response.choices[0].message.content.strip()
    return subject, body
