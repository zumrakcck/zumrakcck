from pathlib import Path
import zipfile
from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor


ROOT = Path(__file__).resolve().parents[1]
DIAGRAMS = ROOT / "diagrams"
PRESENTATION = ROOT / "presentation"
ZIP_TIMESTAMP = (2026, 1, 1, 0, 0, 0)


def font(size=20, bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


F_TITLE = font(28, True)
F_HEAD = font(20, True)
F_BODY = font(16)
F_SMALL = font(13)


def text_size(draw, text, font_obj):
    box = draw.multiline_textbbox((0, 0), text, font=font_obj, spacing=4)
    return box[2] - box[0], box[3] - box[1]


def wrap(text, width=22):
    words = text.split()
    lines = []
    line = ""
    for word in words:
        candidate = f"{line} {word}".strip()
        if len(candidate) <= width:
            line = candidate
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return "\n".join(lines)


def ellipse(draw, center, size, label, fill="#ffffff", outline="#27364a"):
    x, y = center
    w, h = size
    box = (x - w // 2, y - h // 2, x + w // 2, y + h // 2)
    draw.ellipse(box, fill=fill, outline=outline, width=2)
    label = wrap(label, 18)
    tw, th = text_size(draw, label, F_SMALL)
    draw.multiline_text((x - tw / 2, y - th / 2), label, fill="#172033", font=F_SMALL, align="center", spacing=3)


def actor(draw, x, y, name):
    draw.ellipse((x - 16, y, x + 16, y + 32), outline="#172033", width=2)
    draw.line((x, y + 32, x, y + 95), fill="#172033", width=2)
    draw.line((x - 45, y + 55, x + 45, y + 55), fill="#172033", width=2)
    draw.line((x, y + 95, x - 38, y + 145), fill="#172033", width=2)
    draw.line((x, y + 95, x + 38, y + 145), fill="#172033", width=2)
    tw, _ = text_size(draw, name, F_SMALL)
    draw.text((x - tw / 2, y + 152), name, fill="#172033", font=F_SMALL)


def arrow(draw, start, end, fill="#27364a", width=2):
    draw.line((*start, *end), fill=fill, width=width)
    # Lightweight arrow head
    ex, ey = end
    sx, sy = start
    dx = ex - sx
    dy = ey - sy
    length = max((dx * dx + dy * dy) ** 0.5, 1)
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    p1 = (ex - 12 * ux + 6 * px, ey - 12 * uy + 6 * py)
    p2 = (ex - 12 * ux - 6 * px, ey - 12 * uy - 6 * py)
    draw.polygon([end, p1, p2], fill=fill)


def dashed(draw, start, end, fill="#27364a"):
    sx, sy = start
    ex, ey = end
    steps = 32
    for i in range(0, steps, 2):
        a = i / steps
        b = min((i + 1) / steps, 1)
        draw.line((sx + (ex - sx) * a, sy + (ey - sy) * a, sx + (ex - sx) * b, sy + (ey - sy) * b), fill=fill, width=2)


def save_vpd(path, title, content):
    path.write_text(f"Visual Paradigm text export - {title}\n\n{content}\n", encoding="utf-8")


def use_case():
    out = DIAGRAMS / "use-case"
    img = Image.new("RGB", (1280, 860), "#fff1b8")
    draw = ImageDraw.Draw(img)
    draw.rectangle((210, 40, 1050, 820), outline="#172033", width=2)
    draw.text((520, 55), "Pet Care Assistant", fill="#172033", font=F_TITLE)
    actor(draw, 90, 260, "Pet Owner")
    actor(draw, 1190, 330, "Admin")
    use_cases = {
        "Register / Login": (360, 125),
        "Validate User": (610, 125),
        "Add Pet": (360, 200),
        "Add Reminder": (360, 285),
        "View Pets": (360, 375),
        "Edit Pet Information": (635, 315),
        "Delete Pet": (635, 395),
        "View Reminders": (360, 500),
        "Edit Reminder": (635, 475),
        "Delete Reminder": (635, 555),
        "Chat with AI": (360, 635),
        "Suggest Veterinarian": (660, 610),
        "Validate Request": (660, 690),
        "Track Daily Activities": (360, 735),
        "Activate Premium": (360, 805),
        "Process Payment": (680, 775),
        "Show Payment Error": (690, 840),
        "Manage Users": (880, 325),
        "Manage Premium Status": (880, 430),
        "View Reports": (880, 535),
    }
    for label, pos in use_cases.items():
        ellipse(draw, pos, (150, 58), label, fill="#fffdf5")
    for target in ["Register / Login", "Add Pet", "Add Reminder", "View Pets", "View Reminders", "Chat with AI", "Track Daily Activities", "Activate Premium"]:
        arrow(draw, (135, 330), (use_cases[target][0] - 75, use_cases[target][1]), width=1)
    for target in ["Manage Users", "Manage Premium Status", "View Reports"]:
        arrow(draw, (1145, 405), (use_cases[target][0] + 75, use_cases[target][1]), width=1)
    rels = [
        ("Register / Login", "Validate User", "<<include>>"),
        ("View Pets", "Edit Pet Information", "<<extend>>"),
        ("View Pets", "Delete Pet", "<<extend>>"),
        ("View Reminders", "Edit Reminder", "<<extend>>"),
        ("View Reminders", "Delete Reminder", "<<extend>>"),
        ("Chat with AI", "Suggest Veterinarian", "<<extend>>"),
        ("Chat with AI", "Validate Request", "<<include>>"),
        ("Activate Premium", "Process Payment", "<<include>>"),
        ("Activate Premium", "Show Payment Error", "<<extend>>"),
    ]
    for a, b, label in rels:
        dashed(draw, use_cases[a], use_cases[b])
        mx = (use_cases[a][0] + use_cases[b][0]) / 2
        my = (use_cases[a][1] + use_cases[b][1]) / 2 - 15
        draw.text((mx - 38, my), label, fill="#172033", font=F_SMALL)
    img.save(out / "use-case-diagram.jpeg", quality=95)
    save_vpd(out / "use-case-diagram.vpd", "Use Case Diagram", "\n".join(use_cases.keys()))


def class_diagram():
    out = DIAGRAMS / "class"
    img = Image.new("RGB", (1280, 900), "#f7fbff")
    draw = ImageDraw.Draw(img)
    draw.text((500, 35), "Class Diagram", fill="#172033", font=F_TITLE)
    classes = {
        "User": (70, 110, ["userId", "name", "email", "passwordHash", "role"], ["register()", "login()", "validateUser()"]),
        "PetOwner": (70, 405, ["premiumStatus"], ["addPet()", "addReminder()", "chatWithAI()"]),
        "Admin": (70, 660, ["adminLevel"], ["manageUsers()", "viewReports()"]),
        "Pet": (395, 110, ["petId", "name", "type", "breed", "age", "weight"], ["updateInfo()", "deletePet()"]),
        "Reminder": (395, 405, ["reminderId", "title", "date", "category", "status"], ["create()", "edit()", "delete()"]),
        "DailyActivity": (395, 660, ["activityId", "activityType", "value", "activityDate"], ["track()"]),
        "AIChat": (730, 110, ["chatId", "message", "response"], ["validateRequest()", "suggestVeterinarian()"]),
        "PremiumSubscription": (730, 405, ["subscriptionId", "planName", "paymentStatus"], ["activate()", "processPayment()", "showPaymentError()"]),
        "Report": (730, 660, ["reportId", "reportType", "createdAt"], ["generate()"]),
    }
    boxes = {}
    for name, (x, y, attrs, methods) in classes.items():
        w, h = 245, 190
        boxes[name] = (x, y, x + w, y + h)
        draw.rectangle((x, y, x + w, y + h), fill="#ffffff", outline="#27364a", width=2)
        draw.rectangle((x, y, x + w, y + 38), fill="#dbeafe", outline="#27364a", width=2)
        tw, _ = text_size(draw, name, F_HEAD)
        draw.text((x + w / 2 - tw / 2, y + 8), name, fill="#172033", font=F_HEAD)
        draw.line((x, y + 102, x + w, y + 102), fill="#27364a", width=1)
        for i, attr in enumerate(attrs):
            draw.text((x + 12, y + 48 + i * 18), f"- {attr}", fill="#172033", font=F_SMALL)
        for i, method in enumerate(methods):
            draw.text((x + 12, y + 112 + i * 18), f"+ {method}", fill="#172033", font=F_SMALL)
    links = [("User", "PetOwner"), ("User", "Admin"), ("PetOwner", "Pet"), ("PetOwner", "Reminder"), ("PetOwner", "DailyActivity"), ("PetOwner", "AIChat"), ("PetOwner", "PremiumSubscription"), ("Admin", "Report")]
    for a, b in links:
        ax1, ay1, ax2, ay2 = boxes[a]
        bx1, by1, bx2, by2 = boxes[b]
        arrow(draw, (ax2, (ay1 + ay2) // 2), (bx1, (by1 + by2) // 2), width=2)
    img.save(out / "class-diagram.jpeg", quality=95)
    save_vpd(out / "class-diagram.vpd", "Class Diagram", "\n".join(classes.keys()))


def activity_diagram():
    out = DIAGRAMS / "activity"
    img = Image.new("RGB", (1000, 1400), "#fffdf7")
    draw = ImageDraw.Draw(img)
    draw.text((360, 35), "Activity Diagram", fill="#172033", font=F_TITLE)
    steps = [
        ("Start", "start"),
        ("Register / Login", "action"),
        ("Validate User", "decision"),
        ("Open Dashboard", "action"),
        ("Add or View Pet", "action"),
        ("Create Reminder", "action"),
        ("Track Daily Activity", "action"),
        ("Chat with AI", "action"),
        ("Need veterinarian?", "decision"),
        ("Suggest Veterinarian", "action"),
        ("Activate Premium", "action"),
        ("Process Payment", "decision"),
        ("Premium Active", "action"),
        ("Show Payment Error", "action"),
        ("End", "end"),
    ]
    positions = [(500, 105 + i * 85) for i in range(len(steps))]
    for (label, kind), (x, y) in zip(steps, positions):
        if kind in {"start", "end"}:
            draw.ellipse((x - 28, y - 28, x + 28, y + 28), fill="#172033" if kind == "start" else "#ffffff", outline="#172033", width=4)
            if kind == "end":
                draw.ellipse((x - 18, y - 18, x + 18, y + 18), fill="#172033")
        elif kind == "decision":
            draw.polygon([(x, y - 40), (x + 95, y), (x, y + 40), (x - 95, y)], fill="#fef3c7", outline="#27364a")
            tw, th = text_size(draw, wrap(label, 18), F_SMALL)
            draw.multiline_text((x - tw / 2, y - th / 2), wrap(label, 18), fill="#172033", font=F_SMALL, align="center")
        else:
            draw.rounded_rectangle((x - 140, y - 32, x + 140, y + 32), radius=20, fill="#dbeafe", outline="#27364a", width=2)
            tw, th = text_size(draw, label, F_BODY)
            draw.text((x - tw / 2, y - th / 2), label, fill="#172033", font=F_BODY)
    for i in range(len(positions) - 1):
        arrow(draw, (positions[i][0], positions[i][1] + 42), (positions[i + 1][0], positions[i + 1][1] - 42), width=2)
    draw.text((610, 790), "Yes", fill="#172033", font=F_SMALL)
    draw.text((610, 1045), "Success / Error", fill="#172033", font=F_SMALL)
    img.save(out / "activity-diagram.jpeg", quality=95)
    save_vpd(out / "activity-diagram.vpd", "Activity Diagram", "Login, pet care, reminder, AI, premium payment activity flow.")


def sequence_diagram():
    out = DIAGRAMS / "sequence"
    img = Image.new("RGB", (1300, 850), "#f8fafc")
    draw = ImageDraw.Draw(img)
    draw.text((520, 35), "Sequence Diagram", fill="#172033", font=F_TITLE)
    actors = ["Pet Owner", "Web App", "Auth Service", "Pet Service", "AI Service", "Payment Service"]
    xs = [100, 320, 540, 760, 980, 1190]
    for x, name in zip(xs, actors):
        draw.rounded_rectangle((x - 75, 90, x + 75, 135), radius=10, fill="#dbeafe", outline="#27364a", width=2)
        tw, _ = text_size(draw, name, F_SMALL)
        draw.text((x - tw / 2, 105), name, fill="#172033", font=F_SMALL)
        draw.line((x, 135, x, 790), fill="#94a3b8", width=2)
    messages = [
        (0, 1, 180, "Register / Login"),
        (1, 2, 230, "validateUser()"),
        (2, 1, 280, "session token"),
        (0, 1, 340, "Add Pet / Reminder"),
        (1, 3, 390, "save care data"),
        (3, 1, 440, "updated dashboard"),
        (0, 1, 510, "Chat with AI"),
        (1, 4, 560, "validateRequest()"),
        (4, 1, 610, "care answer + vet suggestion"),
        (0, 1, 680, "Activate Premium"),
        (1, 5, 730, "processPayment()"),
        (5, 1, 780, "success or payment error"),
    ]
    for a, b, y, label in messages:
        arrow(draw, (xs[a], y), (xs[b], y), width=2)
        draw.text(((xs[a] + xs[b]) / 2 - 65, y - 24), label, fill="#172033", font=F_SMALL)
    img.save(out / "sequence-diagram.jpeg", quality=95)
    save_vpd(out / "sequence-diagram.vpd", "Sequence Diagram", "\n".join(m[3] for m in messages))


def database_diagram():
    out = DIAGRAMS / "database"
    img = Image.new("RGB", (1250, 900), "#f9fafb")
    draw = ImageDraw.Draw(img)
    draw.text((485, 35), "Database Diagram", fill="#172033", font=F_TITLE)
    tables = {
        "users": (70, 110, ["PK user_id", "name", "email", "password_hash", "role", "premium_status"]),
        "pets": (390, 110, ["PK pet_id", "FK owner_id", "name", "type", "breed", "age", "weight"]),
        "reminders": (710, 110, ["PK reminder_id", "FK pet_id", "title", "reminder_date", "category", "status"]),
        "daily_activities": (390, 390, ["PK activity_id", "FK pet_id", "activity_type", "value", "activity_date"]),
        "ai_chats": (710, 390, ["PK chat_id", "FK user_id", "message", "response", "created_at"]),
        "subscriptions": (70, 390, ["PK subscription_id", "FK user_id", "plan_name", "payment_status", "started_at"]),
        "reports": (390, 665, ["PK report_id", "FK admin_id", "report_type", "created_at"]),
    }
    boxes = {}
    for name, (x, y, cols) in tables.items():
        w, h = 250, 185
        boxes[name] = (x, y, x + w, y + h)
        draw.rectangle((x, y, x + w, y + h), fill="#ffffff", outline="#27364a", width=2)
        draw.rectangle((x, y, x + w, y + 38), fill="#dcfce7", outline="#27364a", width=2)
        draw.text((x + 12, y + 9), name, fill="#172033", font=F_HEAD)
        for i, col in enumerate(cols):
            draw.text((x + 12, y + 50 + i * 20), col, fill="#172033", font=F_SMALL)
    links = [("users", "pets"), ("pets", "reminders"), ("pets", "daily_activities"), ("users", "ai_chats"), ("users", "subscriptions"), ("users", "reports")]
    for a, b in links:
        ax1, ay1, ax2, ay2 = boxes[a]
        bx1, by1, bx2, by2 = boxes[b]
        arrow(draw, (ax2, (ay1 + ay2) // 2), (bx1, (by1 + by2) // 2), width=2)
    img.save(out / "database-diagram.jpeg", quality=95)
    save_vpd(out / "database-diagram.vpd", "Database Diagram", "\n".join(tables.keys()))


def add_slide(prs, title, bullets):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg = slide.background.fill
    bg.solid()
    bg.fore_color.rgb = RGBColor(247, 245, 239)
    title_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.45), Inches(12), Inches(0.7))
    p = title_box.text_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(34)
    p.font.bold = True
    p.font.color.rgb = RGBColor(23, 32, 51)
    body = slide.shapes.add_textbox(Inches(0.9), Inches(1.5), Inches(11), Inches(4.8))
    tf = body.text_frame
    tf.clear()
    for i, bullet in enumerate(bullets):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.text = bullet
        para.font.size = Pt(22)
        para.space_after = Pt(12)
        para.level = 0
    return slide


def presentation():
    PRESENTATION.mkdir(exist_ok=True)
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = RGBColor(255, 241, 184)
    box = slide.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(11.3), Inches(1.1))
    p = box.text_frame.paragraphs[0]
    p.text = "Pet Care Assistant"
    p.font.size = Pt(48)
    p.font.bold = True
    p.alignment = PP_ALIGN.CENTER
    subtitle = slide.shapes.add_textbox(Inches(1.5), Inches(3.0), Inches(10.3), Inches(1.0))
    sp = subtitle.text_frame.paragraphs[0]
    sp.text = "Evcil hayvan bakım, hatırlatıcı, AI öneri ve premium yönetim sistemi"
    sp.font.size = Pt(24)
    sp.alignment = PP_ALIGN.CENTER
    add_slide(prs, "Problem ve Amaç", [
        "Pet sahipleri bakım, aşı, ilaç ve aktivite bilgilerini farklı yerlerde takip ediyor.",
        "Sistem tüm bakım süreçlerini tek panelde birleştirir.",
        "Admin, kullanıcı ve premium durumlarını raporlarla izler.",
    ])
    add_slide(prs, "Temel Aktörler", [
        "Pet Owner: kayıt olur, pet ve hatırlatıcı yönetir, AI ile sohbet eder.",
        "Admin: kullanıcıları, premium durumlarını ve raporları yönetir.",
        "Sistem servisleri: doğrulama, ödeme işleme ve AI öneri üretimi sağlar.",
    ])
    add_slide(prs, "Use Case Kapsamı", [
        "Register / Login, Add Pet, View Pets, View Reminders ve Track Daily Activities.",
        "Chat with AI akışı istek doğrulama ve veteriner önerisini kapsar.",
        "Activate Premium, ödeme başarılıysa premium açar; hatada kullanıcıya bilgi verir.",
    ])
    add_slide(prs, "Teknik Tasarım", [
        "Bağımlılıksız HTML, CSS ve JavaScript ile çalışan prototip.",
        "LocalStorage üzerinde örnek veri saklama ve dashboard güncelleme.",
        "Dokümanlardaki sınıflar ve veritabanı tabloları kod ekranlarıyla uyumludur.",
    ])
    add_slide(prs, "Sonuç", [
        "Teslim paketinde proje kodları, use case dokümantasyonu ve tüm diyagram çıktıları bulunur.",
        "Her diyagram için JPEG görseli ve VPD kaynak dosyası eklenmiştir.",
        "Prototip tarayıcıda src/index.html açılarak çalıştırılabilir.",
    ])
    output = PRESENTATION / "Zumra_Cicek_Pet_Care_Assistant.pptx"
    prs.save(output)
    normalize_zip(output)


def normalize_zip(path):
    """Keep generated Office files stable across repeated asset generation."""
    temp = path.with_suffix(".tmp")
    with zipfile.ZipFile(path, "r") as source, zipfile.ZipFile(temp, "w", zipfile.ZIP_DEFLATED) as target:
        for item in source.infolist():
            data = source.read(item.filename)
            normalized = zipfile.ZipInfo(item.filename, ZIP_TIMESTAMP)
            normalized.compress_type = zipfile.ZIP_DEFLATED
            normalized.external_attr = item.external_attr
            target.writestr(normalized, data)
    temp.replace(path)


def main():
    for directory in ["use-case", "class", "activity", "sequence", "database"]:
        (DIAGRAMS / directory).mkdir(parents=True, exist_ok=True)
    use_case()
    class_diagram()
    activity_diagram()
    sequence_diagram()
    database_diagram()
    presentation()


if __name__ == "__main__":
    main()
