from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
)
import datetime
import os
from aiohttp import web
import asyncio
import telegram

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")




# Define Years (from 2017 to current year)
CURRENT_YEAR = datetime.datetime.now().year
YEARS = [str(year) for year in range(2017, CURRENT_YEAR + 1)]

# Semesters
SEMESTERS = ["Spring", "Fall", "Summer"]

# Departments
MAIN_OPTIONS = {
    "Computer Eng": "computer_eng",
    "Computer Science": "computer_science",
    "Security": "security",
    "AI": "ai"
}

# Course Codes
COURSE_CODES = {
    "computer_eng": [  "ESPU1081", "MATH105", "CSBP119", "PHYS105", "GEIT112",
    "CSBP121", "Phys135", "CENG202", "MATH110", "CSBP219",
    "CENG205", "CSBP221", "HSS105", "MATH140", "CENG201",
    "CENG231", "PHYS110", "PHYS140", "GESU121", "CSBP319",
    "ELEC370", "ELEC375", "CENG328", "CENG329", "STAT210",
    "ITBP301", "CENG530", "SWEB300", "ITBP418", "ITBP480",
    "ITBP495", "MATH275", "CENG221", "PHYS231", "CENG210",
    "BIOC100/CHEM111", "ISLM100", "CENG320", "CENG324",
    "CENG325", "CSBP315", "CENG529", "ITBP481", "ITBP370"],
    "computer_science": [ "MATH105", "MATH110", "PHYS105", "CENG205", "CENG202",
    "CSBP119", "CSBP219", "MATH140", "CSBP221", "CSBP315",
    "CSBP319", "BIOC100/CHEM111", "CENG210", "STAT210",
    "CSBP340", "ITBP370", "SWEB300", "ITBP301", "CSBP316",
    "CSBP400", "CSBP301", "CSBP461", "ITBP321", "GESU121",
    "CSBP411", "CSBP421", "ISLM100", "ITBP480", "CSBPxxx",
    "ITBP481", "ITBP495"],
    "security": [ "ESPU1081", "MATH105", "CSBP119", "PHYS105", "GEIT112",
    "CSBP121", "CENG210", "CSBP315", "BIOC100/CHEM111",
    "CSBP319", "ISEC311", "ISEC312", "CSBP320", "ISEC411",
    "ISEC421", "ISEC321", "ITBP480", "ISEC414", "ITBP495",
    "CENG202", "MATH110", "CSBP219", "CENG205", "CSBP221",
    "HSS105", "ITBP301", "CSBP340", "ITBP370", "ISLM1103",
    "STAT210", "ISEC322", "ISEC323", "ISEC324", "ITBP418",
    "ISEC412", "ISEC422", "ITBP481", "ISEC413", "ISEC423"]}

# Flatten all course codes into one list
ALL_COURSES = [course for courses in COURSE_CODES.values() for course in courses]

# Store user selections
user_data = {}
async def handle_root(request):
    return web.Response(text="✅ Bot is alive!")


### 🔹 1️⃣ Start Command ###
async def start(update: Update, context):
    """Start command to introduce the bot."""
    
    keyboard = [[InlineKeyboardButton(text, callback_data=data)] for text, data in MAIN_OPTIONS.items()]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "📌 **Welcome!**\n1️⃣ Select a department.\n2️⃣ Click on a course or search.\n3️⃣ Choose a year & semester.\n4️⃣ Enter professor's name & upload a file.",
        reply_markup=reply_markup
    )
    user_data[update.message.chat_id] = {"waiting_for_search": False, "waiting_for_professor": False}

