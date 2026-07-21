import { useState } from 'react'

const inputCls = 'w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500'

const DEFAULTS = {
  bp: '',
  chestPain: 'none',
  breathlessness: 'no',
  familyHistory: 'no',
  smoking: 'no',
}

export default function SimpleGuidanceForm({ base, onResult, onBack }) {
  const [form, setForm] = useState(DEFAULTS)
  const set = (k, v) => setForm(f => ({ ...f, [k]: v }))

  function handleSubmit(e) {
    e.preventDefault()
    onResult({ ...base, ...form })
  }

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 sm:p-8">
      <button onClick={onBack} className="text-sm text-gray-400 hover:text-gray-600 mb-4 flex items-center gap-1">
        ← Back
      </button>

      <h1 className="text-lg font-semibold text-gray-800 mb-1">General health check</h1>
      <p className="text-gray-400 text-sm mb-6">
        Answer what you know — no lab results needed.
      </p>

      <form onSubmit={handleSubmit} className="space-y-5">
        <div className="grid grid-cols-2 gap-4 p-3 bg-gray-50 rounded-lg text-sm text-gray-500">
          <span>Age: <strong className="text-gray-700">{base.age}</strong></span>
          <span>Sex: <strong className="text-gray-700">{base.sex === 1 ? 'Male' : 'Female'}</strong></span>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Resting blood pressure <span className="text-gray-400 font-normal">(mm Hg)</span>
          </label>
          <select value={form.bp} onChange={e => set('bp', e.target.value)} className={inputCls}>
            <option value="">I don't know</option>
            <option value="normal">Normal (&lt;120/80)</option>
            <option value="elevated">Elevated (120–139/80–89)</option>
            <option value="high">High (≥140/90)</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Chest pain or discomfort during physical activity?</label>
          <select value={form.chestPain} onChange={e => set('chestPain', e.target.value)} className={inputCls}>
            <option value="none">None</option>
            <option value="mild">Mild / occasional</option>
            <option value="severe">Frequent / severe</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Shortness of breath during normal exercise?</label>
          <select value={form.breathlessness} onChange={e => set('breathlessness', e.target.value)} className={inputCls}>
            <option value="no">No</option>
            <option value="yes">Yes</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Family history of heart disease?</label>
          <select value={form.familyHistory} onChange={e => set('familyHistory', e.target.value)} className={inputCls}>
            <option value="no">No / Not sure</option>
            <option value="yes">Yes</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Do you smoke?</label>
          <select value={form.smoking} onChange={e => set('smoking', e.target.value)} className={inputCls}>
            <option value="no">No</option>
            <option value="yes">Yes</option>
          </select>
        </div>

        <button type="submit"
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2.5 rounded-md transition-colors text-sm">
          Get guidance
        </button>
      </form>
    </div>
  )
}
