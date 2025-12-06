import streamlit as st
from firebase_admin import auth, firestore
from datetime import datetime

def init_auth_state():
    """Initialize authentication session state"""
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None

def sync_google_user_to_firebase(google_user_info):
    """
    Sync Google OAuth user to Firebase Firestore.
    Creates or updates user document based on Google account info.
    """
    try:
        db = firestore.client()
        email = google_user_info.get('email')
        name = google_user_info.get('name', email)
        
        # Use email as the document ID for easy lookup
        # Replace @ and . with _ to make it a valid Firestore document ID
        user_id = email.replace('@', '_').replace('.', '_')
        
        user_ref = db.collection('users').document(user_id)
        user_doc = user_ref.get()
        
        if user_doc.exists:
            # Update last login time
            user_ref.update({
                'last_login': datetime.now(),
                'name': name  # Update name in case it changed
            })
        else:
            # Create new user document
            user_ref.set({
                'email': email,
                'name': name,
                'display_name': name,
                'created_at': datetime.now(),
                'last_login': datetime.now(),
                'favorites': [],
                'custom_affixes': {
                    'prefixes': [],
                    'roots': [],
                    'suffixes': []
                }
            })
        
        return user_id
    except Exception as e:
        st.error(f"Failed to sync user to Firebase: {e}")
        return None

from core.user_features import remove_favorite, get_favorites

def show_auth_ui(lang="fa"):
    """Display Google OAuth authentication UI or User Dashboard"""
    init_auth_state()
    
    # Check if user is logged in with Google OAuth
    # st.user exists but may not have is_logged_in in older versions
    is_logged_in = hasattr(st, 'user') and hasattr(st.user, 'email') and st.user.email
    
    if is_logged_in:
        # Sync to Firebase on first login or if not synced
        if not st.session_state.user_id or st.session_state.user_email != st.user.email:
            user_id = sync_google_user_to_firebase(st.user)
            if user_id:
                st.session_state.user_id = user_id
                st.session_state.user_email = st.user.email
                st.session_state.user = st.user
        
        # --- USER DASHBOARD ---
        if st.session_state.user_id:
            with st.sidebar:
                st.markdown("---")
                st.success(f"سلام، {st.user.name or st.user.email}!" if lang == "fa" else f"Welcome {st.user.name or st.user.email}!")
                
                with st.expander("👤 " + ("پروفایل من" if lang == "fa" else "My Profile")):
                    st.markdown(f"**{st.user.name}**")
                    st.caption(st.user.email)
                
                # Favorites Section
                favorites_label = "❤️ " + ("واژه‌های محبوب من" if lang == "fa" else "My Favorites")
                with st.expander(favorites_label, expanded=True):
                    # Fetch fresh data
                    favorites = get_favorites(st.session_state.user_id)
                    
                    if favorites:
                        # Use a fixed-height container to allow scrolling for long lists
                        with st.container(height=200, border=False):
                            for item in favorites:
                                # Handle both string (legacy) and dict (new) formats
                                if isinstance(item, dict):
                                    word_text = item.get('word', 'Unknown')
                                else:
                                    word_text = str(item)
                                
                                # Use columns for layout: Word (Left) | Delete Button (Right)
                                c1, c2 = st.columns([4, 1])
                                with c1:
                                    # Display word WITHOUT bullet
                                    st.markdown(f"**{word_text}**")
                                with c2:
                                    # Delete button with unique key
                                    if st.button("🗑️", key=f"del_{st.session_state.user_id}_{word_text}", help="حذف" if lang == "fa" else "Delete"):
                                        if remove_favorite(st.session_state.user_id, word_text):
                                            st.toast("حذف شد" if lang == "fa" else "Deleted")
                                            st.rerun()
                    else:
                        st.info("هنوز واژه‌ای ذخیره نکرده‌اید" if lang == "fa" else "No saved words yet")
                
                st.markdown("---")
                
                # Logout Button
                if st.button(("خروج از حساب" if lang == "fa" else "Sign Out"), use_container_width=True):
                    st.logout()
        return True
    
    else:
        # --- LOGIN UI ---
        with st.sidebar:
            st.subheader("🔐 " + ("ورود به حساب" if lang == "fa" else "Login"))
            st.markdown("---")
            
            description = (
                "برای ذخیره واژه‌ها و دسترسی به امکانات بیشتر وارد شوید" 
                if lang == "fa" 
                else "Sign in to save your favorite words and access more features"
            )
            
            st.markdown(f"""
                <div style='text-align: center; margin-bottom: 1rem; color: #666;'>
                    <small>{description}</small>
                </div>
            """, unsafe_allow_html=True)
            
            # Google Sign-In button
            if st.button(
                "🔐 " + ("ورود با گوگل" if lang == "fa" else "Sign in with Google"),
                use_container_width=True,
                type="primary"
            ):
                st.login()
        
        return False

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
