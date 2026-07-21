function scoreAnswers({ age, sex, bp, chestPain, breathlessness, familyHistory, smoking }) {
  const flags = []

  if (age >= 45 && sex === 1) flags.push('Age \u2265 45 (male)')
  if (age >= 55 && sex === 0) flags.push('Age \u2265 55 (female)')
  if (bp === 'high') flags.push('High blood pressure (\u2265 140/90)')
  if (bp === 'elevated') flags.push('Elevated blood pressure (120-139/80-89)')
  if (chestPain === 'severe') flags.push('Frequent or severe chest pain during activity')
  if (chestPain === 'mild') flags.push('Occasional chest discomfort during activity')
  if (breathlessness === 'yes') flags.push('Shortness of breath during normal exercise')
  if (familyHistory === 'yes') flags.push('Family history of heart disease')
  if (smoking === 'yes') flags.push('Current smoker')

  return flags
}

function recommendation(flags) {
  const high = flags.some(f =>
    f.includes('chest pain') || f.includes('Shortness') || f.includes('High blood')
  )
  if (high || flags.length >= 3) {
    return {
      level: 'See a doctor soon',
      colour: 'red',
      advice: 'You have multiple risk indicators. Consider booking an appointment with your GP — an ECG and lipid panel would give a much clearer picture.',
    }
  }
  if (flags.length >= 2) {
    return {
      level: 'Worth monitoring',
      colour: 'amber',
      advice: "A few indicators are present. It's a good idea to discuss these with your GP at your next visit and ask about an ECG or blood pressure check.",
    }
  }
  return {
    level: 'Low immediate concern',
    colour: 'green',
    advice: 'No major risk indicators flagged. Keep up healthy habits — regular exercise, a balanced diet, and not smoking all help long-term heart health.',
  }
}

const colours = {
  red:   { card: 'bg-red-50 border-red-200',     label: 'text-red-700',   bar: 'bg-red-500' },
  amber: { card: 'bg-amber-50 border-amber-200', label: 'text-amber-700', bar: 'bg-amber-400' },
  green: { card: 'bg-green-50 border-green-200', label: 'text-green-700', bar: 'bg-green-500' },
}

export default function GuidanceCard({ answers, onBack }) {
  const flags = scoreAnswers(answers)
  const { level, colour, advice } = recommendation(flags)
  const c = colours[colour]

  return (
    <div className="space-y-5 mt-6">
      <div className={`rounded-lg p-5 border ${c.card}`}>
        <p className={`text-lg font-bold mb-1 ${c.label}`}>{level}</p>
        <p className="text-sm text-gray-600">{advice}</p>
      </div>

      {flags.length > 0 && (
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <p className="text-sm font-semibold text-gray-700 mb-3">Indicators noted ({flags.length})</p>
          <ul className="space-y-1">
            {flags.map((f, i) => (
              <li key={i} className="text-sm text-gray-600 flex items-start gap-2">
                <span className="mt-0.5 text-gray-400">•</span>{f}
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="rounded-lg p-4 bg-gray-50 border border-gray-200 text-xs text-gray-500 leading-relaxed">
        <strong>This is general guidance, not a risk score.</strong> A full assessment needs lab results
        (ECG, lipid panel, blood pressure reading). These observations are based only on self-reported
        information and should not replace advice from a healthcare professional.
      </div>

      <button onClick={onBack}
        className="text-sm text-gray-400 hover:text-gray-600 flex items-center gap-1">
        ← Start over
      </button>
    </div>
  )
}
