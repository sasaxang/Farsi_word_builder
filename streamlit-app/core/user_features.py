import streamlit as st
from firebase_admin import firestore
from datetime import datetime

def add_favorite(user_id, word_data):
    """Add a word to user's favorites"""
    try:
        db = firestore.client()
        user_ref = db.collection('users').document(user_id)
        
        # Add word with timestamp
        favorite_entry = {
            **word_data,
            'favorited_at': datetime.now()
        }
        
        user_ref.update({
            'favorites': firestore.ArrayUnion([favorite_entry])
        })
        return True
    except Exception as e:
        st.error(f"Failed to add favorite: {e}")
        return False

def remove_favorite(user_id, word):
    """Remove a word from user's favorites"""
    try:
        db = firestore.client()
        user_ref = db.collection('users').document(user_id)
        user_data = user_ref.get().to_dict()
        
        # Filter out the word
        favorites = user_data.get('favorites', [])
        updated_favorites = [fav for fav in favorites if fav.get('word') != word]
        
        user_ref.update({'favorites': updated_favorites})
        return True
    except Exception as e:
        st.error(f"Failed to remove favorite: {e}")
        return False

def get_favorites(user_id):
    """Get user's favorite words"""
    try:
        db = firestore.client()
        user_doc = db.collection('users').document(user_id).get()
        if user_doc.exists:
            return user_doc.to_dict().get('favorites', [])
        return []
    except Exception as e:
        st.error(f"Failed to fetch favorites: {e}")
        return []

def is_favorited(user_id, word):
    """Check if a word is in user's favorites"""
    favorites = get_favorites(user_id)
    return any(fav.get('word') == word for fav in favorites)

def add_custom_affix(user_id, affix_type, affix_value):
    """Add a custom affix to user's library"""
    try:
        db = firestore.client()
        user_ref = db.collection('users').document(user_id)
        
        user_ref.update({
            f'custom_affixes.{affix_type}': firestore.ArrayUnion([affix_value])
        })
        return True
    except Exception as e:
        st.error(f"Failed to add custom affix: {e}")
        return False

def get_custom_affixes(user_id):
    """Get user's custom affixes"""
    try:
        db = firestore.client()
        user_doc = db.collection('users').document(user_id).get()
        if user_doc.exists:
            return user_doc.to_dict().get('custom_affixes', {
                'prefixes': [],
                'roots': [],
                'suffixes': []
            })
        return {'prefixes': [], 'roots': [], 'suffixes': []}
    except Exception as e:
        st.error(f"Failed to fetch custom affixes: {e}")
        return {'prefixes': [], 'roots': [], 'suffixes': []}

def merge_affixes_with_custom(global_affixes, user_id):
    """Merge global affixes with user's custom affixes"""
    if not user_id:
        return global_affixes
    
    custom = get_custom_affixes(user_id)
    
    merged = {
        'prefixes': list(set(global_affixes['prefixes'] + custom['prefixes'])),
        'roots': list(set(global_affixes['roots'] + custom['roots'])),
        'suffixes': list(set(global_affixes['suffixes'] + custom['suffixes']))
    }
    
    # Sort for consistent display
    for key in merged:
        merged[key] = sorted(merged[key])
    
    return merged

def show_favorites_ui(lang="fa"):
    """Display user's favorites"""
    if not st.session_state.get('user_id'):
        st.info("لطفا ابتدا وارد شوید" if lang == "fa" else "Please login to view favorites")
        return
    
    favorites = get_favorites(st.session_state.user_id)
    
    if not favorites:
        st.info("هنوز کلمه‌ای را به علاقه‌مندی‌ها اضافه نکرده‌اید" if lang == "fa" else "No favorites yet")
        return
    
    st.subheader(f"⭐ علاقه‌مندی‌ها ({len(favorites)} مورد)" if lang == "fa" else f"⭐ Favorites ({len(favorites)})")
    
    for idx, fav in enumerate(reversed(favorites)):  # Most recent first
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"### {fav.get('word', '')}")
            st.caption(f"{fav.get('prefix', '')} + {fav.get('root', '')} + {fav.get('suffix', '')}")
        with col2:
            if st.button("🗑️", key=f"remove_fav_{idx}"):
                if remove_favorite(st.session_state.user_id, fav.get('word')):
                    st.success("حذف شد!" if lang == "fa" else "Removed!")
                    st.rerun()
        
        if idx < len(favorites) - 1:
            st.divider()
