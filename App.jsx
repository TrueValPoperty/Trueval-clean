
import { useState } from 'react'

function App() {
  const [form, setForm] = useState({ bedrooms: '', bathrooms: '', sqft: '', epc_rating: '', heating_type: '' })
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleChange = e => setForm({ ...form, [e.target.name]: e.target.value })

  const handleSubmit = async e => {
    e.preventDefault()
    setError(null)
    setResult(null)
    try {
      const res = await fetch('https://trueval-api.onrender.com/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form)
      })
      const data = await res.json()
      if (data.valuation) setResult(data.valuation)
      else setError(data.error || 'Unknown error')
    } catch (err) {
      setError('Server error')
    }
  }

  return (
    <div className="max-w-xl mx-auto mt-10 p-6 bg-white shadow rounded">
      <h1 className="text-2xl font-bold mb-4">TrueVal Property Valuation</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        {['bedrooms', 'bathrooms', 'sqft'].map(field => (
          <input
            key={field}
            name={field}
            type="number"
            value={form[field]}
            onChange={handleChange}
            required
            placeholder={field}
            className="w-full p-2 border rounded"
          />
        ))}
        <select name="epc_rating" value={form.epc_rating} onChange={handleChange} required className="w-full p-2 border rounded">
          <option value="">EPC Rating</option>
          {['A','B','C','D','E','F','G'].map(r => <option key={r}>{r}</option>)}
        </select>
        <select name="heating_type" value={form.heating_type} onChange={handleChange} required className="w-full p-2 border rounded">
          <option value="">Heating Type</option>
          {['gas','electric','oil','biomass','heat pump'].map(h => <option key={h}>{h}</option>)}
        </select>
        <button className="bg-blue-600 text-white px-4 py-2 rounded" type="submit">Get Valuation</button>
      </form>
      {result && <div className="mt-4 text-green-700 font-bold">Estimated Value: £{result.toLocaleString()}</div>}
      {error && <div className="mt-4 text-red-700">{error}</div>}
    </div>
  )
}

export default App