### 🔹 2️⃣ Handle Department Selection ###
async def handle_selection(update: Update, context):
    """Handles department selection."""
    query = update.callback_query
    await query.answer()

    selected_department = query.data
    user_data[query.message.chat_id] = {
        "department": selected_department, 
        "waiting_for_search": False, 
        "waiting_for_professor": False
    }

    courses = COURSE_CODES.get(selected_department, [])

    keyboard = [[InlineKeyboardButton(course, callback_data=f"course_{course}")] for course in courses]
    keyboard.append([InlineKeyboardButton("🔍 Search Course", callback_data="search_course")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.edit_text("📚 **Select a Course or Search Below:**", reply_markup=reply_markup)

### 🔹 3️⃣ Handle Course Selection ###
### 🔹 3️⃣ Handle Course Selection ###
async def handle_course_selection(update: Update, context):
    """Handles course selection and shows year options."""
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat_id

    # Ensure the chat_id exists in user_data
    if chat_id not in user_data:
        user_data[chat_id] = {
            "waiting_for_search": False,
            "waiting_for_professor": False,
            "department": None,
            "course": None,
            "year": None,
            "semester": None,
            "professor": None
        }

    if query.data == "search_course":
        user_data[chat_id]["waiting_for_search"] = True
        user_data[chat_id]["waiting_for_professor"] = False  # Ensure professor mode is disabled
        await query.message.edit_text("🔎 **Enter a course name or code to search:**")
        return

    selected_course = query.data.split("_")[1]
    user_data[chat_id]["course"] = selected_course
    user_data[chat_id]["waiting_for_search"] = False  # Disable search mode

    keyboard = [[InlineKeyboardButton(year, callback_data=f"year_{year}")] for year in YEARS]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.edit_text(f"📆 **Select Year for {selected_course}:**", reply_markup=reply_markup)


### 🔹 4️⃣ Handle Course Search (All Departments) ###
### 🔹 4️⃣ Handle Course Search (All Departments) ###
### 🔹 4️⃣ Handle Course Search (All Departments) ###
async def search_course(update: Update, context):
    """Handles course search based on user input from all departments."""
    chat_id = update.message.chat_id

    # Ensure the bot is in search mode
    if not user_data.get(chat_id, {}).get("waiting_for_search", False):
        return  

    search_query = update.message.text.strip().upper()  # Convert input to uppercase for case-insensitive search
    if not search_query.isalnum():
        await update.message.reply_text("❌ **Invalid Input!**\nPlease enter a valid course code (e.g., CSBP119).")
        return
    # Find matching courses and remove duplicates using set()
    matched_courses = list(set([course for course in ALL_COURSES if search_query in course]))

    if matched_courses:
        # Show valid courses as selectable buttons
        keyboard = [[InlineKeyboardButton(course, callback_data=f"course_{course}")] for course in matched_courses]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("✅ **Search Results:**", reply_markup=reply_markup)

        # Stop waiting for input
        user_data[chat_id]["waiting_for_search"] = False  
    else:
        # Show an error and allow user to try again
         await update.message.reply_text(
            "❌ **Course code not found!**\nPlease check the code and try again.\n\n"
            "Example: CSBP119, MATH105, ISEC311"
        )


### 🔹 5️⃣ Handle Year Selection ###
async def handle_year_selection(update: Update, context):
    """Handles year selection and shows semester options."""
    query = update.callback_query
    await query.answer()

    selected_year = query.data.split("_")[1]
    user_data[query.message.chat_id]["year"] = selected_year

    keyboard = [[InlineKeyboardButton(sem, callback_data=f"semester_{sem}")] for sem in SEMESTERS]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.edit_text("📅 **Select Semester:**", reply_markup=reply_markup)


### 🔹 6️⃣ Handle Semester Selection ###
async def handle_semester_selection(update: Update, context):
    """Handles semester selection and asks for professor's name."""
    query = update.callback_query
    await query.answer()

    selected_semester = query.data.split("_")[1]
    user_data[query.message.chat_id]["semester"] = selected_semester

    user_data[query.message.chat_id]["waiting_for_professor"] = True  # Enable professor name input
    user_data[query.message.chat_id]["waiting_for_search"] = False  # Ensure search mode is disabled

    await query.message.edit_text("👨‍🏫 **Enter the professor's name** (Max 20 characters):")

async def handle_professor_name(update: Update, context):
    """Handles professor name input properly."""
    chat_id = update.message.chat_id

    if not user_data.get(chat_id, {}).get("waiting_for_professor", False):
        await update.message.delete()
        return

    professor_name = update.message.text.strip()

    if len(professor_name) > 20:
        await update.message.reply_text("❌ **Error:** Name too long! Please enter a name with 20 characters or less.")
        return

    user_data[chat_id]["professor"] = professor_name
    user_data[chat_id]["waiting_for_professor"] = False  

    await update.message.reply_text("📁 **Now upload the file (PDF, DOC, etc.)**")


### 🔹 9️⃣ Handle Invalid File Uploads ###
async def handle_invalid_upload(update: Update, context):
    """Handles invalid file uploads (images, videos, or unsupported files)."""
    await update.message.reply_text(
        "❌ **Invalid File Type!**\nPlease upload a valid document (PDF, DOC, DOCX, TXT) only."
    )

### 🔹 8️⃣ Handle File Upload ###
### 🔹 8️⃣ Handle File Upload ###
async def handle_file_upload(update: Update, context):
    """Handles file uploads and ensures only valid document types are accepted."""
    chat_id = update.message.chat_id
    file = update.message.document

    # Ensure that a file is uploaded
    if not file:
        await update.message.reply_text("❌ **Error:** No file detected. Please upload a valid document.")
        return

    # Get the file type (MIME type)
    file_type = file.mime_type

    # Define allowed document MIME types
    # Define allowed document MIME types (including ZIP files)
    allowed_types = ["application/pdf", "application/msword",
                 "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                 "text/plain", "application/zip", "application/x-zip-compressed"]


    if file_type not in allowed_types:
        await update.message.reply_text(
            "❌ **Invalid File Type!**\nPlease upload a document file (PDF, DOC, DOCX, etc.. )."
        )
        return

    # Retrieve user data
    course = user_data.get(chat_id, {}).get("course", "Unknown Course")
    year = user_data.get(chat_id, {}).get("year", "Unknown Year")
    semester = user_data.get(chat_id, {}).get("semester", "Unknown Semester")
    professor = user_data.get(chat_id, {}).get("professor", "Unknown Professor")

    summary = f"📖 {course} ({semester} {year}) - {professor}"

    # Send the document to the specified channel
    await context.bot.send_document(chat_id=CHANNEL_ID, document=file.file_id, caption=summary)

    # Confirm successful upload
    await update.message.reply_text(
        "✅ **File uploaded successfully!**\n\n"
        "🎓 Thank you for contributing! Your upload will help other students access valuable course materials. "
        "Together, we make learning easier for everyone! 📚✨"
    )
    GIF_URL = "https://64.media.tumblr.com/99bd529dd5cfcc606c327abe4be392ce/6116479ccc0098fa-62/s1280x1920/f721463409f800ef4783cc0c7fab7a07e6d72cec.gifv"  # Replace with the actual direct GIF link
    await context.bot.send_animation(chat_id=chat_id, animation=GIF_URL)
    

async def ping(update: Update, context):
    await update.message.reply_text("✅ Bot is alive!")
async def webhook_handler(request):
    update = telegram.Update.de_json(await request.json(), app.bot)
    await app.process_update(update)
    return web.Response()

async def root_handler(request):
    return web.Response(text="✅ Bot is alive!")
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle_selection, pattern="^(computer_eng|computer_science|security|ai)$"))
app.add_handler(CallbackQueryHandler(handle_course_selection, pattern="^course_.*$|search_course"))
app.add_handler(CallbackQueryHandler(handle_year_selection, pattern="^year_.*$"))
app.add_handler(CallbackQueryHandler(handle_semester_selection, pattern="^semester_.*$"))
 
app.add_handler(MessageHandler(filters.Regex(r'^[A-Za-z ]+$'), handle_professor_name))
app.add_handler(MessageHandler(filters.Regex(r'^[A-Za-z0-9]+$'), search_course))
app.add_handler(MessageHandler(filters.Document.ALL, handle_file_upload))
app.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO | filters.AUDIO, handle_invalid_upload))  # Reject invalid files
app.add_handler(CommandHandler("ping", ping))

async def main():
    await app.initialize()
    await app.start()

    web_app = web.Application()
    web_app.router.add_get("/", root_handler)  # For UptimeRobot
    web_app.router.add_post(f"/{TOKEN}", webhook_handler)  # Telegram webhook

    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 5000)
    print("✅ Bot & Webhook running on port 5000")
    await site.start()

    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
