import { postOptimize, getJob, getJobs, getRoutes, postInstructions } from '../../lib/api'

const originalFetch = global.fetch

beforeEach(() => {
  global.fetch = jest.fn()
})

afterEach(() => {
  global.fetch = originalFetch
})

describe('api', () => {
  it('postOptimize sends POST to /optimize', async () => {
    global.fetch.mockResolvedValueOnce({ ok: true, json: () => ({ job_id: 'x', status: 'queued' }) })
    await postOptimize({ instance: 'test.csv', num_vehicles: 2 })
    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringContaining('/optimize'),
      expect.objectContaining({ method: 'POST', body: expect.any(String) })
    )
  })

  it('getJob fetches /jobs/{id}', async () => {
    global.fetch.mockResolvedValueOnce({ ok: true, json: () => ({ status: 'finished' }) })
    await getJob('abc-123')
    expect(global.fetch).toHaveBeenCalledWith(expect.stringContaining('/jobs/abc-123'), expect.any(Object))
  })

  it('getJobs fetches /jobs', async () => {
    global.fetch.mockResolvedValueOnce({ ok: true, json: () => ({ jobs: {} }) })
    await getJobs()
    expect(global.fetch).toHaveBeenCalledWith(expect.stringContaining('/jobs'), expect.any(Object))
  })

  it('getRoutes fetches /routes/{id}', async () => {
    global.fetch.mockResolvedValueOnce({ ok: true, json: () => ({ status: 'finished' }) })
    await getRoutes('x')
    expect(global.fetch).toHaveBeenCalledWith(expect.stringContaining('/routes/x'), expect.any(Object))
  })

  it('postInstructions sends POST to /instructions/{id}', async () => {
    global.fetch.mockResolvedValueOnce({ ok: true, json: () => ({ instruction: '/path/instruction.txt' }) })
    await postInstructions('y')
    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringContaining('/instructions/y'),
      expect.objectContaining({ method: 'POST' })
    )
  })
})
