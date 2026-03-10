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
  if (res.status === 204) return null
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

export async function askJobQuestion(jobId, question) {
  return fetchApi(`/jobs/${jobId}/ask`, {
    method: 'POST',
    body: JSON.stringify({ question }),
  })
}

export async function getLocations() {
  return fetchApi('/locations')
}

export async function postLocation(data) {
  return fetchApi('/locations', { method: 'POST', body: JSON.stringify(data) })
}

export async function putLocation(id, data) {
  return fetchApi(`/locations/${id}`, { method: 'PUT', body: JSON.stringify(data) })
}

export async function deleteLocation(id) {
  return fetchApi(`/locations/${id}`, { method: 'DELETE' })
}

export async function getVehicles() {
  return fetchApi('/vehicles')
}

export async function postVehicle(data) {
  return fetchApi('/vehicles', { method: 'POST', body: JSON.stringify(data) })
}

export async function putVehicle(id, data) {
  return fetchApi(`/vehicles/${id}`, { method: 'PUT', body: JSON.stringify(data) })
}

export async function deleteVehicle(id) {
  return fetchApi(`/vehicles/${id}`, { method: 'DELETE' })
}

export async function getDeliveries() {
  return fetchApi('/deliveries')
}

export async function postDelivery(data) {
  return fetchApi('/deliveries', { method: 'POST', body: JSON.stringify(data) })
}

export async function getWeeklyReport(fromDate, toDate) {
  const params = new URLSearchParams()
  if (fromDate) params.set('from', fromDate)
  if (toDate) params.set('to', toDate)
  return fetchApi(`/reports/weekly?${params}`)
}
