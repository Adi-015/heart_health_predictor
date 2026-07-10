import { useState } from 'react'
import PatientForm from './PatientForm'
import { predict } from './api'

export default function App() {
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function handleSubmit(formData) {
    setLoading(true)
    setError(null)
    try {
      const data = await predict(formData)
      setResult(data)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      <main className="max-w-2xl mx-auto px-4 py-10">
        <h1 className="text-2xl font-bold mb-2">Heart Health Predictor</h1>
        <p className="text-gray-500 text-sm mb-8">
          Enter patient data to estimate cardiovascular disease risk.
        </p>

        <PatientForm onSubmit={handleSubmit} loading={loading} />

        {error && (
          <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-md text-red-700 text-sm">
            {error}
          </div>
        )}

        {/* Results rendered in Commit 4 */}
        {result && (
          <pre className="mt-6 p-4 bg-gray-100 rounded text-xs overflow-auto">
            {JSON.stringify(result, null, 2)}
          </pre>
        )}
      </main>
    </div>
  )
}
