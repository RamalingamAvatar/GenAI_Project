from playwright.async_api import async_playwright
from datetime import datetime
import pandas as pd
import asyncio

print("Starting the Playwright script...")
print(f"Current date and time: {datetime.now()}")
start_time = datetime.now()

#Steps to automate:
#1. Launch the Chromium Browser
#2. Navigate to https://web.whatsapp.com/
#3. Read the "contacts.xlsx" and read the Name, Number and Personalized message from the sheet
#4. Search the contact in the whatsapp web and generate the personalized message for the contact
#5. Extract the last 3 sent messages in the chat
#6. Save it in a JSON and excel file for all the contacts read from the excel sheet

async def get_last_three_messages():
    async with async_playwright() as p:
        user_data_dir = "./whatsapp_session"
        browser = await p.chromium.launch_persistent_context(
            user_data_dir,
            headless = False,
            args = ["--start-maximized"]
        )
        print("Launching the Chromium browser...")
        page = browser.pages[0]

        print("Navigating to WhatsApp Web...")
        await page.goto("https://web.whatsapp.com/")

         # Wait for the chat application to load fully
        print("Waiting for chat list to load (Scan QR code if prompted)...")
        await page.wait_for_selector("div[data-testid='chat-list']", timeout=60000)

        #Read the contacts from the excel sheet and send the personalized message to each contact
        contacts_df = pd.read_excel("contacts.xlsx")
        messages_data = {}
        for index, row in contacts_df.iterrows():
            contact_name = row['Name']
            contact_number = row['Number']
            personalized_message = row['Message']

            
            print(f"Searching for contact: {contact_name} ({contact_number})")
            search_box = page.get_by_placeholder("Search or start a new chat")
            await search_box.fill(contact_name)
            await page.wait_for_timeout(2000)  # Wait for the search results to load

            # Click on the contact from the search results
            #contact_locator = page.locator(f"span[title='{contact_name}']")
            contact_locator = page.locator(f"(//*[contains(text(),'{contact_name}')])[1]")
            if await contact_locator.count() > 0:
                await contact_locator.first.click()
                print(f"Contact {contact_name} found. Sending message...")
                message_box = page.locator("div[contenteditable='true']").last
                await message_box.fill(personalized_message)
                await message_box.press("Enter")
                await page.wait_for_timeout(20000)
                print(f"Message sent to {contact_name}.")
            else:
                print(f"Contact {contact_name} not found.")

            print(f"Opening chat with: {contact_name}")

            chat_selector = f"span[title='{contact_name}']"
            await page.wait_for_selector(chat_selector)
            await page.click(chat_selector)

            # Wait briefly for the chat window content to render
            await page.wait_for_timeout(3000)

            # WhatsApp stores actual text bubbles inside 'span.copyable-text > span'
            message_selector = "span.copyable-text > span"
            await page.wait_for_selector(message_selector)

             # Fetch all available visible message elements in the open pane
            message_elements = await page.locator(message_selector).all()

            # Grab the text content of the last 3 elements
            last_three_elements = message_elements[-3:]
            text_data = []
            for i, locator in enumerate(last_three_elements, 1):
                # Use await to resolve the text from each locator object
                text = await locator.text_content()
                text_data.append(text)

            #Save the message with name in JSON and Excel file
            messages_data[contact_name] = {
                "Name": contact_name,
                "Number": contact_number,
                "Last_3_Messages": text_data
            }

        date_now = datetime.now().strftime("%Y-%m-%d")
        file_name = f'whatsapp_report_{date_now}'

        # Save the messages data to a JSON file
        messages_df = pd.DataFrame.from_dict(messages_data, orient='index')
        messages_df.to_json(f"{file_name}.json", orient='index', indent=4)

        #Update Excel file with the last 3 messages
        messages_df.to_excel(f"{file_name}.xlsx", index=False)

        # Keep the session alive briefly before closing
        await page.wait_for_timeout(2000)
        await browser.close()

asyncio.run(get_last_three_messages())

print("Playwright script completed successfully.")
print(f"Current date and time: {datetime.now()}")
end_time = datetime.now()
run_time = end_time - start_time
print(f"Total time taken for the script to run: {run_time}")