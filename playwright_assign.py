from playwright.sync_api import sync_playwright
import pandas as pd
import json
import random
import time
import os
from datetime import datetime

# ================================
# CONFIGURATION
# ================================
CONTACTS_FILE = "contacts.xlsx"
OUTPUT_DIR = "output"
MAX_MESSAGES = 3
LOGIN_TIMEOUT = 120000  # milliseconds
RANDOM_DELAY_MIN = 1.0   # seconds
RANDOM_DELAY_MAX = 3.0

# Create output folder
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ================================
# HELPER FUNCTIONS
# ================================
def random_delay(min_sec=RANDOM_DELAY_MIN, max_sec=RANDOM_DELAY_MAX):
    """Sleep for a random time to mimic human behaviour"""
    time.sleep(random.uniform(min_sec, max_sec))

def read_contacts(file_path):
    """Read contacts from Excel – expects a column named 'name'"""
    df = pd.read_excel(file_path)
    # If your column is called 'Name' or 'Contact', change it here
    return df['Name'].dropna().tolist()

def save_json(data, filename):
    with open(os.path.join(OUTPUT_DIR, filename), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def save_excel(data, filename):
    df = pd.DataFrame(data)
    df.to_excel(os.path.join(OUTPUT_DIR, filename), index=False)

# ================================
# MAIN AUTOMATION
# ================================
def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        context = browser.new_context()
        page = context.new_page()

        #page.wait_for_selector("div[aria-label='Chat list']", timeout=120000)
        #print("WhatsApp Loaded")
    
        # ---- STEP 1: Open WhatsApp Web and login ----
        print("🌐 Opening WhatsApp Web...")
        page.goto("https://web.whatsapp.com/")
        print("🔐 Scan the QR code within 2 minutes...")
        try:
            page.wait_for_selector("div[aria-label='Chat list']", timeout=LOGIN_TIMEOUT)
        except Exception:
            print("❌ Login timeout – did you scan the QR code?")
            browser.close()
            return
        print("✅ WhatsApp loaded successfully!")

        # ---- STEP 2: Read contacts ----
        time.sleep(5)
        contacts = read_contacts(CONTACTS_FILE)
        print(f"📇 Loaded {len(contacts)} contacts from {CONTACTS_FILE}")
        if not contacts:
            print("⚠️ No contacts found. Exiting.")
            browser.close()
            return

        results = []   # store data for each contact

        # ---- STEP 3: Process each contact ----
        for contact_name in contacts:
            print(f"\n🔍 Processing: {contact_name}")
            result_entry = {
                "contact": contact_name,
                "status": "success",
                "messages": [],
                "screenshot": None,
                "error": None
            }

            try:
                # --- 3a. Search for the contact ---
                # Click the search icon (or use the shortcut)
                page.click("div[aria-label='Search or start new chat']")
                random_delay()

                # Clear any existing text
                page.keyboard.press("Control+A")
                page.keyboard.press("Backspace")
                random_delay()

                # Type the contact name
                page.fill("div[aria-label='Search or start a new chat']", contact_name)
                random_delay(2.0, 4.0)  # give search results time

                # Find the contact in the list – using title attribute
                contact_selector = f"span[title='{contact_name}']"
                if not page.locator(contact_selector).count():
                    print(f"⚠️ Contact '{contact_name}' not found – skipping")
                    result_entry["status"] = "not found"
                    results.append(result_entry)
                    continue

                # Click on the contact to open the chat
                page.locator(contact_selector).click()
                random_delay(2.0, 4.0)

                # --- 3b. Extract last N messages ---
                msg_selector = "div[data-testid='msg-container']"
                # Wait for at least one message to appear
                page.wait_for_selector(msg_selector, timeout=10000)

                # Get all message containers
                messages_elements = page.locator(msg_selector).all()
                # Take the last MAX_MESSAGES (or all if fewer)
                last_messages = messages_elements[-MAX_MESSAGES:]

                for msg_elem in last_messages:
                    # Extract text – some messages may be media only
                    try:
                        text = msg_elem.locator("span[aria-label*='message']").text_content() or ""
                    except:
                        text = "[media or unsupported]"

                    # Determine sender (outgoing = me)
                    is_outgoing = "msg-outgoing" in (msg_elem.get_attribute("data-testid") or "")
                    sender = "You" if is_outgoing else "Contact"

                    result_entry["messages"].append({
                        "sender": sender,
                        "text": text.strip() or "[empty]"
                    })

                # Reverse to have newest first (optional)
                result_entry["messages"].reverse()

                # --- 3c. Take a screenshot of the chat ---
                safe_name = contact_name.replace(" ", "_")
                screenshot_path = os.path.join(OUTPUT_DIR, f"{safe_name}.png")
                page.screenshot(path=screenshot_path)
                result_entry["screenshot"] = f"{safe_name}.png"

                print(f"✅ Extracted {len(result_entry['messages'])} messages")

            except Exception as e:
                print(f"❌ Error processing {contact_name}: {str(e)}")
                result_entry["status"] = "error"
                result_entry["error"] = str(e)

            results.append(result_entry)

            # Random pause before next contact
            random_delay(3.0, 6.0)

        # ---- STEP 4: Generate reports ----
        print("\n📊 Generating reports...")

        # JSON report (full structure)
        save_json(results, "results.json")

        # Excel report (flattened: one row per message)
        excel_rows = []
        for res in results:
            if not res["messages"]:
                excel_rows.append({
                    "contact": res["contact"],
                    "status": res["status"],
                    "sender": "",
                    "message": "",
                    "screenshot": res.get("screenshot", ""),
                    "error": res.get("error", "")
                })
            else:
                for msg in res["messages"]:
                    excel_rows.append({
                        "contact": res["contact"],
                        "status": res["status"],
                        "sender": msg["sender"],
                        "message": msg["text"],
                        "screenshot": res.get("screenshot", ""),
                        "error": res.get("error", "")
                    })
        save_excel(excel_rows, "results.xlsx")

        print(f"✅ Reports saved in '{OUTPUT_DIR}' folder")
        print("🎉 Done! Closing browser...")
        browser.close()

if __name__ == "__main__":
    main()