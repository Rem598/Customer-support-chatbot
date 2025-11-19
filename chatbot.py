import streamlit as st
import random
from datetime import datetime

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
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
    }
    .chat-message.user {
        background-color: #2b313e;
        color: white;
    }
    .chat-message.bot {
        background-color: #475063;
        color: white;
    }
    .chat-message .message {
        flex-grow: 1;
        padding-left: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Knowledge Base - FAQ responses
KNOWLEDGE_BASE = {
    'greetings': {
        'patterns': ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening', 'greetings'],
        'responses': [
            '👋 Hello! How can I assist you today?',
            '😊 Hi there! What can I help you with?',
            '🌟 Hey! I\'m here to help. What do you need?'
        ]
    },
    'order_tracking': {
        'patterns': ['track order', 'where is my order', 'order status', 'track my package', 
                     'delivery status', 'when will my order arrive'],
        'responses': [
            '📦 To track your order, please provide your order number (starting with #). You can find it in your confirmation email.',
            '🚚 I can help you track your order! Please share your order ID and I\'ll check the status for you.',
            '📍 To check your delivery status, I\'ll need your order number. It should look like #12345.'
        ]
    },
    'returns': {
        'patterns': ['return', 'refund', 'exchange', 'send back', 'cancel order', 'money back'],
        'responses': [
            '🔄 Our return policy allows returns within 30 days of delivery. Items must be unused and in original packaging. Would you like to initiate a return?',
            '💰 For refunds, please note: Returns are processed within 5-7 business days. You can start a return from your account dashboard.',
            '↩️ To return an item: 1) Go to Orders, 2) Select the item, 3) Click "Return", 4) Choose reason. Need help with this?'
        ]
    },
    'payment': {
        'patterns': ['payment', 'pay', 'credit card', 'debit card', 'payment method', 
                     'billing', 'charge', 'transaction failed'],
        'responses': [
            '💳 We accept Credit Cards, Debit Cards, UPI, Net Banking, and Wallets. Is there a specific payment issue you\'re facing?',
            '💵 Payment issues? Please check: 1) Card details are correct, 2) Sufficient balance, 3) Card is enabled for online transactions. Still stuck?',
            '🔒 All payments are secure and encrypted. If your transaction failed, the amount will be refunded in 5-7 days automatically.'
        ]
    },
    'shipping': {
        'patterns': ['shipping', 'delivery', 'courier', 'shipping cost', 'free shipping', 
                     'how long', 'delivery time'],
        'responses': [
            '🚀 Standard shipping: 5-7 business days | Express shipping: 2-3 business days. Free shipping on orders above $50!',
            '📬 Delivery times: Metro cities 3-5 days, Other cities 5-7 days. You\'ll get tracking details via email once shipped.',
            '🌍 We ship nationwide! Shipping costs start at $5 for standard delivery. Express delivery available for $15.'
        ]
    },
    'account': {
        'patterns': ['account', 'login', 'password', 'forgot password', 'sign up', 'register', 'profile'],
        'responses': [
            '👤 Account issues? Use "Forgot Password" on the login page to reset. Check your email for the reset link.',
            '🔐 To create an account: Click "Sign Up" → Enter email → Set password → Verify email. Need help with this?',
            '✉️ Can\'t login? Try: 1) Reset password, 2) Check if email is verified, 3) Clear browser cache. Still having trouble?'
        ]
    },
    'contact': {
        'patterns': ['contact', 'call', 'email', 'support', 'help', 'phone number', 
                     'customer service', 'reach you'],
        'responses': [
            '📞 Contact us: Email: support@example.com | Phone: 1-800-SUPPORT (24/7) | Live Chat: Available on website',
            '💬 Need human support? Email: help@example.com or call 1-800-555-0100. We respond within 2 hours!',
            '🤝 You can reach our customer service team: Phone: +1-800-HELP | Email: care@example.com | Hours: 24/7'
        ]
    },
    'products': {
        'patterns': ['product', 'item', 'availability', 'in stock', 'out of stock', 'size', 'color'],
        'responses': [
            '🛍️ Looking for product information? Please share the product name or link, and I\'ll check availability and details for you.',
            '📦 To check product availability, please provide the product name or SKU. I can also help with size guides and specifications!',
            '🎨 Need product details like size, color, or specs? Share the product name and I\'ll get you all the information.'
        ]
    },
    'thanks': {
        'patterns': ['thank', 'thanks', 'appreciate', 'helpful', 'great'],
        'responses': [
            '😊 You\'re welcome! Is there anything else I can help you with?',
            '🌟 Happy to help! Feel free to ask if you need anything else.',
            '💙 Glad I could assist! Don\'t hesitate to reach out if you have more questions.'
        ]
    },
    'goodbye': {
        'patterns': ['bye', 'goodbye', 'see you', 'later', 'exit'],
        'responses': [
            '👋 Goodbye! Have a great day! Feel free to return if you need help.',
            '😊 Take care! Come back anytime you need assistance.',
            '🌟 See you later! Hope your issue is resolved. Happy shopping!'
        ]
    }
}

def find_best_match(user_input):
    """Find the best matching response based on user input"""
    input_lower = user_input.lower().strip()
    
    # Check each category
    for category, data in KNOWLEDGE_BASE.items():
        for pattern in data['patterns']:
            if pattern in input_lower:
                return random.choice(data['responses'])
    
    # Fallback responses
    fallbacks = [
        '🤔 I\'m not sure I understand. Could you rephrase that? Or try asking about: orders, returns, payments, or shipping.',
        '❓ Hmm, I didn\'t quite get that. I can help with order tracking, returns, payments, shipping, and account issues. What do you need?',
        '💭 Sorry, I\'m still learning! I can assist with common questions about orders, delivery, refunds, and payments. What would you like to know?'
    ]
    
    return random.choice(fallbacks)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {'role': 'bot', 'content': '👋 Hi! I\'m your customer support assistant. How can I help you today?'}
    ]

