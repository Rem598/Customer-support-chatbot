import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Customer Support Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
    }
    .chat-message.user {
        background-color: #0f3460;
        color: white;
    }
    .chat-message.bot {
        background-color: #1a1a2e;
        color: white;
        border: 1px solid #16213e;
    }
    .chat-message .message {
        flex-grow: 1;
        padding-left: 1rem;
    }
    .stTextInput input {
        background-color: #16213e;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Get API key from environment variable
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# Fake order database for demo
FAKE_ORDERS = {
    '#12345': {
        'status': 'Out for Delivery',
        'items': 'Wireless Headphones',
        'eta': 'Today by 6 PM',
        'location': 'Mombasa Distribution Center'
    },
    '#67890': {
        'status': 'Shipped',
        'items': 'Running Shoes',
        'eta': 'Tomorrow',
        'location': 'Nairobi Hub'
    },
    '#11111': {
        'status': 'Processing',
        'items': 'Laptop Stand',
        'eta': '3-5 business days',
        'location': 'Warehouse'
    },
    '#99999': {
        'status': 'Delivered',
        'items': 'Phone Case',
        'eta': 'Delivered on Nov 15',
        'location': 'Your doorstep'
    }
}

def check_order_number(user_input):
    """Check if input contains an order number and return tracking info"""
    input_upper = user_input.upper()
    for order_id in FAKE_ORDERS.keys():
        if order_id in input_upper:
            order_info = FAKE_ORDERS[order_id]
            return f"""📦 **Order Found!** Order {order_id}

**Status:** {order_info['status']} ✅
**Items:** {order_info['items']}
**Expected Delivery:** {order_info['eta']}
**Current Location:** {order_info['location']}

Need anything else? I can help with returns, cancellations, or any other questions!"""
    return None

def get_ai_response(user_input, conversation_history):
    """Get AI-powered response using Groq"""
    
    if not GROQ_API_KEY:
        return "⚠️ **API Key Missing!**\n\nPlease add your Groq API key to the `.env` file:\n```\nGROQ_API_KEY=your_key_here\n```\n\n🔑 Get your free key at: https://console.groq.com"
    
    try:
        client = Groq(api_key=GROQ_API_KEY)
        
        # System prompt with company knowledge
        system_prompt = """You are a friendly and helpful customer support assistant for an e-commerce company.

COMPANY INFORMATION:
- Return Policy: 30 days return window, items must be unused and in original packaging
- Shipping: Standard (5-7 days), Express (2-3 days). Free shipping on orders above $50
- Payment Methods: Credit Cards, Debit Cards, UPI, Net Banking, Wallets
- Contact: Email: support@shop.com | Phone: 1-800-SUPPORT (24/7)
- Refund Processing Time: 5-7 business days

GUIDELINES:
1. Be friendly, empathetic, and professional
2. Use emojis to make responses engaging (but don't overdo it)
3. Keep responses concise but helpful
4. If you don't know something, admit it and offer to connect them with human support
5. Always try to resolve the issue or provide next steps
6. For order tracking, ask for the order number if not provided

RESPONSE STYLE:
- Start with acknowledging their concern
- Provide clear, actionable information
- End with asking if they need more help

Remember: You're here to make customers happy and solve their problems!"""

        # Build messages with conversation history
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history (last 10 messages for context)
        for msg in conversation_history[-10:]:
            messages.append({
                "role": "user" if msg['role'] == 'user' else "assistant",
                "content": msg['content']
            })
        
        # Add current user input
        messages.append({"role": "user", "content": user_input})
        
        # Get response from Groq
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile", 
            temperature=0.7,
            max_tokens=500,
            top_p=1,
        )
        
        return chat_completion.choices[0].message.content
        
    except Exception as e:
        return f"⚠️ **Error:** {str(e)}\n\nPlease check:\n1. Your API key is valid\n2. You have internet connection\n3. Groq service is available"

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {'role': 'bot', 'content': '👋 Hi! I\'m your AI-powered customer support assistant. How can I help you today?'}
    ]

if 'input_key' not in st.session_state:
    st.session_state.input_key = 0

# Header
st.title('🤖 Customer Support Chatbot')
st.markdown('24/7 Intelligent AI-Powered Support Assistant for Your E-Commerce Needs</i>', unsafe_allow_html=True)

