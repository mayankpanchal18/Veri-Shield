const TOKEN_KEY = 'verishield_token_v2';

export const authStore = {
  get token() { return localStorage.getItem(TOKEN_KEY); },
  set token(value) { value ? localStorage.setItem(TOKEN_KEY, value) : localStorage.removeItem(TOKEN_KEY); },
};

function errorMessage(body, status) {
  if (typeof body === 'string') return body || `Request failed (${status})`;

  const detail = body?.detail ?? body?.error ?? body?.message;
  if (typeof detail === 'string') return detail;

  // FastAPI/Pydantic validation errors are returned as an array of objects.
  // Turn them into human-readable messages instead of showing "[object Object]".
  if (Array.isArray(detail)) {
    const messages = detail.map((item) => {
      if (typeof item === 'string') return item;
      if (item && typeof item === 'object') {
        const location = Array.isArray(item.loc)
          ? item.loc.filter((part) => part !== 'body').join('.')
          : '';
        const message = item.msg || item.message || 'Invalid value';
        return location ? `${location}: ${message}` : message;
      }
      return String(item);
    }).filter(Boolean);
    if (messages.length) return messages.join(' • ');
  }

  if (detail && typeof detail === 'object') {
    return detail.msg || detail.message || JSON.stringify(detail);
  }

  return `Request failed (${status})`;
}

async function request(path, options = {}) {
  const headers = new Headers(options.headers || {});
  if (authStore.token) headers.set('Authorization', `Bearer ${authStore.token}`);
  if (options.body && !(options.body instanceof FormData) && !headers.has('Content-Type')) headers.set('Content-Type', 'application/json');
  const res = await fetch(path, { ...options, headers });
  const isJson = (res.headers.get('content-type') || '').includes('application/json');
  const body = isJson ? await res.json() : await res.text();
  if (!res.ok) throw new Error(errorMessage(body, res.status));
  return body;
}

export const api = {
  login: (payload) => request('/api/auth/login', { method: 'POST', body: JSON.stringify(payload) }),
  register: (payload) => request('/api/auth/register', { method: 'POST', body: JSON.stringify(payload) }),
  me: () => request('/api/auth/me'),
  createScreening: (file) => {
    const form = new FormData();
    form.append('document', file);
    return request('/api/screenings', { method: 'POST', body: form });
  },
  screenings: () => request('/api/screenings'),
  screening: (id) => request(`/api/screenings/${id}`),
  reviewQueue: () => request('/api/reviews/queue'),
  decide: (id, payload) => request(`/api/reviews/${id}/decision`, { method: 'POST', body: JSON.stringify(payload) }),
  verify: (hash) => request(`/api/verify/${encodeURIComponent(hash)}`),
  evidenceUrl: (id) => `/api/screenings/${id}/evidence`,
};

export async function openEvidence(id) {
  const preview = window.open('', '_blank');
  const res = await fetch(api.evidenceUrl(id), { headers: { Authorization: `Bearer ${authStore.token}` } });
  if (!res.ok) {
    if (preview) preview.close();
    const data = await res.json().catch(() => ({}));
    throw new Error(data.detail || 'Could not open evidence');
  }
  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  if (preview) preview.location.href = url;
  else window.location.href = url;
  setTimeout(() => URL.revokeObjectURL(url), 60_000);
}
