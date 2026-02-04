const chatbotQuestions = [
  {
    q: "What kind of photography do you specialize in?",
    a: "We specialize in weddings, birthdays, portraits, pre-weddings, corporate events, and lifestyle shoots.",
    followups: [
      { label: "📷 View portfolio", a: 'See our <a href="/projects/" class="text-green-300 underline">Projects page</a>.' }
    ]
  },
  {
    q: "How can I book a photoshoot?",
    a: 'You can <a href="/contact/" class="text-green-300 underline">book via our Contact page</a>, <a href="https://www.instagram.com/megapixel_creations/" target="_blank" class="text-green-300 underline">Instagram DM</a>, or call us directly at <a href="tel:+919956963676" class="text-green-300 underline">+91 9956963676</a>.',
    followups: [
      { label: "📅 Check availability", a: 'Please <a href="/contact/" class="text-green-300 underline">contact us</a> to check available dates.' },
      { label: "📞 Call us", a: 'Call us at <a href="tel:+919956963676" class="text-green-300 underline">+91 9956963676</a>.' },
      { label: "📷 View portfolio", a: 'See our <a href="/projects/" class="text-green-300 underline">Projects page</a>.' }
    ]
  },
  {
    q: "Where can I check your work on social media?",
    a: 'You can see our work on <a href="https://www.instagram.com/megapixel_creations/" target="_blank" class="text-blue-600 underline">Instagram</a>, <a href="https://www.youtube.com/@Megapixelcreation" target="_blank" class="text-blue-600 underline">YouTube</a>, and <a href="/projects/" class="text-blue-600 underline">our Projects page</a>.'
  },
  {
    q: "Do you cover weddings & events?",
    a: "Yes, we cover weddings, engagements, birthdays, concerts, corporate and private events.",
    followups: [
      { label: "📅 Book an event", a: 'Book via our <a href="/contact/" class="text-green-300 underline">Contact page</a>.' }
    ]
  },
  {
    q: "How can I contact your team?",
    a: 'You can reach us via <a href="/contact/" class="text-green-300 underline">Contact page</a>, <a href="mailto:email@example.com" class="text-green-300 underline">email</a>, or <a href="https://www.instagram.com/megapixel_creations/" target="_blank" class="text-green-300 underline">Instagram</a>.',
    followups: [
      { label: "📞 Call us", a: 'Call us at <a href="tel:+919956963676" class="text-green-300 underline">+91 9956963676</a>.' }
    ]
  },
  {
    q: "What’s your phone number?",
    a: 'Call us at <a href="tel:+919956963676" class="text-green-300 underline">+91 9956963676</a>.'
  }
];

