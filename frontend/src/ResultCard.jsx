import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ReferenceLine, ResponsiveContainer, Cell
} from 'recharts'

function probabilityLabel(prob) {
  if (prob >= 0.75) return 'Very High'
  if (prob >= 0.5)  return 'High'
  if (prob >= 0.25) return 'Moderate'
  return 'Low'
}

// Top contributing feature → plain English summary
function topFactorSummary(factors) {
  if (!factors.length) return null
  const top = factors[0]
  const dir = top.impact > 0 ? 'increasing' : 'decreasing'
  // Feature names come as one-hot suffixes like "thal_2", "ca_0", "cp_1"
  const name = top.feature.replace(/_\d+$/, '').replace(/_/g, ' ')
  return `The strongest factor was ${name}, ${dir} predicted risk.`
}

export default function ResultCard({ result }) {
  const { risk_label, probability, top_factors } = result
  const pct = Math.round(probability * 100)
  const isHigh = probability >= 0.5

  const chartData = top_factors.map(f => ({
    name: f.feature,
    impact: f.impact,
  }))

  return (
    <div className="mt-8 space-y-6">
      {/* Risk summary */}
      <div className={`rounded-lg p-5 border ${isHigh ? 'bg-red-50 border-red-200' : 'bg-green-50 border-green-200'}`}>
        <div className="flex items-center justify-between mb-3">
          <span className={`text-lg font-bold ${isHigh ? 'text-red-700' : 'text-green-700'}`}>
            {risk_label}
          </span>
          <span className="text-2xl font-bold text-gray-800">{pct}%</span>
        </div>

        {/* Probability bar */}
        <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
          <div
            className={`h-3 rounded-full transition-all duration-500 ${isHigh ? 'bg-red-500' : 'bg-green-500'}`}
            style={{ width: `${pct}%` }}
          />
        </div>
        <p className="mt-2 text-xs text-gray-500">
          {probabilityLabel(probability)} risk · {pct}% estimated probability of heart disease
        </p>
      </div>

      {/* SHAP chart */}
      {top_factors.length > 0 && (
        <div>
          <h2 className="text-sm font-semibold text-gray-700 mb-1">Top Contributing Factors</h2>
          <p className="text-xs text-gray-400 mb-3">{topFactorSummary(top_factors)}</p>

          <ResponsiveContainer width="100%" height={top_factors.length * 44 + 20}>
            <BarChart
              data={chartData}
              layout="vertical"
              margin={{ left: 8, right: 24, top: 4, bottom: 4 }}
            >
              <CartesianGrid strokeDasharray="3 3" horizontal={false} />
              <XAxis type="number" domain={['auto', 'auto']} tickFormatter={v => v.toFixed(3)} tick={{ fontSize: 11 }} />
              <YAxis type="category" dataKey="name" width={90} tick={{ fontSize: 11 }} />
              <Tooltip formatter={v => v.toFixed(4)} />
              <ReferenceLine x={0} stroke="#9ca3af" />
              <Bar dataKey="impact" radius={[0, 3, 3, 0]}>
                {chartData.map((d, i) => (
                  <Cell key={i} fill={d.impact > 0 ? '#ef4444' : '#22c55e'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
          <p className="text-xs text-gray-400 mt-1">
            Red = pushes toward disease &nbsp;·&nbsp; Green = pushes away from disease
          </p>
        </div>
      )}
    </div>
  )
}
