import { useState } from 'react'

const inputCls = 'w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500'

export default function IntakeForm({ onHasReports, onNoReports }) {
  const [form, setForm] = useState({ name: '', age: '', sex: '1' })

  function handleChoice(hasReports) {
    if (!form.age) return
    const base = { name: form.name, age: Number(form.age), sex: Number(form.sex) }
    hasReports ? onHasReports(base) : onNoReports(base)
  }

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 sm:p-8">
      <h1 className="text-lg font-semibold text-gray-800 mb-1">Let's get started</h1>
      <p className="text-gray-400 text-sm mb-6">A few quick questions before we begin.</p>

      <div className="space-y-4 mb-8">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Name <span className="text-gray-400 font-normal">(optional)</span></label>
          <input type="text" value={form.name} onChange={e => setForm(f => ({ ...f, name: e.target.value }))}
            placeholder="e.g. Alex" className={inputCls} />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Age <span className="text-red-400">*</span></label>
            <input type="number" min={1} max={120} value={form.age}
              onChange={e => setForm(f => ({ ...f, age: e.target.value }))}
              className={inputCls} required />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Sex</label>
            <select value={form.sex} onChange={e => setForm(f => ({ ...f, sex: e.target.value }))} className={inputCls}>
              <option value="1">Male</option>
              <option value="0">Female</option>
            </select>
          </div>
        </div>
      </div>

      <p className="text-sm font-medium text-gray-700 mb-3">
        Do you have recent medical reports?
        <span className="ml-1 text-xs text-gray-400 font-normal">(ECG, blood test, stress test)</span>
      </p>

      <div className="grid grid-cols-2 gap-3">
        <button onClick={() => handleChoice(true)} disabled={!form.age}
          className="py-3 rounded-lg border-2 border-blue-500 text-blue-600 font-semibold text-sm hover:bg-blue-50 disabled:opacity-40 transition-colors">
          Yes, I have reports
        </button>
        <button onClick={() => handleChoice(false)} disabled={!form.age}
          className="py-3 rounded-lg border-2 border-gray-300 text-gray-600 font-semibold text-sm hover:bg-gray-50 disabled:opacity-40 transition-colors">
          No, I don't
        </button>
      </div>
      {!form.age && <p className="text-xs text-red-400 mt-2">Please enter your age first.</p>}
    </div>
  )
}
