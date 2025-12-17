import streamlit as st
import pandas as pd

from agents.behavior_tracker import track_behavior
from agents.churn_model import train_churn_model
from agents.segmentation import segment_users
from agents.send_time_optimizer import optimize_send_time
from agents.email_generator import generate_email
from agents.email_sender import send_email
from agents.performance_tracker import track_performance

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(page_title="AI Email Marketing Agent", layout="wide")
st.title(" AI Email Marketing Agent")

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
df = pd.read_csv("data/users.csv")

# --------------------------------------------------
# AGENT PIPELINE
# --------------------------------------------------
df = track_behavior(df)
df = train_churn_model(df)
df = segment_users(df)
df = optimize_send_time(df)

# --------------------------------------------------
# 👥 USER DATA TABLE (RESTORED)
# --------------------------------------------------
st.subheader(" User Data")
st.dataframe(
    df[
        [
            "email",
            "plan",
            "signup_days",
            "logins_last_7d",
            "features_used",
            "last_login_days"
        ]
    ],
    use_container_width=True
)

# --------------------------------------------------
# SIDEBAR (OLD UI – RESTORED)
# --------------------------------------------------
st.sidebar.header("User Segments")

df["user_label"] = df["email"] + " (" + df["segment_label"] + ")"
selected_user_label = st.sidebar.selectbox(
    "Select User",
    df["user_label"]
)

selected_user = df[df["user_label"] == selected_user_label].iloc[0]

st.sidebar.subheader(" AI Generated Email")

email_subject, email_body = generate_email(selected_user)

email_subject = st.sidebar.text_input(
    "Email Subject",
    email_subject
)

email_body = st.sidebar.text_area(
    "Email Body",
    email_body,
    height=220
)

# --------------------------------------------------
# 🧠 AGENT DECISION TABLE
# --------------------------------------------------
st.subheader(" Agent Decision Table")
st.dataframe(
    df[["email", "segment_label", "churn_risk", "best_send_hour"]],
    use_container_width=True
)

# --------------------------------------------------
# 🚀 AUTONOMOUS EMAIL CAMPAIGN
# --------------------------------------------------
if st.button(" Run Autonomous Email Campaign"):
    st.success("✅ Autonomous campaign started")

    st.subheader(" Generated Emails (Agent Actions)")

    for _, user in df.iterrows():
        subject, body = generate_email(user)

        with st.expander(
            f"📨 {user.email} | {user.segment_label} | Send @ {user.best_send_hour}:00"
        ):
            st.write(f"**Subject:** {subject}")
            st.write(body)

        # REAL EMAIL SEND (AUTONOMOUS)
        send_email(user.email, subject, body)

    # --------------------------------------------------
    # 📊 PERFORMANCE TRACKING
    # --------------------------------------------------
    open_rate, click_rate, perf_df = track_performance(df)

    st.subheader("📊 Campaign Performance")
    col1, col2 = st.columns(2)
    col1.metric("📬 Open Rate", f"{open_rate*100:.1f}%")
    col2.metric("🖱️ Click Rate", f"{click_rate*100:.1f}%")

    # --------------------------------------------------
    # 📈 ENGAGEMENT CHART
    # --------------------------------------------------
    st.subheader(" Engagement Chart")
    st.bar_chart(
        perf_df.set_index("email")[["opened", "clicked"]],
        use_container_width=True
    )

# --------------------------------------------------
# 📤 MANUAL SEND (SELECTED USER)
# --------------------------------------------------
if st.button("📤 Send Email"):
    try:
        send_email(
            selected_user.email,
            email_subject,
            email_body
        )
        st.success(f"✅ Email sent to {selected_user.email}")
    except Exception as e:
        st.error(f"❌ Email failed: {e}")