# Show API status
# if GROQ_API_KEY:
   # st.success('✅ AI Mode Active - Ready to help!')
#else:
   # st.error('⚠️ API Key not found. Please add GROQ_API_KEY to your .env file')
   # st.info('📝 Instructions:\n1. Create a `.env` file\n2. Add: `GROQ_API_KEY=your_key_here`\n3. Get free key: https://console.groq.com')

# st.markdown('---')

# Sidebar
with st.sidebar:
    st.header(' Bot Information')
    st.info('''
    **Features:**
    - 🧠 AI-Powered Responses
    - 📦 Order Tracking
    - 🔄 Returns & Refunds
    - 💳 Payment Support
    - 🚚 Shipping Information
    - 👤 Account Help
    - 🛍️ Product Queries
    
    ''')
    
    # st.markdown('---')
   # st.header('📈 Statistics')
    #st.metric('Total Messages', len(st.session_state.messages))
    #st.metric('Bot Responses', len([m for m in st.session_state.messages if m['role'] == 'bot']))
    #st.metric('AI Status', 'Active ✅' if GROQ_API_KEY else 'Inactive ❌')
    
    

    
    # st.markdown('---')
    # if st.button('🔄 Clear Chat History'):
     #   st.session_state.messages = [
       #     {'role': 'bot', 'content': '👋 Hi! I\'m your AI-powered customer support assistant. How can I help you today?'}
       # ]
       # st.session_state.input_key += 1
       # st.rerun()

# Display chat messages
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        if message['role'] == 'user':
            st.markdown(f"""
            <div class="chat-message user">
                <div>👤</div>
                <div class="message">{message['content']}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message bot">
                <div>🤖</div>
                <div class="message">{message['content']}</div>
            </div>
            """, unsafe_allow_html=True)

# Quick action buttons
st.markdown('### Quick Actions')
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button('📦 Track Order'):
        user_msg = 'Track my order #12345'
        st.session_state.messages.append({'role': 'user', 'content': user_msg})
        
        # Check for order number first
        order_response = check_order_number(user_msg)
        if order_response:
            bot_response = order_response
        else:
            bot_response = get_ai_response(user_msg, st.session_state.messages)
        
        st.session_state.messages.append({'role': 'bot', 'content': bot_response})
        st.rerun()

with col2:
    if st.button('🔄 Returns'):
        user_msg = 'How do I return an item?'
        st.session_state.messages.append({'role': 'user', 'content': user_msg})
        bot_response = get_ai_response(user_msg, st.session_state.messages)
        st.session_state.messages.append({'role': 'bot', 'content': bot_response})
        st.rerun()

with col3:
    if st.button('💳 Payment'):
        user_msg = 'What payment methods do you accept?'
        st.session_state.messages.append({'role': 'user', 'content': user_msg})
        bot_response = get_ai_response(user_msg, st.session_state.messages)
        st.session_state.messages.append({'role': 'bot', 'content': bot_response})
        st.rerun()

with col4:
    if st.button('📞 Contact'):
        user_msg = 'How can I contact support?'
        st.session_state.messages.append({'role': 'user', 'content': user_msg})
        bot_response = get_ai_response(user_msg, st.session_state.messages)
        st.session_state.messages.append({'role': 'bot', 'content': bot_response})
        st.rerun()

# Chat input
st.markdown('---')

with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_input(
        'Type your message here...', 
        key=f'user_input_{st.session_state.input_key}',
        placeholder='Ask me anything about orders, returns, payments, and more!'
    )
    submit_button = st.form_submit_button('Send 📤')
    
    if submit_button and user_input:
        # Add user message
        st.session_state.messages.append({'role': 'user', 'content': user_input})
        
        # Check for order number first (priority)
        order_response = check_order_number(user_input)
        if order_response:
            bot_response = order_response
        else:
            # Get AI response with full conversation history
            bot_response = get_ai_response(user_input, st.session_state.messages)
        
        st.session_state.messages.append({'role': 'bot', 'content': bot_response})
        st.session_state.input_key += 1
        st.rerun()

# Footer
st.markdown('---')
st.markdown('''
<div style="text-align: center; color: white;">
    <p>🚀 Built with Streamlit + Groq AI | AI-Powered Customer Support</p>
    <p>© 2025 E-Commerce Inc. All rights reserved.</p>
</div>
''', unsafe_allow_html=True)