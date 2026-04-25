const storageKey = "pet-care-assistant-state";

const defaultState = {
  currentUser: {
    name: "Zümra Çiçek",
    email: "zumra@example.com",
    premium: false,
  },
  users: [
    { name: "Zümra Çiçek", email: "zumra@example.com", role: "Pet Owner", premium: false },
    { name: "Admin Kullanıcı", email: "admin@petcare.local", role: "Admin", premium: true },
  ],
  pets: [
    {
      id: "pet-1",
      name: "Mia",
      type: "Kedi",
      breed: "Tekir",
      age: 3,
      weight: 4.2,
      note: "Aşı takibi düzenli yapılmalı.",
    },
    {
      id: "pet-2",
      name: "Max",
      type: "Köpek",
      breed: "Golden Retriever",
      age: 5,
      weight: 28,
      note: "Günlük yürüyüş hedefi 45 dakika.",
    },
  ],
  reminders: [
    {
      id: "rem-1",
      petId: "pet-1",
      title: "Karma aşı",
      date: "2026-05-10",
      type: "Veteriner",
      status: "Planlandı",
    },
    {
      id: "rem-2",
      petId: "pet-2",
      title: "Mama siparişi",
      date: "2026-04-30",
      type: "Bakım",
      status: "Planlandı",
    },
  ],
  activities: [
    { id: "act-1", petId: "pet-2", activity: "Yürüyüş", duration: 40, date: "2026-04-25" },
    { id: "act-2", petId: "pet-1", activity: "Oyun", duration: 20, date: "2026-04-25" },
  ],
  chatMessages: [
    {
      sender: "assistant",
      text: "Merhaba! Evcil dostunuz için beslenme, bakım veya veteriner önerisi isteyebilirsiniz.",
    },
  ],
  payments: [],
};

let state = loadState();
let editingPetId = null;
let editingReminderId = null;

const elements = {
  petList: document.getElementById("pet-list"),
  reminderList: document.getElementById("reminder-list"),
  activityList: document.getElementById("activity-list"),
  chatMessages: document.getElementById("chat-messages"),
  premiumBadge: document.getElementById("premium-badge"),
  userName: document.getElementById("user-name"),
  userEmail: document.getElementById("user-email"),
  adminUsers: document.getElementById("admin-users"),
  reports: document.getElementById("reports"),
};

document.getElementById("auth-form").addEventListener("submit", handleAuth);
document.getElementById("pet-form").addEventListener("submit", handlePetSubmit);
document.getElementById("reminder-form").addEventListener("submit", handleReminderSubmit);
document.getElementById("activity-form").addEventListener("submit", handleActivitySubmit);
document.getElementById("chat-form").addEventListener("submit", handleChatSubmit);
document.getElementById("premium-button").addEventListener("click", handlePremiumActivation);
document.getElementById("reset-button").addEventListener("click", resetDemoData);
document.getElementById("reminder-pet").addEventListener("change", syncPetDependentViews);
document.getElementById("activity-pet").addEventListener("change", syncPetDependentViews);

render();

function loadState() {
  const raw = localStorage.getItem(storageKey);
  if (!raw) {
    return structuredClone(defaultState);
  }

  try {
    return { ...structuredClone(defaultState), ...JSON.parse(raw) };
  } catch {
    return structuredClone(defaultState);
  }
}

function saveState() {
  localStorage.setItem(storageKey, JSON.stringify(state));
}

function render() {
  elements.userName.textContent = state.currentUser.name;
  elements.userEmail.textContent = state.currentUser.email;
  elements.premiumBadge.textContent = state.currentUser.premium ? "Premium Aktif" : "Standart Üyelik";
  elements.premiumBadge.className = state.currentUser.premium ? "badge success" : "badge";

  renderPetOptions();
  renderPets();
  renderReminders();
  renderActivities();
  renderChat();
  renderAdmin();
  saveState();
}

function renderPetOptions() {
  const selects = [document.getElementById("reminder-pet"), document.getElementById("activity-pet")];
  selects.forEach((select) => {
    const current = select.value;
    select.innerHTML = state.pets
      .map((pet) => `<option value="${pet.id}">${escapeHtml(pet.name)} (${escapeHtml(pet.type)})</option>`)
      .join("");
    if (state.pets.some((pet) => pet.id === current)) {
      select.value = current;
    }
  });
}

function renderPets() {
  elements.petList.innerHTML = state.pets
    .map(
      (pet) => `
      <article class="item-card">
        <div>
          <h3>${escapeHtml(pet.name)} <span>${escapeHtml(pet.type)}</span></h3>
          <p>${escapeHtml(pet.breed)} • ${pet.age} yaş • ${pet.weight} kg</p>
          <small>${escapeHtml(pet.note)}</small>
        </div>
        <div class="actions">
          <button type="button" data-edit-pet="${pet.id}">Düzenle</button>
          <button type="button" class="danger" data-delete-pet="${pet.id}">Sil</button>
        </div>
      </article>
    `,
    )
    .join("");

  elements.petList.querySelectorAll("[data-edit-pet]").forEach((button) => {
    button.addEventListener("click", () => startPetEdit(button.dataset.editPet));
  });
  elements.petList.querySelectorAll("[data-delete-pet]").forEach((button) => {
    button.addEventListener("click", () => deletePet(button.dataset.deletePet));
  });
}

