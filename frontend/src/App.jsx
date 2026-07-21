import { useState } from 'react'
import IntakeForm from './IntakeForm'
import PatientForm from './PatientForm'
import SimpleGuidanceForm from './SimpleGuidanceForm'
import GuidanceCard from './GuidanceCard'
import ResultCard from './ResultCard'
import { predict } from './api'

// step: 'intake' | 'clinical' | 'simple' | 'guidance' | 'result'

function Disclaimer() {
  return (
    <div className="mb-6 px-4 py-3 bg-amber-50 border border-amber-200 rounded-md text-amber-800 text-xs leading-relaxed">
      <strong>Educational tool only — not medical advice.</strong> Results should not be used to
      diagnose, treat, or make clinical decisions. Always consult a qualified healthcare professional.
    </div>
  )
}

export default function App() {
  const [step, setStep]       = useState('intake')
  const [base, setBase]       = useState(null)   // { name, age, sex } from intake
  const [result, setResult]   = useState(null)
  const [guidance, setGuidance] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError]     = useState(null)

  function reset() {
    setStep('intake'); setBase(null); setResult(null)
    setGuidance(null); setError(null)
  }

  async function handleClinicalSubmit(formData) {
    setLoading(true); setError(null)
    try {
      const data = await predict(formData)
      setResult(data)
      setStep('result')
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

        {step === 'intake' && (
          <IntakeForm
            onHasReports={b => { setBase(b); setStep('clinical') }}
            onNoReports={b  => { setBase(b); setStep('simple') }}
          />
        )}

        {step === 'clinical' && (
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 sm:p-8">
            <button onClick={() => setStep('intake')} className="text-sm text-gray-400 hover:text-gray-600 mb-4 flex items-center gap-1">
              ← Back
            </button>
            <h1 className="text-lg font-semibold text-gray-800 mb-1">Clinical assessment</h1>
            <p className="text-gray-400 text-sm mb-6">Enter your lab and diagnostic values.</p>
            <PatientForm
              prefill={{ age: base?.age, sex: base?.sex }}
              onSubmit={handleClinicalSubmit}
              loading={loading}
            />
            {error && (
              <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-md text-red-700 text-sm">
                <strong>Error:</strong> {error}
              </div>
            )}
          </div>
        )}

        {step === 'result' && result && (
          <div>
            <ResultCard result={result} />
            <button onClick={reset} className="mt-4 text-sm text-gray-400 hover:text-gray-600 flex items-center gap-1">
              ← Start over
            </button>
          </div>
        )}

        {step === 'simple' && (
          <SimpleGuidanceForm
            base={base}
            onResult={answers => { setGuidance(answers); setStep('guidance') }}
            onBack={() => setStep('intake')}
          />
        )}

        {step === 'guidance' && guidance && (
          <GuidanceCard answers={guidance} onBack={reset} />
        )}
      </main>
    </div>
  )
}
