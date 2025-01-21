import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackContext,
)

TOKEN = '7997069106:AAHe98Ii68ICmv0nnzn6h-r_I39vEibf2_4'

# رسالة الترحيب
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        'مرحبا!\n'
        'أرسل لي ملفًا نصيًا يحتوي على URL:اسم المستخدم:كلمة المرور.\n'
        '\nالأوامر المتاحة:\n'
        '/fetch - استرجاع البيانات من الملف.\n'
        '/list - عرض محتويات الملف.\n'
        '/clear - حذف الملف.\n'
        '/help - عرض هذه القائمة مرة أخرى.\n'
        '/url <URL> - البحث عن بيانات URL معين.\n'
        '/user <اسم المستخدم> - البحث عن بيانات مستخدم معين.\n'
        '/add <URL>:<اسم المستخدم>:<كلمة المرور> - إضافة بيانات جديدة إلى الملف.\n'
        '/update <URL>:<اسم المستخدم>:<كلمة المرور> - تحديث بيانات URL معين.'
    )

# معالجة الملفات النصية
def handle_file(update: Update, context: CallbackContext):
    file = update.message.document.get_file()
    file_path = 'data.txt'
    file.download(file_path)

    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()

        # التحقق من صحة البيانات
        for line in lines:
            if not line.strip() or len(line.split(':')) != 3:
                raise ValueError("تنسيق الملف غير صحيح. تأكد أن كل سطر يحتوي على URL:اسم المستخدم:كلمة المرور.")

        update.message.reply_text('تم تحميل الملف بنجاح! يمكنك الآن استخدام الأوامر الأخرى.')
    except Exception as e:
        os.remove(file_path)  # حذف الملف إذا كان غير صالح
        update.message.reply_text(f'حدث خطأ أثناء معالجة الملف: {e}')

# استرجاع البيانات
def fetch_data(update: Update, context: CallbackContext):
    file_path = 'data.txt'
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            content = f.read()
        update.message.reply_text(f'تم استرجاع المحتوى:\n{content}')
    else:
        update.message.reply_text('لا يوجد ملف لتحميل البيانات منه. أرسل ملفًا أولاً.')

# عرض قائمة البيانات
def list_data(update: Update, context: CallbackContext):
    file_path = 'data.txt'
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            lines = f.readlines()
        if lines:
            formatted_data = '\n'.join([f'{i + 1}. {line.strip()}' for i, line in enumerate(lines)])
            update.message.reply_text(f'محتويات الملف:\n{formatted_data}')
        else:
            update.message.reply_text('الملف فارغ.')
    else:
        update.message.reply_text('لا يوجد ملف لتحميل البيانات منه.')

# حذف الملف
def clear_file(update: Update, context: CallbackContext):
    file_path = 'data.txt'
    if os.path.exists(file_path):
        os.remove(file_path)
        update.message.reply_text('تم حذف الملف بنجاح.')
    else:
        update.message.reply_text('لا يوجد ملف لحذفه.')

# عرض قائمة المساعدة
def help_command(update: Update, context: CallbackContext):
    update.message.reply_text(
        'الأوامر المتاحة:\n'
        '/start - بدء المحادثة وعرض التعليمات.\n'
        '/fetch - استرجاع البيانات من الملف.\n'
        '/list - عرض محتويات الملف.\n'
        '/clear - حذف الملف.\n'
        '/help - عرض هذه القائمة.\n'
        '/url <URL> - البحث عن بيانات URL معين.\n'
        '/user <اسم المستخدم> - البحث عن بيانات مستخدم معين.\n'
        '/add <URL>:<اسم المستخدم>:<كلمة المرور> - إضافة بيانات جديدة إلى الملف.\n'
        '/update <URL>:<اسم المستخدم>:<كلمة المرور> - تحديث بيانات URL معين.'
    )

