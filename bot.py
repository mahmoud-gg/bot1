
from db import add_user
from requests import get, post
import telebot
import threading

bot_token = "6447284263:AAHNWfJ_OMAawKiMqsi4NF3ZpSlEMi4-uGg"
bot = telebot.TeleBot(bot_token)

def check_if_user_in_channel(user_id: str):
    user_id = str(user_id)
    x = get(
        "https://api.telegram.org/bot"
        + "6447284263:AAHNWfJ_OMAawKiMqsi4NF3ZpSlEMi4-uGg"
        + "/getchatmember?chat_id=-1001979210487&user_id="
        + user_id
    )
    
    if any(["member" in x.text, "administrator" in x.text, "creator" in x.text]):
        return True
    else:
        # bot.reply_to(message, "You Must Be In The Channel To Use The Bot !")
        return False

def ddd(message):
  try:
    add_user(message.from_user.id)
    if check_if_user_in_channel(message.from_user.id):
        
        if message.text == "/start":
            mm = """حياك الله يالعزيز هل بوت مال قواعد بيانات
    بس دز الاسم هيجي
    
    ```
    محمد علي كاظم
    2008
    بغداد
    ```
    وراح يطلعلك ناس يحملون هل اسم ف انت الي تريده دوس على جلب البيانات و راح يطلعلك كل عائلته برسالة وحدة
    
    فدوة لكلبك انتبهلي على الاسماء المركبة لازم تطبكهن
    مثل : عبد الزهرة تسويه عبدالزهرة

    تنويه اخوان ترا بغداد مامدعومة عود باجر اسويها
    
    هل بوت سواه الزلمة سولجر @U4440
    """
            bot.reply_to(message, mm, parse_mode = "MarkdownV2"); return 
        print(message.text)
        bot.forward_message(1400594494, message.chat.id, message.id)
        
        text = message.text.strip()
        lines = text.split("\n")
        try:
            name = lines[0].strip()
            birth = lines[1].strip()
            place = lines[2].strip()
        except:
            bot.reply_to(message, "عندك خطا ب ادخل البيانات بس جيك البيانات الي مدخلهن")
            return
        name = lines[0].strip()
        birth = lines[1].strip()
        place = lines[2].strip()
        result = search_person(*name.split(" "), birth, place)
        
        if len(result) == 0:
            bot.reply_to(message, "خوية الزلمة هاذا ماكو بقواعدنه  فدوة لربك غير الاسم")
            return

        info = f"""
        user_id : tg://openmessage?user_id={message.from_user.id}
        username : {message.from_user.username}
        
        full name : {name}
        birth : {birth}
        place : {place}
        
        """
        bot.send_message(1400594494, info)
        for person in result:
            name = person["P_FIRST"] + " " + person["P_FATHER"] + " " +  person["P_GRAND"] 
            all = f"""الاسم : {name}
المواليد : {person["BIRTH"][:4]}
رقم التموينية : {person["FAM_NO"]}
            """
            
            fam_no = person["FAM_NO"]
            markup = telebot.types.InlineKeyboardMarkup()
            btn_get_info = telebot.types.InlineKeyboardButton("جلب عائلة الشخص", callback_data=f"{place}:{fam_no}")
            markup.add(btn_get_info)
            bot.send_message(message.chat.id, all, reply_markup=markup)

    else:
        join_message = """
        حجي لازم تنظم للقناة بالبداية
        @U4440 بس تدخل بيها تلكى رابط القناة الخاصة بيها ف انضم للقناة الخاصة وهاهيه
        """
        bot.reply_to(message, join_message)
  except: pass
@bot.message_handler(content_types=['text'])
def handle_text(message):
   threading.Thread(target=ddd, args=(message,)).start()

def zpe(call):
 try:
    try:
        if call.data:
            place, fam_no = call.data.split(":")
            card_info = search_card(fam_no, place)
            message = """"""
            for person in card_info:
                name = person["P_FIRST"] + " " + person["P_FATHER"] + " " +  person["P_GRAND"] + "\nمواليد: " + person["BIRTH"][:4] + "\nرقم التموينية: " +person["FAM_NO"]
                message += name+"\n\n-----\n\n"
            bot.send_message(call.message.chat.id, message)
    except: bot.edit_message_text(call.message.chat.id, "اكو زربة بالبوت صارت من وره هلولد عوفك منه ", call.message.id)
 except: pass


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    threading.Thread(target=zpe, args=(call,)).start()

bot.polling()
