const BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8001'

export async function predict(patient) {
  const res = await fetch(`${BASE}/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(patient),
  })

  if (!res.ok) {
    // 422 = validation error from backend — surface the detail
    const body = await res.json().catch(() => null)
    const msg = body?.detail?.[0]?.msg ?? `Request failed (${res.status})`
    throw new Error(msg)
  }

  return res.json()
}
