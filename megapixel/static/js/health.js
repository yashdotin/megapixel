const csrfToken = document.cookie.split('; ').find((row) => row.startsWith('csrftoken='))?.split('=')[1] || '';

async function sendJSON(url, body) {
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
    body: JSON.stringify(body),
  });
  return response.json();
}

function card(title, value) {
  return `<div class="metric-card"><p class="text-xs opacity-80">${title}</p><p class="text-2xl font-bold">${value}</p></div>`;
}

function renderDashboard(data) {
  const m = data.metrics;
  document.getElementById('metric-cards').innerHTML = [
    card('Health Score', `${m.overall_health}%`),
    card('Heart Risk', `${m.heart_risk}%`),
    card('Diabetes Risk', `${m.diabetes_risk}%`),
    card('Lifestyle', `${m.lifestyle_score}/100`),
  ].join('');

  document.getElementById('timeline').innerHTML = `
    <p class="mt-2 text-sm">${data.timeline_dates.three_months}: Continue → <b>${data.timeline.three_months_continue}% risk</b></p>
    <p class="text-sm">${data.timeline_dates.one_year}: Improve → <b>${data.timeline.one_year_improve}% risk</b></p>
  `;

  document.getElementById('explainability').innerHTML = `
    <p class="text-sm mt-2">Sleep impact: <b>${m.explainability.sleep}%</b></p>
    <p class="text-sm">Diet impact: <b>${m.explainability.diet}%</b></p>
    <p class="text-sm">Activity impact: <b>${m.explainability.activity}%</b></p>
  `;

  document.getElementById('alerts').innerHTML = (data.alerts || []).map((a) => `<li>${a.message}</li>`).join('') || '<li>No alerts right now.</li>';
}

async function refreshDashboard() {
  const data = await fetch('/health/api/dashboard/').then((r) => r.json());
  renderDashboard(data);
}

document.getElementById('onboarding-form')?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const form = new FormData(e.target);
  const payload = Object.fromEntries(form.entries());
  ['age','height_cm','weight_kg','sleep_hours','stress_level'].forEach((k)=> payload[k]= Number(payload[k] || 0));
  const response = await sendJSON('/health/api/onboarding/', payload);
  if (response.status === 'ok') refreshDashboard();
});

document.getElementById('daily-log-form')?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const form = new FormData(e.target);
  const payload = Object.fromEntries(form.entries());
  ['sleep_hours','water_liters','stress_level','steps'].forEach((k)=> payload[k]= Number(payload[k] || 0));
  const response = await sendJSON('/health/api/log/', payload);
  document.getElementById('xp-box').textContent = `+10 XP earned. Total XP: ${response.xp} | Streak: ${response.streak}`;
  if (response.silent_alert) document.getElementById('alerts').innerHTML = `<li>${response.silent_alert}</li>`;
  refreshDashboard();
});

document.getElementById('assistant-form')?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const message = new FormData(e.target).get('message');
  const response = await sendJSON('/health/api/assistant/', { message });
  document.getElementById('assistant-reply').textContent = response.reply;
});

refreshDashboard();