function renderReminders() {
  elements.reminderList.innerHTML = state.reminders
    .slice()
    .sort((a, b) => a.date.localeCompare(b.date))
    .map((reminder) => {
      const pet = state.pets.find((item) => item.id === reminder.petId);
      return `
        <article class="item-card">
          <div>
            <h3>${escapeHtml(reminder.title)} <span>${escapeHtml(reminder.status)}</span></h3>
            <p>${escapeHtml(pet?.name || "Silinmiş pet")} • ${formatDate(reminder.date)} • ${escapeHtml(reminder.type)}</p>
          </div>
          <div class="actions">
            <button type="button" data-edit-reminder="${reminder.id}">Düzenle</button>
            <button type="button" class="danger" data-delete-reminder="${reminder.id}">Sil</button>
          </div>
        </article>
      `;
    })
    .join("");

  elements.reminderList.querySelectorAll("[data-edit-reminder]").forEach((button) => {
    button.addEventListener("click", () => startReminderEdit(button.dataset.editReminder));
  });
  elements.reminderList.querySelectorAll("[data-delete-reminder]").forEach((button) => {
    button.addEventListener("click", () => deleteReminder(button.dataset.deleteReminder));
  });
}

function renderActivities() {
  elements.activityList.innerHTML = state.activities
    .slice()
    .sort((a, b) => b.date.localeCompare(a.date))
    .map((activity) => {
      const pet = state.pets.find((item) => item.id === activity.petId);
      return `
        <article class="item-card compact">
          <strong>${escapeHtml(activity.activity)}</strong>
          <span>${escapeHtml(pet?.name || "Silinmiş pet")} • ${activity.duration} dk • ${formatDate(activity.date)}</span>
        </article>
      `;
    })
    .join("");
}

function renderChat() {
  elements.chatMessages.innerHTML = state.chatMessages
    .map((message) => `<p class="${message.sender}">${escapeHtml(message.text)}</p>`)
    .join("");
  elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;
}

function renderAdmin() {
  elements.adminUsers.innerHTML = state.users
    .map(
      (user) => `
      <li>
        <span>${escapeHtml(user.name)} (${escapeHtml(user.role)})</span>
        <strong>${user.premium ? "Premium" : "Standart"}</strong>
      </li>
    `,
    )
    .join("");

  const premiumCount = state.users.filter((user) => user.premium).length;
  elements.reports.innerHTML = `
    <li>Toplam kullanıcı: <strong>${state.users.length}</strong></li>
    <li>Kayıtlı pet: <strong>${state.pets.length}</strong></li>
    <li>Aktif hatırlatıcı: <strong>${state.reminders.length}</strong></li>
    <li>Premium kullanıcı: <strong>${premiumCount}</strong></li>
  `;
}

function handleAuth(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const name = form.name.value.trim();
  const email = form.email.value.trim().toLowerCase();
  if (!name || !email.includes("@")) {
    showToast("Kullanıcı doğrulama başarısız. Lütfen geçerli bilgi girin.", true);
    return;
  }

  const existingUser = state.users.find((user) => user.email === email);
  state.currentUser = existingUser || { name, email, role: "Pet Owner", premium: false };
  if (!existingUser) {
    state.users.push(state.currentUser);
  }
  showToast("Kullanıcı doğrulandı ve oturum açıldı.");
  render();
}

function handlePetSubmit(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const pet = {
    id: editingPetId || createId("pet"),
    name: form.name.value.trim(),
    type: form.type.value,
    breed: form.breed.value.trim(),
    age: Number(form.age.value),
    weight: Number(form.weight.value),
    note: form.note.value.trim(),
  };

  if (editingPetId) {
    state.pets = state.pets.map((item) => (item.id === editingPetId ? pet : item));
    editingPetId = null;
    form.querySelector("button[type='submit']").textContent = "Pet Kaydet";
    showToast("Pet bilgisi güncellendi.");
  } else {
    state.pets.push(pet);
    showToast("Yeni pet eklendi.");
  }

  form.reset();
  render();
}

function startPetEdit(petId) {
  const pet = state.pets.find((item) => item.id === petId);
  if (!pet) return;
  const form = document.getElementById("pet-form");
  form.name.value = pet.name;
  form.type.value = pet.type;
  form.breed.value = pet.breed;
  form.age.value = pet.age;
  form.weight.value = pet.weight;
  form.note.value = pet.note;
  editingPetId = petId;
  form.querySelector("button[type='submit']").textContent = "Pet Güncelle";
}

