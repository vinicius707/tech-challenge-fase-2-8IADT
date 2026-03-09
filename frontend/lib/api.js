const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

async function fetchApi(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  })
  if (!res.ok) {
    const err = new Error(res.statusText || 'API error')
    err.status = res.status
    try {
      err.body = await res.json()
    } catch {
      err.body = await res.text()
    }
    throw err
  }
  return res.json()
}

export async function postOptimize(params) {
  return fetchApi('/optimize', {
    method: 'POST',
    body: JSON.stringify(params),
  })
}

export async function getJobs() {
  return fetchApi('/jobs')
}

export async function getJob(jobId) {
  return fetchApi(`/jobs/${jobId}`)
}

export async function getRoutes(jobId) {
  return fetchApi(`/routes/${jobId}`)
}

export async function postInstructions(jobId) {
  return fetchApi(`/instructions/${jobId}`, { method: 'POST' })
}