function createChatbot() {
  // Create chatbot container
  const bot = document.createElement('div');
  bot.id = 'megapixel-chatbot';
  bot.className = `fixed bottom-8 right-8 z-50 w-80 max-w-[90vw] bg-white border border-blue-200 rounded-2xl shadow-2xl flex flex-col animate-fade-in`;
  bot.style.display = 'none';

  // Header with camera.png and bot name
  bot.innerHTML = `
    <div class="flex items-center gap-3 px-4 py-3 border-b border-blue-100 bg-blue-50 rounded-t-2xl">
      <img src="/static/camera.png" class="w-8 h-8 rounded-full border border-blue-400 bg-white shadow" alt="Chatbot">
      <span class="font-semibold text-base text-blue-800">MegaPixel Assistant</span>
      <button id="closeChatbot" class="ml-auto text-blue-400 hover:text-red-500 text-xl">✕</button>
    </div>
    <div id="chatbotMessages" class="flex-1 px-4 py-3 space-y-3 overflow-y-auto text-sm bg-white text-blue-900" style="max-height: 300px;"></div>
    <div class="px-4 py-3 border-t border-blue-100 bg-blue-50 rounded-b-2xl">
      <div class="flex flex-wrap gap-2" id="chatbotQuestions"></div>
    </div>
  `;

  document.body.appendChild(bot);

  // Open/close logic
  document.getElementById('openChatbotBtn').onclick = () => {
    bot.style.display = 'flex';
    // Show intro message only once per open
    const msgWrap = document.getElementById('chatbotMessages');
    if (!msgWrap.dataset.intro) {
      msgWrap.innerHTML = `<div class='mb-2'><div class='font-semibold text-blue-800'>MegaPixel Assistant</div><div class='ml-3 text-black'>Hi! I’m the MegaPixel Assistant. I can help with bookings, photography services, pricing, and contact details. What would you like to know?</div></div>`;
      msgWrap.dataset.intro = '1';
    }
  };
  bot.querySelector('#closeChatbot').onclick = () => {
    bot.style.display = 'none';
  };

  // Render questions (show only first 4, but allow all to be asked once)
  const qWrap = bot.querySelector('#chatbotQuestions');
  let shownQuestions = chatbotQuestions.slice(); // allow all questions, not just 4
  function renderQuestions(questions) {
    qWrap.innerHTML = '';
    questions.forEach((item, idx) => {
      const btn = document.createElement('button');
      btn.className = 'bg-blue-100 hover:bg-blue-200 text-blue-800 px-3 py-1 rounded-xl transition border border-blue-200 mb-2';
      btn.innerHTML = item.q;
      btn.addEventListener('click', function() {
        addChatbotMessage(item.q, item.a);
        // Hide this question (never show again until reopen)
        shownQuestions = shownQuestions.filter((q, i) => q.q !== item.q);
        renderQuestions(shownQuestions);
        // Show followups if any
        if (item.followups && item.followups.length > 0) {
          renderFollowups(item.followups);
        }
      });
      qWrap.appendChild(btn);
    });
    if (questions.length === 0) {
      qWrap.innerHTML = '<div class="text-blue-700 mt-2 text-xs">You have asked all questions! You can close the chat or reopen to start again.</div>';
    }
  }
  function renderFollowups(followups) {
    const followupWrap = document.createElement('div');
    followupWrap.className = 'flex flex-wrap gap-2 mt-2';
    followups.forEach(fu => {
      const fbtn = document.createElement('button');
      fbtn.className = 'bg-blue-200 hover:bg-blue-300 text-blue-800 px-2 py-1 rounded-xl text-xs border border-blue-200';
      fbtn.innerHTML = fu.label;
      fbtn.onclick = () => {
        addChatbotMessage(fu.label, fu.a);
        // After followup, re-render remaining main questions if any
        if (shownQuestions.length > 0) {
          renderQuestions(shownQuestions);
        } else {
          qWrap.innerHTML = '<div class="text-blue-700 mt-2 text-xs">You can close the chat or reopen to start again!</div>';
        }
      };
      followupWrap.appendChild(fbtn);
    });
    qWrap.appendChild(followupWrap);
  }
  renderQuestions(shownQuestions);
}

function addChatbotMessage(q, a) {
  const msgWrap = document.getElementById('chatbotMessages');
  msgWrap.innerHTML += `
    <div class="mb-4">
      <div class="font-semibold text-blue-700 flex items-center gap-2"><img src="/static/camera.png" class="w-5 h-5 rounded-full border border-blue-200"> You asked: <span class="font-normal">${q}</span></div>
      <div class="ml-7 mt-2 p-3 bg-blue-50 border border-blue-100 rounded-xl text-blue-900">${a}</div>
    </div>
  `;
  msgWrap.scrollTop = msgWrap.scrollHeight;
}

// Floating button
function createChatbotButton() {
  const btn = document.createElement('button');
  btn.id = 'openChatbotBtn';
  btn.className = 'fixed bottom-8 right-8 z-50 bg-gradient-to-br from-blue-500 to-blue-700 text-white shadow-xl rounded-full w-16 h-16 flex flex-col items-center justify-center text-xs hover:scale-110 transition border-4 border-white';
  btn.innerHTML = '<img src="/static/camera.png" class="w-8 h-8 mb-1"> <span class="block text-xs font-semibold text-blue-100">Ask me</span>';
  document.body.appendChild(btn);
}

window.addEventListener('DOMContentLoaded', () => {
  createChatbotButton();
  createChatbot();
});
