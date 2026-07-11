import { useState } from 'react'
import PatientForm from './PatientForm'
import ResultCard from './ResultCard'
import { predict } from './api'

function Disclaimer() {
  return (
    <div className="mb-8 px-4 py-3 bg-amber-50 border border-amber-200 rounded-md text-amber-800 text-xs leading-relaxed">
      <strong>Educational tool only — not medical advice.</strong> This tool uses a machine learning
      model trained on a small research dataset. Results should not be used to diagnose, treat,
      or make clinical decisions. Always consult a qualified healthcare professional.
    </div>
  )
}

function EmptyState() {
  return (
    <div className="mt-8 rounded-lg border-2 border-dashed border-gray-200 p-8 text-center text-gray-400 text-sm">
      <div className="text-3xl mb-2">🫀</div>
      Fill in the patient data above and click <strong className="text-gray-500">Predict Risk</strong> to see results.
    </div>
  )
}

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
      <header className="bg-white border-b border-gray-200 px-4 py-4">
        <div className="max-w-2xl mx-auto flex items-center gap-2">
          <span className="text-xl">🫀</span>
          <span className="font-semibold text-gray-800">Heart Health Predictor</span>
        </div>
      </header>

      <main className="max-w-2xl mx-auto px-4 py-8 sm:py-10">
        <Disclaimer />

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 sm:p-8">
          <h1 className="text-lg font-semibold text-gray-800 mb-1">Patient Assessment</h1>
          <p className="text-gray-400 text-sm mb-6">
            Enter clinical measurements to estimate cardiovascular disease risk.
          </p>
          <PatientForm onSubmit={handleSubmit} loading={loading} />
        </div>

        {error && (
          <div className="mt-5 p-4 bg-red-50 border border-red-200 rounded-md text-red-700 text-sm">
            <strong>Error:</strong> {error}
          </div>
        )}

        {result ? <ResultCard result={result} /> : !error && <EmptyState />}
      </main>
    </div>
  )
}
