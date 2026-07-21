import { useState } from 'react'

const DEFAULTS = {
  age: 50, sex: 1, cp: 0, trestbps: 120, chol: 200,
  fbs: 0, restecg: 0, thalach: 150, exang: 0,
  oldpeak: 1.0, slope: 1, ca: 0, thal: 2,
}

function Field({ label, hint, children }) {
  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-1">
        {label}
        {hint && <span className="ml-1 text-xs text-gray-400 font-normal">{hint}</span>}
      </label>
      {children}
    </div>
  )
}

const inputCls = 'w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500'

export default function PatientForm({ onSubmit, loading, prefill = {} }) {
  const [form, setForm] = useState({ ...DEFAULTS, ...prefill })

  const set = (k, v) => setForm(f => ({ ...f, [k]: v }))
  const num = (k, v) => set(k, v === '' ? '' : Number(v))

  return (
    <form
      onSubmit={e => { e.preventDefault(); onSubmit(form) }}
      className="space-y-6"
    >
      {/* Demographics */}
      <section>
        <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">Demographics</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <Field label="Age" hint="1–120">
            <input type="number" min={1} max={120} value={form.age}
              onChange={e => num('age', e.target.value)}
              className={inputCls} required />
          </Field>

          <Field label="Sex">
            <select value={form.sex} onChange={e => num('sex', e.target.value)} className={inputCls}>
              <option value={1}>Male</option>
              <option value={0}>Female</option>
            </select>
          </Field>
        </div>
      </section>

      {/* Symptoms */}
      <section>
        <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">Symptoms</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <Field label="Chest Pain Type">
            <select value={form.cp} onChange={e => num('cp', e.target.value)} className={inputCls}>
              <option value={0}>Typical Angina</option>
              <option value={1}>Atypical Angina</option>
              <option value={2}>Non-anginal Pain</option>
              <option value={3}>Asymptomatic</option>
            </select>
          </Field>

          <Field label="Exercise-induced Angina">
            <select value={form.exang} onChange={e => num('exang', e.target.value)} className={inputCls}>
              <option value={0}>No</option>
              <option value={1}>Yes</option>
            </select>
          </Field>
        </div>
      </section>

      {/* Vitals */}
      <section>
        <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">Vitals</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <Field label="Resting BP" hint="mm Hg">
            <input type="number" min={50} max={250} value={form.trestbps}
              onChange={e => num('trestbps', e.target.value)} className={inputCls} required />
          </Field>

          <Field label="Cholesterol" hint="mg/dl">
            <input type="number" min={100} max={600} value={form.chol}
              onChange={e => num('chol', e.target.value)} className={inputCls} required />
          </Field>

          <Field label="Max Heart Rate" hint="bpm">
            <input type="number" min={60} max={250} value={form.thalach}
              onChange={e => num('thalach', e.target.value)} className={inputCls} required />
          </Field>

          <Field label="Fasting Blood Sugar &gt;120 mg/dl">
            <select value={form.fbs} onChange={e => num('fbs', e.target.value)} className={inputCls}>
              <option value={0}>No</option>
              <option value={1}>Yes</option>
            </select>
          </Field>
        </div>
      </section>

      {/* Diagnostics */}
      <section>
        <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">Diagnostics</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <Field label="Resting ECG">
            <select value={form.restecg} onChange={e => num('restecg', e.target.value)} className={inputCls}>
              <option value={0}>Normal</option>
              <option value={1}>ST-T Wave Abnormality</option>
              <option value={2}>Left Ventricular Hypertrophy</option>
            </select>
          </Field>

          <Field label="ST Depression" hint="oldpeak">
            <input type="number" min={0} max={10} step={0.1} value={form.oldpeak}
              onChange={e => num('oldpeak', e.target.value)} className={inputCls} required />
          </Field>

          <Field label="ST Slope">
            <select value={form.slope} onChange={e => num('slope', e.target.value)} className={inputCls}>
              <option value={0}>Upsloping</option>
              <option value={1}>Flat</option>
              <option value={2}>Downsloping</option>
            </select>
          </Field>

          <Field label="Major Vessels" hint="0–3, fluoroscopy">
            <input type="number" min={0} max={3} value={form.ca}
              onChange={e => num('ca', e.target.value)} className={inputCls} required />
          </Field>

          <Field label="Thalassemia">
            <select value={form.thal} onChange={e => num('thal', e.target.value)} className={inputCls}>
              <option value={1}>Normal</option>
              <option value={2}>Reversible Defect</option>
              <option value={3}>Fixed Defect</option>
            </select>
          </Field>
        </div>
      </section>

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white font-semibold py-2.5 rounded-md transition-colors"
      >
        {loading ? 'Analysing…' : 'Predict Risk'}
      </button>
    </form>
  )
}