# Header
st.title('🤖 Customer Support Chatbot')
st.markdown('**24/7 Intelligent Support Assistant**')
st.markdown('---')

# Sidebar
with st.sidebar:
    st.header('📊 Bot Information')
    st.info('''
    **Features:**
    - Order Tracking
    - Returns & Refunds
    - Payment Support
    - Shipping Information
    - Account Help
    - Product Queries
    ''')
    
    st.markdown('---')
    st.header('📈 Statistics')
    st.metric('Total Messages', len(st.session_state.messages))
    st.metric('Bot Responses', len([m for m in st.session_state.messages if m['role'] == 'bot']))
    
    st.markdown('---')
    if st.button('🔄 Clear Chat History'):
        st.session_state.messages = [
            {'role': 'bot', 'content': '👋 Hi! I\'m your customer support assistant. How can I help you today?'}
        ]
        st.rerun()

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
        st.session_state.messages.append({'role': 'user', 'content': 'Where is my order?'})
        bot_response = find_best_match('Where is my order?')
        st.session_state.messages.append({'role': 'bot', 'content': bot_response})
        st.rerun()

with col2:
    if st.button('🔄 Returns'):
        st.session_state.messages.append({'role': 'user', 'content': 'How do I return an item?'})
        bot_response = find_best_match('How do I return an item?')
        st.session_state.messages.append({'role': 'bot', 'content': bot_response})
        st.rerun()

with col3:
    if st.button('💳 Payment'):
        st.session_state.messages.append({'role': 'user', 'content': 'Payment methods'})
        bot_response = find_best_match('Payment methods')
        st.session_state.messages.append({'role': 'bot', 'content': bot_response})
        st.rerun()

with col4:
    if st.button('📞 Contact'):
        st.session_state.messages.append({'role': 'user', 'content': 'Contact support'})
        bot_response = find_best_match('Contact support')
        st.session_state.messages.append({'role': 'bot', 'content': bot_response})
        st.rerun()

# Chat input
st.markdown('---')
user_input = st.text_input('Type your message here...', key='user_input', placeholder='Ask me anything!')

if st.button('Send 📤') and user_input:
    # Add user message
    st.session_state.messages.append({'role': 'user', 'content': user_input})
    
    # Get bot response
    bot_response = find_best_match(user_input)
    st.session_state.messages.append({'role': 'bot', 'content': bot_response})
    
    st.rerun()

# Footer
st.markdown('---')
st.markdown('''
<div style="text-align: center; color: white;">
    <p>Built with ❤️ using Streamlit | AI-Powered Customer Support</p>
</div>
''', unsafe_allow_html=True)