# البحث عن بيانات بناءً على URL
def search_by_url(update: Update, context: CallbackContext):
    file_path = 'data.txt'
    if os.path.exists(file_path):
        if len(context.args) != 1:
            update.message.reply_text('يرجى كتابة الأمر بالشكل التالي: /url <URL>.')
            return
        search_url = context.args[0]
        with open(file_path, 'r') as f:
            lines = f.readlines()
        results = [line.strip() for line in lines if line.startswith(search_url)]
        if results:
            update.message.reply_text(f'نتائج البحث عن URL:\n{chr(10).join(results)}')
        else:
            update.message.reply_text('لم يتم العثور على أي بيانات لهذا URL.')
    else:
        update.message.reply_text('لا يوجد ملف للبحث فيه. أرسل ملفًا أولاً.')

# البحث عن بيانات بناءً على اسم المستخدم
def search_by_user(update: Update, context: CallbackContext):
    file_path = 'data.txt'
    if os.path.exists(file_path):
        if len(context.args) != 1:
            update.message.reply_text('يرجى كتابة الأمر بالشكل التالي: /user <اسم المستخدم>.')
            return
        search_user = context.args[0]
        with open(file_path, 'r') as f:
            lines = f.readlines()
        results = [line.strip() for line in lines if line.split(':')[1] == search_user]
        if results:
            update.message.reply_text(f'نتائج البحث عن اسم المستخدم:\n{chr(10).join(results)}')
        else:
            update.message.reply_text('لم يتم العثور على أي بيانات لهذا المستخدم.')
    else:
        update.message.reply_text('لا يوجد ملف للبحث فيه. أرسل ملفًا أولاً.')

# إضافة بيانات جديدة إلى الملف
def add_data(update: Update, context: CallbackContext):
    file_path = 'data.txt'
    if len(context.args) != 1:
        update.message.reply_text('يرجى كتابة الأمر بالشكل التالي: /add <URL>:<اسم المستخدم>:<كلمة المرور>.')
        return

    new_entry = context.args[0]
    if len(new_entry.split(':')) != 3:
        update.message.reply_text('تنسيق البيانات غير صحيح. تأكد من استخدام التنسيق: <URL>:<اسم المستخدم>:<كلمة المرور>.')
        return

    with open(file_path, 'a') as f:
        f.write(new_entry + '\n')

    update.message.reply_text('تمت إضافة البيانات بنجاح.')

# تحديث بيانات موجودة
def update_data(update: Update, context: CallbackContext):
    file_path = 'data.txt'
    if not os.path.exists(file_path):
        update.message.reply_text('لا يوجد ملف لتحديث البيانات فيه. أرسل ملفًا أولاً.')
        return

    if len(context.args) != 1:
        update.message.reply_text('يرجى كتابة الأمر بالشكل التالي: /update <URL>:<اسم المستخدم>:<كلمة المرور>.')
        return

    updated_entry = context.args[0]
    if len(updated_entry.split(':')) != 3:
        update.message.reply_text('تنسيق البيانات غير صحيح. تأكد من استخدام التنسيق: <URL>:<اسم المستخدم>:<كلمة المرور>.')
        return

    url_to_update = updated_entry.split(':')[0]
    updated_lines = []
    updated = False

    with open(file_path, 'r') as f:
        lines = f.readlines()

    for line in lines:
        if line.startswith(url_to_update):
            updated_lines.append(updated_entry + '\n')
            updated = True
        else:
            updated_lines.append(line)

    with open(file_path, 'w') as f:
        f.writelines(updated_lines)

    if updated:
        update.message.reply_text('تم تحديث البيانات بنجاح.')
    else:
        update.message.reply_text('لم يتم العثور على URL للتحديث.')

# الوظيفة الرئيسية
def main():
    application = ApplicationBuilder().token(TOKEN).build()

    # إضافة المعالجات
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("fetch", fetch_data))
    application.add_handler(CommandHandler("list", list_data))
    application.add_handler(CommandHandler("clear", clear_file))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("url", search_by_url))
    application.add_handler(CommandHandler("user", search_by_user))
    application.add_handler(CommandHandler("add", add_data))
    application.add_handler(CommandHandler("update", update_data))

    # بدء البوت
    application.run_polling()

if __name__ == '__main__':
    main()