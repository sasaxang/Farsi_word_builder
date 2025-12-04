# 📖 Farsi Word Builder User Guide

<div style="background-color: #e3f2fd; padding: 15px; border-radius: 8px; border-left: 4px solid #2196F3;">

**Version:** 1.0  
**Date:** November 2025  
**For:** Non-technical users

</div>

---

## 📑 Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Understanding the Interface](#understanding-the-interface)
4. [Building Your First Word](#building-your-first-word)
5. [Using the Random Generator](#using-the-random-generator)
6. [Locking Components](#locking-components)
7. [Nominal Form](#nominal-form)
8. [Adding New Affixes](#adding-new-affixes)
9. [Advanced Tips](#advanced-tips)
10. [Troubleshooting](#troubleshooting)

---

## 🎯 Introduction

### What is Farsi Word Builder?

Farsi Word Builder is an online tool that helps you create new and creative Farsi words. The application combines **prefixes**, **roots**, and **suffixes** to generate new words.

<div style="background-color: #fff3e0; padding: 12px; border-radius: 6px; margin: 10px 0;">

💡 **Example:** Combining prefix "بی" + root "گربه" + suffix "گاه" = **بی‌گربه‌گاه**

</div>

### What Can You Do?

✅ Build new words by manually selecting components  
✅ Generate random words  
✅ Lock part of a word and change the rest  
✅ Apply nominal form to words  
✅ Add new prefixes, roots, or suffixes  

---

## 🚀 Getting Started

### Accessing the Application

1. Open your web browser (Chrome, Firefox, Safari, etc.)
2. Navigate to the application URL
3. The main Farsi Word Builder interface will appear

### Changing Language

At the top of the page, you can switch between **فارسی** and **English**.

![Main Interface](screenshots/main_interface_en.png)
*Figure 1: Main application interface in English*

---

## 🖥️ Understanding the Interface

The user interface consists of the following sections:

### 1. Word Structure Selector

<div style="background-color: #f3e5f5; padding: 12px; border-radius: 6px; margin: 10px 0;">

📐 **Word Structure** determines which components will be used in your word:

- **Prefix + Root** (e.g. بی‌گربه)
- **Root + Suffix** (e.g. گربه‌گاه)
- **Prefix + Root + Suffix** (e.g. خویش‌گربه‌پرداز)

</div>

![Word Structure](screenshots/word_structure_en.png)
*Figure 2: Word structure selection menu*

### 2. Affix and Root Selectors

Each selector includes:
- **Label** with count of available items (e.g., Root (34))
- **Dropdown menu** for selection
- **Lock checkbox** to keep it fixed

![Affix Selectors](screenshots/affix_counts_en.png)
*Figure 3: Prefix, root, and suffix selectors with item counts*

<div style="background-color: #e8f5e9; padding: 12px; border-radius: 6px; margin: 10px 0;">

📊 **Item Counts** show how many options are available in each category:
- Prefix (23)
- Root (34)
- Suffix (68)

</div>

### 3. Nominal Form Checkbox

This option converts the word to its nominal form (more details in the [Nominal Form](#nominal-form) section)

### 4. Generated Word Display

The final word is displayed in a blue box with animation.

![Generated Word](screenshots/generated_word_en.png)
*Figure 4: Display of generated word*

### 5. Random Button and Combinations Counter

<div style="background-color: #fce4ec; padding: 12px; border-radius: 6px; margin: 10px 0;">

🎲 **"Spin Random!" button** generates a random word  
🔢 **Combinations counter** shows the total number of possible combinations

</div>

![Random Button](screenshots/random_button_en.png)
*Figure 5: Random button and total combinations counter*

---

## 🎨 Building Your First Word

### Step by Step:

#### Step 1: Select Word Structure

1. Click on the **Word Structure** menu
2. Choose one of the three options
3. For starters, select **Prefix + Root + Suffix**

#### Step 2: Select Prefix

1. Click on the **Prefix** menu
2. Choose a prefix (e.g., **بی**)

#### Step 3: Select Root

1. Click on the **Root** menu
2. Choose a root (e.g., **گربه**)

#### Step 4: Select Suffix

1. Click on the **Suffix** menu
2. Choose a suffix (e.g., **گاه**)

#### Step 5: See the Result

The generated word (**بی‌گربه‌گاه**) is displayed in the blue box! 🎉

<div style="background-color: #fff9c4; padding: 12px; border-radius: 6px; margin: 10px 0;">

⚠️ **Note:** Some combinations may not be valid due to linguistic rules. The application automatically prevents invalid combinations.

</div>

---

## 🎲 Using the Random Generator

### How Does It Work?

The **Spin Random!** button automatically generates a random word.

### Steps to Use:

1. Select your desired word structure
2. Click the **Spin Random!** button
3. A new word is generated!
4. Click again for another word

### Total Possible Combinations

Next to the random button, the total number of possible combinations is displayed:

<div style="background-color: #e1f5fe; padding: 12px; border-radius: 6px; margin: 10px 0; text-align: center; font-size: 1.1em;">

**Total Possible Combinations: 2076**

</div>

This number is calculated based on:
- The selected word structure
- Number of prefixes, roots, and suffixes
- Linguistic rules (e.g., the "انه" suffix cannot follow roots ending in "ه", "ا", or "آ")

---

## 🔒 Locking Components

### Why Lock?

Sometimes you want to keep part of the word fixed and only change the rest.

### How to Lock?

1. Select the desired components
2. Check the **Lock** checkbox next to that component
3. Now when you click **Spin Random!**, only unlocked components will change

![Lock Example](screenshots/lock_example_en.png)
*Figure 6: Example of locking the root*

<div style="background-color: #f1f8e9; padding: 12px; border-radius: 6px; margin: 10px 0;">

💡 **Practical Example:**  
Lock the root "گربه" and repeatedly click random to try different prefixes and suffixes with this root!

</div>

---

## 📝 Nominal Form

### What is Nominal Form?

Nominal form is a suffix added to the end of a word to convert it into a noun.

### How to Use?

1. Build a word
2. Check the **Nominal Form** checkbox
3. The word is converted to nominal form

### Examples:

| Without Nominal Form | With Nominal Form |
|---------------------|-------------------|
| بی‌گربه‌گاه | بی‌گربه‌گاهی |
| خویش‌گربه‌پرداز | خویش‌گربه‌پردازی |
| گربه‌خوار | گربه‌خواری |

![Before Nominal Form](screenshots/nominal_before_en.png)
*Figure 7: Word without nominal form*

![After Nominal Form](screenshots/nominal_after_en.png)
*Figure 8: Same word with nominal form*

<div style="background-color: #ede7f6; padding: 12px; border-radius: 6px; margin: 10px 0;">

📚 **Rule:** The nominal form suffix varies depending on the last letter of the word:
- Words ending in "ا" or "و" → "یی"
- Words ending in "ه" → "ای" or "ی" (depending on the type of "ه")
- Other cases → "ی"

</div>

---

## ➕ Adding New Affixes

### How to Add?

#### Step 1: Open the Form

1. Click the **➕ Add Affix** button
2. The add form will open

![Add Button](screenshots/add_affix_collapsed_en.png)
*Figure 9: Add affix button*

#### Step 2: Enter Information

In the opened form:
1. **New Prefix:** If you want to add a prefix, type it here
2. **New Root:** If you want to add a root, type it here
3. **New Suffix:** If you want to add a suffix, type it here

![Add Form](screenshots/add_affix_expanded_en.png)
*Figure 10: Add affix form*

#### Step 3: Submit

1. Click the **✅ Add** button
2. If the input is valid, a success message will appear
3. The new affix or root is added to the list

<div style="background-color: #ffebee; padding: 12px; border-radius: 6px; margin: 10px 0;">

⚠️ **Important:** Only Persian text is acceptable. If you enter English text or numbers, you will receive an error message.

</div>

### Tips:

✅ You can add multiple items at once (e.g., one prefix and one root)  
✅ If an item already exists, it won't be added again  
✅ After adding, the item counts in the labels are updated  

---

## 🎓 Advanced Tips

### 1. Discovering Interesting Combinations

- Try different structures
- Use locks to focus on one component
- Click the random button multiple times

### 2. Understanding Linguistic Rules

The application automatically prevents some invalid combinations:

<div style="background-color: #fff3e0; padding: 12px; border-radius: 6px; margin: 10px 0;">

📖 **Example Rule:**  
The "انه" suffix cannot be used after roots ending in "ه" (except "اه"), "ا", or "آ".

**Valid:** دست + انه = دستانه ✅  
**Invalid:** گربه + انه ❌ (because "گربه" ends in "ه")

</div>

### 3. Using the Combinations Counter

- Larger number = more options to explore
- Changing the structure changes the number of combinations
- Locking components reduces the number of combinations

---

## 🔧 Troubleshooting

### Problem: Word is not generated

**Solution:**
- Make sure at least one root is selected
- Check that the appropriate word structure is selected

### Problem: Cannot select prefix or suffix

**Solution:**
- Check that the word structure includes that component
- If the dropdown is disabled, change the word structure

### Problem: Error message when adding affix

**Solution:**
- Make sure you entered Persian text
- Don't use English letters or numbers

### Problem: Some combinations are not created

**Solution:**
- This is normal! The application follows linguistic rules
- Some combinations are not allowed due to linguistic rules

---

<div style="background-color: #e8eaf6; padding: 20px; border-radius: 8px; text-align: center; margin-top: 30px;">

## 🎉 You're Ready!

With this guide, you can use all the features of the Farsi Word Builder.  
**Create creative words and have fun!** 🚀

---

**Have questions or problems?**  
Refer to the technical documentation or contact the developer.

</div>