function deletePet(petId) {
  state.pets = state.pets.filter((pet) => pet.id !== petId);
  state.reminders = state.reminders.filter((reminder) => reminder.petId !== petId);
  state.activities = state.activities.filter((activity) => activity.petId !== petId);
  showToast("Pet ve ilişkili kayıtlar silindi.");
  render();
}

function handleReminderSubmit(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const reminder = {
    id: editingReminderId || createId("rem"),
    petId: form.petId.value,
    title: form.title.value.trim(),
    date: form.date.value,
    type: form.type.value,
    status: form.status.value,
  };

  if (!reminder.petId) {
    showToast("Hatırlatıcı için önce pet ekleyin.", true);
    return;
  }

  if (editingReminderId) {
    state.reminders = state.reminders.map((item) => (item.id === editingReminderId ? reminder : item));
    editingReminderId = null;
    form.querySelector("button[type='submit']").textContent = "Hatırlatıcı Kaydet";
    showToast("Hatırlatıcı güncellendi.");
  } else {
    state.reminders.push(reminder);
    showToast("Yeni hatırlatıcı eklendi.");
  }

  form.reset();
  render();
}

function startReminderEdit(reminderId) {
  const reminder = state.reminders.find((item) => item.id === reminderId);
  if (!reminder) return;
  const form = document.getElementById("reminder-form");
  form.petId.value = reminder.petId;
  form.title.value = reminder.title;
  form.date.value = reminder.date;
  form.type.value = reminder.type;
  form.status.value = reminder.status;
  editingReminderId = reminderId;
  form.querySelector("button[type='submit']").textContent = "Hatırlatıcı Güncelle";
}

function deleteReminder(reminderId) {
  state.reminders = state.reminders.filter((reminder) => reminder.id !== reminderId);
  showToast("Hatırlatıcı silindi.");
  render();
}

function handleActivitySubmit(event) {
  event.preventDefault();
  const form = event.currentTarget;
  if (!form.petId.value) {
    showToast("Aktivite için önce pet ekleyin.", true);
    return;
  }

  state.activities.push({
    id: createId("act"),
    petId: form.petId.value,
    activity: form.activity.value.trim(),
    duration: Number(form.duration.value),
    date: form.date.value,
  });
  form.reset();
  showToast("Günlük aktivite kaydedildi.");
  render();
}

function handleChatSubmit(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const question = form.message.value.trim();
  if (!question) return;

  state.chatMessages.push({ sender: "owner", text: question });
  state.chatMessages.push({ sender: "assistant", text: buildAssistantReply(question) });
  form.reset();
  render();
}

function buildAssistantReply(question) {
  const normalized = question.toLocaleLowerCase("tr-TR");
  if (normalized.includes("veteriner") || normalized.includes("hasta")) {
    return "Belirtiler devam ediyorsa en yakın veteriner kliniğinden randevu almanızı öneririm. Acil durumda beklemeyin.";
  }
  if (normalized.includes("mama") || normalized.includes("beslen")) {
    return "Yaş, kilo ve tür bilgisine göre porsiyon planı yapın; ani mama değişimlerini kademeli uygulayın.";
  }
  if (normalized.includes("aşı")) {
    return "Aşı takvimini hatırlatıcı olarak ekleyebilirsiniz. Sistem yaklaşan tarihi ana panelde listeler.";
  }
  return "Genel bakım için düzenli aktivite, temiz su, dengeli beslenme ve dönemsel veteriner kontrolü önerilir.";
}

function handlePremiumActivation() {
  const accepted = document.getElementById("payment-confirm").checked;
  const payment = {
    id: createId("pay"),
    userEmail: state.currentUser.email,
    date: new Date().toISOString(),
    status: accepted ? "Başarılı" : "Hata",
  };
  state.payments.push(payment);

  if (!accepted) {
    showToast("Ödeme hatası: kart onayı alınamadı.", true);
    render();
    return;
  }

  state.currentUser.premium = true;
  state.users = state.users.map((user) =>
    user.email === state.currentUser.email ? { ...user, premium: true } : user,
  );
  showToast("Premium üyelik aktif edildi.");
  render();
}

function resetDemoData() {
  state = structuredClone(defaultState);
  editingPetId = null;
  editingReminderId = null;
  localStorage.removeItem(storageKey);
  showToast("Demo verileri sıfırlandı.");
  render();
}

function syncPetDependentViews() {
  saveState();
}

function createId(prefix) {
  return `${prefix}-${crypto.randomUUID()}`;
}

function formatDate(value) {
  if (!value) return "-";
  return new Intl.DateTimeFormat("tr-TR", { day: "2-digit", month: "long", year: "numeric" }).format(
    new Date(`${value}T00:00:00`),
  );
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function showToast(message, isError = false) {
  const toast = document.getElementById("toast");
  toast.textContent = message;
  toast.className = isError ? "toast error visible" : "toast visible";
  window.clearTimeout(showToast.timeout);
  showToast.timeout = window.setTimeout(() => {
    toast.className = "toast";
  }, 2600);
}
