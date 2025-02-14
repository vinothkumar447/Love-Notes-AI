import streamlit as st
from streamlit_option_menu import option_menu
import random
import datetime
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from urllib.parse import quote  # For URL encoding

# Load Hugging Face model & tokenizer (fallback to GPT-2 if DeepSeek-V3 fails)
model_name = "deepseek-ai/DeepSeek-V3"  # Try loading DeepSeek-V3 first
fallback_model = "gpt2"  # Fallback model if DeepSeek-V3 fails

try:
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_name, 
        trust_remote_code=True,
        device_map="auto"  # This helps if you're using a GPU
    )
    generator = pipeline("text-generation", model=model, tokenizer=tokenizer, device_map="auto")
    print(f"✅ Model '{model_name}' loaded successfully!")
except Exception as e:
    print(f"⚠️ Model '{model_name}' loading error: {e}")
    print(f"⚠️ Falling back to '{fallback_model}'...")
    try:
        tokenizer = AutoTokenizer.from_pretrained(fallback_model)
        model = AutoModelForCausalLM.from_pretrained(fallback_model)
        generator = pipeline("text-generation", model=model, tokenizer=tokenizer)
        print(f"✅ Fallback model '{fallback_model}' loaded successfully!")
    except Exception as e:
        generator = None
        print(f"❌ Fallback model loading error: {e}")

# Define default date of birth
default_dob = datetime.date(2000, 1, 1)

# Custom CSS for styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: #FFC0CB !important;
    }
    .love-text {
        font-size: 20px;
        font-weight: bold;
        color: #800020;
        text-align: center;
        padding: 10px;
    }
    .social-icons {
        text-align: center;
        margin-top: 20px;
    }
    .social-icons img {
        width: 40px;
        margin: 0 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to calculate love percentage (between 80% and 99%)
def calculate_love(name1, name2):
    random.seed(name1 + name2)  # Seed random generator for consistent results
    love_percent = random.randint(80, 99)
    return love_percent

# Function to generate unique AI-powered love notes
def generate_love_note(name1, name2, years_in_love):
    if generator is None:
        return "Error: Hugging Face model is not loaded."

    # Improved prompt with clear instructions and examples
    prompt = f"""
    Write a heartfelt love note from {name1} to {name2}.
    They have been together for {years_in_love} years. Make it romantic, poetic, and emotional.
    Here is an example of the tone and style:
    ---
    My dearest {name2},
    Every moment with you feels like a dream. Over the past {years_in_love} years, my love for you has only grown stronger. You are my everything, and I cherish every second we spend together.
    Forever yours,
    {name1}
    ---
    Now, write a love note in a similar style:
    """
    try:
        response = generator(
            prompt,
            max_length=300,  # Adjusted for approximately 150 words
            do_sample=True,
            temperature=0.7,  # Lower for more focused, higher for more creative
            top_p=0.9,  # Controls diversity
            num_return_sequences=1  # Generate only one response
        )
        # Extract and clean the generated text
        love_note = response[0]["generated_text"].split("---")[-1].strip()
        return love_note
    except Exception as e:
        return f"Error generating love note: {e}"

# Sidebar Navigation Menu
with st.sidebar:
    selected_model = option_menu(
        menu_title="Main Menu",
        options=["Home", "Love Calculator", "Love Notes"],
        icons=["house", "heart", "envelope"],
        menu_icon="cast",
        default_index=0,
    )

# Home Page
if selected_model == "Home":
    st.title("💘 Welcome to Love Calculator & Notes AI")
    st.write("Find out your love compatibility & create personalized love notes! 💖✨")
    romantic_sentence = "Love is an endless adventure where two hearts beat as one, creating a masterpiece of happiness and passion. 💑💞"
    st.markdown(f"<p class='love-text'>{romantic_sentence}</p>", unsafe_allow_html=True)

# Love Calculator Page
elif selected_model == "Love Calculator":
    st.title("💑 Love Calculator")

    col1, col2 = st.columns(2)
    
    with col1:
        name1 = st.text_input("👤 Enter your name:")
        gender1 = st.selectbox("🚻 Select your gender:", ["Male", "Female", "Other"])
        dob1 = st.date_input("📅 Your Date of Birth:", value=default_dob)

    with col2:
        name2 = st.text_input("👤 Enter your partner's name:")
        gender2 = st.selectbox("🚻 Select your partner's gender:", ["Male", "Female", "Other"])
        dob2 = st.date_input("📅 Partner's Date of Birth:", value=default_dob)

    years_in_love = st.number_input("❤️ How many years have you been in love?", min_value=0, step=1)

    if st.button("Calculate Love"):
        if name1 and name2:
            love_percent = calculate_love(name1, name2)
            st.success(f"💖 The love between {name1} and {name2} is {love_percent}%!")
            st.balloons()
        else:
            st.error("Please enter both names to calculate love.")

# Love Notes Page
elif selected_model == "Love Notes":
    st.title("💌 Love Notes")

    name1 = st.text_input("👤 Enter your name:")
    name2 = st.text_input("👤 Enter your partner's name:")
    years_in_love = st.number_input("❤️ How many years have you been together?", min_value=0, step=1)

    if name1 and name2 and st.button("Generate Love Note"):
        if generator is None:
            st.error("Hugging Face model is not loaded. Please check the model configuration.")
        else:
            love_note = generate_love_note(name1, name2, years_in_love)
            st.write(f"💖 {love_note}")
            st.balloons()

            # Social Media Share Icons
            encoded_note = quote(love_note)  # URL encode the love note
            st.markdown(
                f"""
                <div class="social-icons">
                    <p style="text-align:center; font-size:18px; font-weight:bold; color:#800020;">
                    Share Your Love 💕
                    </p>
                    <a href="https://api.whatsapp.com/send?text={encoded_note}" target="_blank">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" alt="WhatsApp">
                    </a>
                    <a href="https://www.instagram.com/" target="_blank">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png" alt="Instagram">
                    </a>
                    <a href="https://www.facebook.com/sharer/sharer.php?u={encoded_note}" target="_blank">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/1/1b/Facebook_icon.svg" alt="Facebook">
                    </a>
                    <a href="https://www.snapchat.com/" target="_blank">
                        <img src="https://upload.wikimedia.org/wikipedia/en/thumb/c/c4/Snapchat_logo.svg/1200px-Snapchat_logo.svg.png" alt="Snapchat">
                    </a>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.warning("Please enter names and years together to generate a love note.")

# Footer
st.markdown("---")