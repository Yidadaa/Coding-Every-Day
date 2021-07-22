import React, { useState } from 'react'
import logo from './logo.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="App">
      <div className="AppContent">
        <div className="Number">{count}</div>
        <button className="UpdateButton" onClick={() => setCount(count + 1)}>
          update
        </button>
      </div>
    </div>
  )
}

export default App
