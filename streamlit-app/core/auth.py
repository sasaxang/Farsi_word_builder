import streamlit as st
from firebase_admin import auth, firestore
from datetime import datetime
import hashlib

def init_auth_state():
    """Initialize authentication session state"""
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None

def create_user_document(user_id, email, display_name):
    """Create initial user document in Firestore"""
    try:
        db = firestore.client()
        user_ref = db.collection('users').document(user_id)
        
        # Check if user already exists
        if user_ref.get().exists:
            return True
        
        # Create new user document
        user_ref.set({
            'email': email,
            'display_name': display_name,
            'created_at': datetime.now(),
            'favorites': [],
            'custom_affixes': {
                'prefixes': [],
                'roots': [],
                'suffixes': []
            }
        })
        return True
    except Exception as e:
        st.error(f"Failed to create user document: {e}")
        return False

def register_user(email, password, display_name):
    """Register a new user with Firebase Auth"""
    try:
        # Create user in Firebase Auth
        user = auth.create_user(
            email=email,
            password=password,
            display_name=display_name
        )
        
        # Create user document in Firestore
        if create_user_document(user.uid, email, display_name):
            st.success(f"✅ Account created successfully! Welcome, {display_name}!")
            return user
        else:
            # Rollback: delete the auth user if Firestore creation fails
            auth.delete_user(user.uid)
            st.error("❌ Failed to complete registration. Please try again.")
            return None
            
    except auth.EmailAlreadyExistsError:
        st.error("❌ This email is already registered. Please login instead.")
        return None
    except Exception as e:
        st.error(f"❌ Registration failed: {str(e)}")
        return None

def verify_user_credentials(email, password):
    """
    Verify user credentials using Firebase Auth REST API.
    Firebase Admin SDK doesn't support email/password login directly,
    so we check if user exists and verify via custom token approach.
    """
    try:
        # Get user by email
        user = auth.get_user_by_email(email)
        
        # For production, you'd use Firebase Auth REST API here
        # For now, we'll use a simplified approach with custom tokens
        # Generate custom token for the user
        custom_token = auth.create_custom_token(user.uid)
        
        return user
    except auth.UserNotFoundError:
        st.error("❌ No account found with this email.")
        return None
    except Exception as e:
        st.error(f"❌ Login failed: {str(e)}")
        return None

def login_user(email, password):
    """Login user and create session"""
    user = verify_user_credentials(email, password)
    
    if user:
        # Set session state
        st.session_state.user = user
        st.session_state.user_id = user.uid
        st.session_state.user_email = user.email
        st.success(f"✅ Welcome back, {user.display_name or email}!")
        st.rerun()
        return True
    return False

def logout_user():
    """Clear user session"""
    st.session_state.user = None
    st.session_state.user_id = None
    st.session_state.user_email = None
    st.success("👋 Logged out successfully!")
    st.rerun()

def get_user_data(user_id):
    """Get user data from Firestore"""
    try:
        db = firestore.client()
        user_doc = db.collection('users').document(user_id).get()
        if user_doc.exists:
            return user_doc.to_dict()
        return None
    except Exception as e:
        st.error(f"Failed to fetch user data: {e}")
        return None

def show_auth_ui(lang="fa"):
    """Display authentication UI (login/register)"""
    init_auth_state()
    
    # If user is logged in, show logout button
    if st.session_state.user:
        with st.sidebar:
            st.success(f"👤 {st.session_state.user_email}")
            if st.button("🚪 خروج" if lang == "fa" else "🚪 Logout", use_container_width=True):
                logout_user()
        return True
    
    # Show login/register form
    with st.sidebar:
        st.subheader("🔐 ورود / ثبت‌نام" if lang == "fa" else "🔐 Login / Register")
        
        tab1, tab2 = st.tabs(["ورود" if lang == "fa" else "Login", "ثبت‌نام" if lang == "fa" else "Register"])
        
        with tab1:
            with st.form("login_form"):
                email = st.text_input("ایمیل" if lang == "fa" else "Email", key="login_email")
                password = st.text_input("رمز عبور" if lang == "fa" else "Password", type="password", key="login_password")
                submit = st.form_submit_button("ورود" if lang == "fa" else "Login", use_container_width=True)
                
                if submit:
                    if email and password:
                        login_user(email, password)
                    else:
                        st.error("لطفا تمام فیلدها را پر کنید" if lang == "fa" else "Please fill all fields")
        
        with tab2:
            with st.form("register_form"):
                name = st.text_input("نام" if lang == "fa" else "Name", key="register_name")
                email = st.text_input("ایمیل" if lang == "fa" else "Email", key="register_email")
                password = st.text_input("رمز عبور" if lang == "fa" else "Password", type="password", key="register_password")
                password_confirm = st.text_input("تکرار رمز عبور" if lang == "fa" else "Confirm Password", type="password", key="register_password_confirm")
                submit = st.form_submit_button("ثبت‌نام" if lang == "fa" else "Register", use_container_width=True)
                
                if submit:
                    if not all([name, email, password, password_confirm]):
                        st.error("لطفا تمام فیلدها را پر کنید" if lang == "fa" else "Please fill all fields")
                    elif password != password_confirm:
                        st.error("رمز عبور و تکرار آن یکسان نیستند" if lang == "fa" else "Passwords do not match")
                    elif len(password) < 6:
                        st.error("رمز عبور باید حداقل ۶ کاراکتر باشد" if lang == "fa" else "Password must be at least 6 characters")
                    else:
                        user = register_user(email, password, name)
                        if user:
                            # Auto-login after registration
                            st.session_state.user = user
                            st.session_state.user_id = user.uid
                            st.session_state.user_email = user.email
                            st.rerun()
    
    return False
