# تفعيل النماذج الذكية الحقيقية — AI Research Agents

هذه التعليمات مخصصة لمالك مستودع AMMARICA1791/ai-research-agents.

## الحالة الحالية
توجد واجهة اتصال برمجية بمزوّد نماذج متوافق مع Chat Completions.
إذا لم يُسجّل GitHub Secret الخاص بالمفتاح واسم النموذج وعنوان الخدمة
فسيعمل المختبر بتحليل الشيفرة المحلي فقط. اشتراك ChatGPT لا يعني
تلقائياً وجود مفتاح API لخدمة GitHub Actions.

## خطوات التفعيل من التابلت
1. لدى مزود النماذج المعتمد، أنشئ مفتاح API في حسابك الخاص وحدد حدود الإنفاق.
2. افتح صفحة Settings للمستودع في GitHub ثم Secrets and variables → Actions.
3. ضمن تبويب Variables أضف:
   - LAB_LLM_ENDPOINT : رابط HTTPS كامل ومتوافق مع chat completions.
     مثال OpenAI: https://api.openai.com/v1/chat/completions
   - LAB_LLM_MODEL : اسم نموذج متاح في حساب مزودك ويدعم حقول chat completions.
4. ضمن تبويب Secrets أضف **New repository secret** باسم
   LAB_LLM_API_KEY والصق المفتاح هناك فقط، لا في المحادثة أو في المستودع.
5. افتح Actions → Verify Real LLM Provider → Run workflow.
   سيظهر MODEL_ACTIVATION_STATUS=REMOTE_MODEL وLIVE_LLM_RESPONSE_CONFIRMED
   فقط إذا نجحت مكالمتان حقيقيتان إلى النموذج. إذا نقصت الإعدادات
   فسيظهر CONFIG_REQUIRED مع أسماء الحقول الناقصة دون كشف القيم.
6. بعدها افتح Actions → Research Lab - Persistent Missions → Run workflow
   مع تحديد enable_model=true. تشغيلات push التلقائية لا تستخدم النموذج
   المدفوع، إلا عند التشغيل اليدوي مع الموافقة.

## حدود الأمان والتكلفة
- مكالمتان فقط لكل مهمة بحثية مفعلة، بحد أقصى 250 رمز إجابة لكل مكالمة
  في المحول الحالي، وفق قابلية دعم المزود.
- لا يرسل المساعد شيفرة المشروع أو نص الأهداف أو أسماء الملفات للمزود؛
  ترسل أعداد المشاكل المصنفة فقط.
- لا يمنح المفتاح أي صلاحية للمساعد في تغيير الملفات أو الدمج.
- قد يطلب المزود تمويل رصيد API ويُحاسب على الاستخدام بشكل مستقل.
- لا تنشر المفتاح في أي مكان عام، ولا تضعه في Variables؛ يوضع في Secrets.
- اتصال GitHub في هذه المحادثة لا يملك إجراء إنشاء الأسرار، لذلك
  يجب على المالك تنفيذ الخطوات الخاصة بإعدادات GitHub بنفسه.

توثيق GitHub الرسمي: https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets
توثيق OpenAI لواجهة Chat Completions:
https://platform.openai.com/docs/api-reference/chat
